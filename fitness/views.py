from django.shortcuts import render,redirect

from rest_framework.views import APIView as View

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http.response import JsonResponse
from django.template.loader import render_to_string

from django.db.models import Q
from django.db.models import Sum
from django.utils import timezone


from . import calendar
from .models import FitnessCategory,FitnessMemory,FoodCategory,FoodMemory,Menu,MenuDetail,Trophy,TrophyUser,Target,Health
from .forms import YearMonthForm,FitnessCategoryForm,FitnessMemoryForm,MenuForm,MenuDetailForm,UUIDForm,FoodCategoryForm,FoodMemoryForm,TargetForm,HealthForm

import datetime


#TODO:django message framework 実装
from django.contrib import messages


class HomeView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        context = {}

        #カレンダーの表示
        form    = YearMonthForm(request.GET)
        today   = datetime.date.today()

        context["today"]    = today

        if form.is_valid():
            cleaned         = form.clean()
            selected_date   = datetime.datetime(year=cleaned["year"], month=cleaned["month"], day=1)
        else:
            selected_date   = datetime.datetime(year=today.year, month=today.month, day=1)

        context["selected_date"]                        = selected_date


        context["months"], context["years"]             = calendar.create_months_years(selected_date, today)
        context["last_month"], context["next_month"]    = calendar.create_last_next_month(selected_date)

        context["categories"]   = FitnessCategory.objects.filter(user=request.user.id).order_by("-dt")
        context["menus"]        = Menu.objects.filter(user=request.user.id).order_by("-dt")

        #FoodCategory
        context["food_categories"]  = FoodCategory.objects.filter(user=request.user.id).order_by("-dt")
        #FoodMemory.objects.filter(user=request.user.id).order_by("-dt")

        #カレンダーを作る
        month_date  = calendar.create_calendar(selected_date.year, selected_date.month)

        #FitnessMemoryの内容を含める
        for week in month_date:
            for date in week:
                if not date["day"]:
                    continue

                calendar_date       = date["day"]
                #カレンダーの日付で検索
                
                query = Q(user=request.user.id, exe_dt__year=calendar_date.year, exe_dt__month=calendar_date.month, exe_dt__day=calendar_date.day)

                #ここで新しい順に並べる(横並びの部分の左が新しいデータになる。)
                date["memories"]        = FitnessMemory.objects.filter(query).order_by("-dt")
                date["food_memories"]   = FoodMemory.objects.filter(query).order_by("-dt")

                #print(date["food_memories"])

                #日ごとの合計を記録
                memories_total          = FitnessMemory.objects.filter(query).order_by("dt").aggregate(Sum("time"))

                #このmemories_total["time__sum"]にはtimedeltaのオブジェクトが入っている、もしデータがない場合はNone
                if memories_total["time__sum"]:
                    # TODO:chart.jsでは時間でグラフを作れない。秒に統一させる(分単位で出したい場合は↓を60で割る、もしくはJS側で60で割る)
                    #date["memories_total"]  = memories_total["time__sum"].total_seconds() 
                    date["memories_total"]  = memories_total["time__sum"].total_seconds() // 60
                else:
                    date["memories_total"]  = 0



        context["month_date"]   = month_date
        context["trophies"]     = Trophy.objects.filter(user=request.user.id).order_by("-dt")


        #TODO:今月のフィットネスの集計を表示(カテゴリをループさせることで、カテゴリごとの集計ができる)
        month_category_times        = []
        month_category_total_times  = datetime.timedelta()

        for category in context["categories"]:

            dic = {}

            dic["category"] = category 
            fitness         = FitnessMemory.objects.filter(user=request.user.id, exe_dt__year=selected_date.year, exe_dt__month=selected_date.month, category=category ).aggregate(Sum("time"))

            if fitness["time__sum"]:

                dic["time"]         = fitness["time__sum"]

                #TODO:分単位にするため60で割って切り捨て
                #dic["time_second"]  = fitness["time__sum"].total_seconds()
                dic["time_second"]  = fitness["time__sum"].total_seconds() // 60

                #カテゴリの合計がある場合、合計に加算
                month_category_total_times += fitness["time__sum"]

            else:
                dic["time"]         = 0
                dic["time_second"]  = 0

            month_category_times.append(dic)


        context["month_category_times"]         = month_category_times
        context["month_category_total_times"]   = month_category_total_times



        #この原理を利用して1年分を月ごとに分けて集計する。(←グラフに利用できる)

        #selected_dateを起点に1月から順に追加していく。

        year_totals = []
        
        for i in range(1,13):
            dic = {}
            dic["month"]    = i

            fitness = FitnessMemory.objects.filter(user=request.user.id, exe_dt__year=selected_date.year, exe_dt__month=i ).aggregate(Sum("time"))

            if fitness["time__sum"]:
                dic["time"]         = fitness["time__sum"]

                #TODO:グラフの分単位表示のため、60で割って切り捨てる
                #dic["time_second"]  = fitness["time__sum"].total_seconds()
                dic["time_second"]  = fitness["time__sum"].total_seconds() // 60
            else:
                dic["time"]         = 0
                dic["time_second"]  = 0

            year_totals.append(dic)

        context["year_totals"] = year_totals

        
        now = timezone.now()

        #TODO:連続日数計算処理(forms.pyでも使うので、別ファイル化しても良いかも)
        serial      = 0 

        while True:
            #指定日付のデータが存在するかチェック
            serial_flag = FitnessMemory.objects.filter(user=request.user.id, exe_dt__year=now.year, exe_dt__month=now.month, exe_dt__day=now.day ).exists()

            if not serial_flag:
                break

            #1日前に戻る
            now -= datetime.timedelta(days=1)

            #連続日数を1増やす
            serial += 1

        context["serial"] = serial

        #連続日数が止まった時、トロフィーを剥奪
        """
        # 取得済みのトロフィーの中で、現在の連続日数記録よりも大きいものを取り出し、剥奪する。
        trophies = Trophy.objects.filter(serial__gt=serial,user=request.user)

        #トロフィーをループして取得処理を
        for trophy in trophies:
            trophy.user.remove(request.user)
            print("剥奪")
        """

        context["target"]   = Target.objects.filter(date__year=selected_date.year, date__month=selected_date.month, user=request.user.id).order_by("-dt").first()


        
        context["healthes"] = Health.objects.filter(user=request.user.id, date__year=selected_date.year, date__month=selected_date.month ).order_by("dt")
        context["health"]   = Health.objects.filter(user=request.user.id ).order_by("-dt").first()


        return render(request, 'fitness/home.html' ,context)

Home = HomeView.as_view()


class FitnessCategoryView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form            = FitnessCategoryForm(copied)

        if form.is_valid():
            form.save()

            messages.success(request, "フィットネスカテゴリを登録しました")

        return redirect("fitness:home")

    def put(self, request, *args, **kwargs):
        pass
    def delete(self, request, *args, **kwargs):
        pass

fitness_category = FitnessCategoryView.as_view()

class FitnessMemoryView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):

        data    = {"error":True}

        #TODO:以下3つのケースでFitnessMemoryを受け付ける

        #1:ストップウォッチから運動したケース
        #2:フィットネスメニューから運動したケース
        #3:手動記録追加にて手動で追加したケース

        categories  = request.POST.getlist("category")
        times       = request.POST.getlist("time")
        exe_dts     = request.POST.getlist("exe_dt")

        for category,time,exe_dt in zip(categories, times, exe_dts):
            dic = {}

            dic["category"] = category
            dic["time"]     = time
            dic["exe_dt"]   = exe_dt
            dic["user"]     = request.user.id

            form    = FitnessMemoryForm(dic)

            if form.is_valid():
                print("保存")
                form.save()
                messages.success(request, "フィットネスを登録しました")
            else:
                print(form.errors)


        #TODO:レンダリングは左の領域を返す。
        data["error"]   = False


        return JsonResponse(data)


    def put(self, request, *args, **kwargs):
        pass
    def delete(self, request, *args, **kwargs):
        pass

fitness_memory = FitnessMemoryView.as_view()



class FoodCategoryView(LoginRequiredMixin,View):


    def get(self, request, *args, **kwargs):
        pass


    def post(self, request, *args, **kwargs):

        data        = {"error":True}

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = FoodCategoryForm(copied)

        if not form.is_valid():
            print(form.errors)
            return redirect("fitness:home")

        data["error"]   = False
        form.save()
        messages.success(request, "フードカテゴリを登録しました")

        return redirect("fitness:home")


    def put(self, request, *args, **kwargs):
        pass
    def delete(self, request, *args, **kwargs):
        pass

food_category   = FoodCategoryView.as_view()



class FoodMemoryView(LoginRequiredMixin,View):



    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):

        data        = {"error":True}

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = FoodMemoryForm(copied, request.FILES)

        if not form.is_valid():
            print(form.errors)
            return redirect("fitness:home")

        data["error"]   = False
        food = form.save()
        print(food)
        messages.success(request, "フードを登録しました")

        return redirect("fitness:home")

    def put(self, request, *args, **kwargs):
        pass
    def delete(self, request, *args, **kwargs):
        pass


food_memory = FoodMemoryView.as_view()


class MenuView(LoginRequiredMixin,View):

    def render_menu(self, request, context):
        context["categories"]   = FitnessCategory.objects.filter(user=request.user.id).order_by("-dt")
        context["menus"]        = Menu.objects.filter(user=request.user.id).order_by("-dt")

        return render_to_string("fitness/fitness_menu.html", context, request)

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        data        = {"error":True}

        #ここからMenuとMenuDetailを連続で保存する。

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = MenuForm(copied)

        if not form.is_valid():
            print(form.errors)
            return JsonResponse(data)
            #return redirect("fitness:home")

        #Menuの保存(返り値はMenuDetailのmenuフィールドで使うので取っておく)
        menu    = form.save()



        #MenuDetailの保存処理(同じname属性が複数ある場合、全て取得するには、.getlist()を使う。返り値はリスト)
        times       = request.POST.getlist("time")
        categories  = request.POST.getlist("category")

        sort        = 1

        #zipを使って2つのリストを同時にループする。
        for time,category in zip(times, categories):

            dic             = {}
            dic["user"]     = request.user.id
            dic["menu"]     = menu.id
            dic["time"]     = time
            dic["category"] = category
            dic["sort"]     = sort

            form            = MenuDetailForm(dic)

            if form.is_valid():
                print("保存")
                form.save()
            else:
                print(form.errors)

            sort += 1

        context = {}

        data["content"]     = self.render_menu(request,context)
        data["error"]       = False

        messages.success(request, "フィットネスメニューを登録しました")

        return JsonResponse(data)

    #この編集はMenuとMenuDetailの編集を兼ねる
    def put(self, request, *args, **kwargs):
        data        = {"error":True}

        #編集対象のMenuが指定されていない場合は終わる
        if "pk" not in kwargs:
            return JsonResponse(data)

        #Menuの編集
        menu        = Menu.objects.filter(id=kwargs["pk"],user=request.user.id).first()

        if not menu:
            return JsonResponse(data)

        copied          = request.data.copy()
        copied["user"]  = request.user.id

        form    = MenuForm(copied, instance=menu)

        if not form.is_valid():
            print(form.errors)
            return JsonResponse(data)

        menu    = form.save()

        #MenuDetailの編集

        #MenuDetailのidを抜き取る
        id_list     = request.POST.getlist("id")
        times       = request.POST.getlist("time")
        categories  = request.POST.getlist("category")

        sort        = 1
        for id,time,category in zip(id_list, times, categories):

            #編集対象のMenuDetailの特定
            #ここで空欄の場合は検索しないようにしておかないと、有効なUUIDではありませんというエラーができて、MenuDetailの追加ができない。
            #ここはuuid型であることをチェックしたほうがよい(現状空文字列とUUIDの2種類しか入らないので、これでも機能はする)
            if id:
                menu_detail = MenuDetail.objects.filter(id=id,user=request.user.id).first()
            else:
                menu_detail = None

            dic             = {}
            dic["user"]     = request.user.id
            dic["menu"]     = menu.id
            dic["time"]     = time
            dic["category"] = category
            dic["sort"]     = sort

            #ここでmenu_detailがNoneなら新しく追加される
            form            = MenuDetailForm(dic, instance=menu_detail)

            if form.is_valid():
                form.save()
            else:
                print(form.errors)

            sort += 1

        context = {}
        data["content"]     = self.render_menu(request,context)
        data["error"]       = False

        messages.success(request, "フィットネスメニューを編集しました")


        return JsonResponse(data)
        
    #ここの削除はMenuとMenuDetailの削除を兼ねる
    def delete(self, request, *args, **kwargs):
        data        = {"error":True}
        context     = {}

        if "pk" not in kwargs:
            return JsonResponse(data)

        #Menuの削除
        menu        = Menu.objects.filter(id=kwargs["pk"],user=request.user.id).first()

        if menu:
            menu.delete()
            data["content"] = self.render_menu(request,context)
            data["error"]   = False
            return JsonResponse(data)

        #MenuDetailの削除
        menu_detail = MenuDetail.objects.filter(id=kwargs["pk"],user=request.user.id).first()

        if menu_detail:
            menu_detail.delete()
            data["content"] = self.render_menu(request,context)
            data["error"]   = False

        return JsonResponse(data)

menu    = MenuView.as_view()


class TargetView(LoginRequiredMixin,View):

    def render_target(self,request,context):

        #ここでselected_dateは使えないので、form.save()の返り値から受け取る
        #context["target"]   = Target.objects.filter(date__year=selected_date.year, date__month=selected_date.month, user=request.user.id).order_by("-dt").first()

        return render_to_string("fitness/parts/target.html", context, request)

    def post(self, request, *args, **kwargs):

        data    = {"error":True}
        context = {}

        #kwargsを使った投稿と編集の両立
        if "pk" in kwargs:
            target      = Target.objects.filter(user=request.user.id, id=kwargs["pk"]).first()
        else:
            target      = Target()

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = TargetForm(copied, instance=target)

        if form.is_valid():
            target      = form.save()
            messages.success(request, "今月の目標を登録しました")


        context["target"]   = target

        data["content"]     = self.render_target(request,context)
        data["error"]       = False

        return JsonResponse(data)

    def patch(self, request, *args, **kwargs):

        data    = {"error":True}
        context = {}

        if "pk" not in kwargs:
            return JsonResponse(data)

        target      = Target.objects.filter(user=request.user.id, id=kwargs["pk"]).first()
        target.done = not target.done
        target.save()

        print(target)
        print(target.done)

        context["target"]   = target

        data["content"]     = self.render_target(request,context)
        data["error"]       = False

        return JsonResponse(data)

target  = TargetView.as_view()

class HealthView(LoginRequiredMixin,View):

    def post(self, request, *args, **kwargs):

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = HealthForm(copied)

        if form.is_valid():
            form.save()

        return redirect("fitness:home")

health  = HealthView.as_view()

