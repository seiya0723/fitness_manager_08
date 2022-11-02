import datetime 

from .models import FitnessMemory,FoodMemory

def create_calendar(year,month):

    #今月の初日を指定
    dt  = datetime.date(year,month,1)

    #calendarはweekのリスト、weekは日付のリスト
    calendar    = []
    week        = []

    
    #TODO:先月と来月の日付も入れたい場合の対策

    """
    1. 空欄を入れるのではなく、timedeltaで加減算した値を入れる
    2. 今月でない日付の場合は、テンプレート側で目立たないように装飾を入れるため、 to_monthのキーにFalseを入れておく。
    3. 今月のデータだけ表示する時、to_monthを元に分岐させる
    """

    #月始めが日曜日以外の場合、空欄を追加する。
    if dt.weekday() != 6:
        week    = [ {"day":""} for i in range(dt.weekday()+1) ]

    #1日ずつ追加して月が変わったらループ終了
    while True:

        #week.append({"day":dt.day}) #TODO:←ここでdt.dayだけ入れているが、dateオブジェクトを入れる方が良いのでは？
        week.append({"day": dt})
        dt += datetime.timedelta(days=1)

        #週末になるたびに追加する。
        if dt.weekday() == 6:
            calendar.append(week)
            week    = []

        #月が変わったら終了
        if month != dt.month:
            #一ヶ月の最終週を追加する。
            if dt.weekday() != 6:

                #最終週の空白を追加
                for i in range(6-dt.weekday()):
                    week.append({"day":""})

                calendar.append(week)

            break

    return calendar

    #最終的に作られるcalendarのイメージ。(dayの値はdate型)
    """
    [ [ {'day':''  }, {'day':''  }, {'day':'1' }, {'day':'2' }, {'day': '3' }, {'day':'4' }, {'day': '5' } ],
      [ {'day':'6' }, {'day':'7' }, {'day':'8' }, {'day':'9' }, {'day': '10'}, {'day':'11'}, {'day': '12'} ],
      [ {'day':'13'}, {'day':'14'}, {'day':'15'}, {'day':'16'}, {'day': '17'}, {'day':'18'}, {'day': '19'} ],
      [ {'day':'20'}, {'day':'21'}, {'day':'22'}, {'day':'23'}, {'day': '24'}, {'day':'25'}, {'day': '26'} ],
      [ {'day':'27'}, {'day':'28'}, {'day':'29'}, {'day':'30'}, {'day': ''  }, {'day':''  }, {'day': ''  } ]
      ]
    """


#カレンダーの年の選択肢(リスト)を作る
def create_months_years(selected_date, today):

    months  = [ i for i in range(1,13) ]

    #TODO:最新と最古のデータ
    """
    oldest  = Topic.objects.order_by( "dt").first()
    newest  = Topic.objects.order_by("-dt").first()
    """

    #TODO:存在チェックを行った上で、比較をする
    #oldest  = FitnessMemory.objects.order_by( "exe_dt").first()
    #newest  = FitnessMemory.objects.order_by("-exe_dt").first()
    #oldest  = FoodMemory.objects.order_by( "exe_dt").first()
    #newest  = FoodMemory.objects.order_by("-exe_dt").first()


    oldest  = None
    newest  = None

    #最新最古のデータと指定された日付の年を比較。年の選択肢を作る
    #Date型とDateTime型でもyearだけ比較できればOK
    if oldest and newest:
        if selected_date.year < oldest.exe_dt.year:
            years = [ i for i in range(selected_date.year, newest.exe_dt.year+1)]
        elif newest.exe_dt.year < selected_date.year:
            years = [ i for i in range(oldest.exe_dt.year, selected_date.year+1)]  
        else:
            years = [ i for i in range(oldest.exe_dt.year, newest.exe_dt.year+1)]
    else:
        if selected_date.year < today.year:
            years = [ i for i in range(selected_date.year, today.year+1)]
        else:
            years = [ i for i in range(today.year, selected_date.year+1)]
    
    return months, years


#先月と来月のdatetimeオブジェクトを作る
def create_last_next_month(selected_date):

    #timedeltaにはdaysの加減算までしか用意されていない(月の加減算はできない)
    #next_month      = selected_date + timedelta(months=1)
    #last_month      = selected_date - timedelta(months=1)

    if selected_date.month == 12: 
        next_month   = datetime.date( year=selected_date.year+1 , month=1                     , day=1 )
        last_month   = datetime.date( year=selected_date.year   , month=selected_date.month-1 , day=1 )
    elif selected_date.month == 1:
        next_month   = datetime.date( year=selected_date.year   , month=selected_date.month+1 , day=1 )
        last_month   = datetime.date( year=selected_date.year-1 , month=12 ,                    day=1 )
    else:
        next_month   = datetime.date( year=selected_date.year   , month=selected_date.month+1 , day=1 )
        last_month   = datetime.date( year=selected_date.year   , month=selected_date.month-1 , day=1 )
    
    return last_month, next_month


