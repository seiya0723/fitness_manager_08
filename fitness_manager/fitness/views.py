from django.shortcuts import render,redirect

from rest_framework.views import APIView as View

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http.response import JsonResponse
from django.template.loader import render_to_string

from . import calendar
from .models import FitnessCategory,FitnessMemory,FoodCategory,FoodMemory,Menu,MenuDetail,Trophy,TrophyUser
from .forms import YearMonthForm,FitnessCategoryForm,FitnessMemoryForm,MenuForm,MenuDetailForm,UUIDForm

import datetime


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


        #カレンダーを作る
        month_date  = calendar.create_calendar(selected_date.year, selected_date.month)

        #TODO:FitnessMemoryの内容を含める
        for week in month_date:
            for date in week:
                if not date["day"]:
                    continue

                calendar_date   = date["day"]

                #カレンダーの日付で検索
                date["memories"]    = FitnessMemory.objects.filter(user=request.user.id, exe_dt__year=calendar_date.year, exe_dt__month=calendar_date.month, exe_dt__day=calendar_date.day ).order_by("dt")


        context["month_date"]   = month_date



        #自分が投稿した今月のフィットネス記録を日付順(古いほうが先)で取り出す
        memories    = FitnessMemory.objects.filter(user=request.user.id, exe_dt__year=selected_date.year, exe_dt__month=selected_date.month ).order_by("dt")

        memories_lists  = []
        memories_list   = {}

        old_date        = datetime.date(1,1,1)
        
        for memory in memories:
            #exe_dtは日時型なので、日付型に直してnow_dateとする
            now_date    = datetime.date(memory.exe_dt.year,memory.exe_dt.month,memory.exe_dt.day)

            if now_date != old_date:

                #ここでdict.copy()でappendしないと、次のmemories_listで上書きされてしまう
                #https://gist.github.com/dogrunjp/9748789

                if {} != memories_list.copy():
                    memories_lists.append(memories_list.copy())

                memories_list["date"]       = now_date
                memories_list["memories"]   = [ memory ]

                old_date    = now_date
            else:
                memories_list["memories"].append(memory)

        #最後のmemories_listをappend
        memories_lists.append(memories_list.copy())
        print(memories_lists)






        #TODO:↑と↓のデータを一本化。month_dateに↓のFitnessMemoryのデータを日付ごとに含ませる

        #自分が投稿した今月のフィットネス記録を日付順(古いほうが先)で取り出す
        memories    = FitnessMemory.objects.filter(user=request.user.id, exe_dt__year=selected_date.year, exe_dt__month=selected_date.month ).order_by("dt")

        memories_lists  = []
        memories_list   = {}

        old_date        = datetime.date(1,1,1)
        
        for memory in memories:
            #exe_dtは日時型なので、日付型に直してnow_dateとする
            now_date    = datetime.date(memory.exe_dt.year,memory.exe_dt.month,memory.exe_dt.day)

            if now_date != old_date:

                #ここでdict.copy()でappendしないと、次のmemories_listで上書きされてしまう
                #https://gist.github.com/dogrunjp/9748789

                if {} != memories_list.copy():
                    memories_lists.append(memories_list.copy())

                memories_list["date"]       = now_date
                memories_list["memories"]   = [ memory ]

                old_date    = now_date
            else:
                memories_list["memories"].append(memory)

        #最後のmemories_listをappend
        memories_lists.append(memories_list.copy())
        print(memories_lists)

        context["memories_lists"]   = memories_lists




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
                form.save()


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
        pass
    def put(self, request, *args, **kwargs):
        pass
    def delete(self, request, *args, **kwargs):
        pass

food_category   = FoodCategoryView.as_view()



class FoodMemoryView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        pass
    def put(self, request, *args, **kwargs):
        pass
    def delete(self, request, *args, **kwargs):
        pass


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

"""
class TrophyView(LoginRequiredMixin,View):
class TrophyUserView(LoginRequiredMixin,View):
"""



