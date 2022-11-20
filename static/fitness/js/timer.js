//グローバル変数に、MenuDetailのカテゴリと時間を入れる。
MENU_DETAILS    = []; 
//現在実行中のMenuDetailのindex番号
DOING_DETAIL    = 0;

//稼働中のtimerがストップウォッチであるか否か
WATCH           = false;


// MENUとストップウォッチの共存はNGで
window.addEventListener("load" , function (){

    //Menuを始める(MenuDetailを取得して、モーダルを表示、タイマー発動)
    $(document).on("click", ".menu_start", function(){ menu_pre_start(this); }); 

    //ストップウォッチで始める
    $(document).on("click", "#watch_start", function(){ watch_pre_start(this); }); 


    //====================================================-

    function timer_init(){
        //Timerオブジェクトを作る
        timer = new Timer();

        //時間経過したときのイベント
        timer.addEventListener('secondsUpdated', function (e) {
            $('#remain').html(timer.getTimeValues().toString());
        });

        //カウントダウン終了時のイベント
        timer.addEventListener('targetAchieved', function (e) {

            //TODO:カウントダウン終了時、一旦初期化する。これがないと次のタイマーが動かない。
            timer_init()


            //ここでtimer.start()を発動することはできない既に、Timerのオブジェクトが作られstartしているから。
            //stopで次のメニューに行けるようになる(startが発動できるようになる)
            //カウントダウンをしてくれない。(timer.jsの仕様？)
            //timer.stop()

            timer_init();


            //1個のMenuDetail終了時、次のMenuDetailに行くため、DOING_DETAILを1加算して、start_menu()を実行する
            DOING_DETAIL += 1;
            menu_start();
            play_music(ALARM);

        });
    }
    timer_init();

    //モーダルを閉じる時、タイマーをストップして初期化。
    $(document).on("click", ".modal_label" , function(){
        console.log("モーダルを閉じる")
        timer.stop();

        //ストップウォッチ稼働中の時、送信処理を実行
        if (WATCH){

            //フロッピーのアイコンをクリックした時だけ保存処理を実行する。
            if ($(this).hasClass("modal_label_save")){
                MENU_DETAILS[DOING_DETAIL]["time"] = $('#remain').text();
                fitness_memory_list_submit(MENU_DETAILS);
            }
        }

        MENU_DETAILS = [];
        DOING_DETAIL = 0;

        //閉じる時、一時停止の表記を元に戻す
        $("#timer_pause").children(".fa-play").css({"display":"none"});
        $("#timer_pause").children(".fa-pause").css({"display":"inline"});

        //TODO:タイマーを動かした後、ストップウォッチを動かそうとした時、ストップウォッチが動かない問題の対策
        //タイマーの後にタイマーを動かした場合は問題なく動く。
        timer_init();

        console.log("閉じる");
    });




    //ポーズするときのイベント
    $(document).on("click", "#timer_pause" , function(){
        //isRunning()で動作中かどうかを判定できる
        if (timer.isRunning()){
            console.log("一時停止");
            timer.pause();

            $("#timer_pause").children(".fa-play").css({"display":"inline"});
            $("#timer_pause").children(".fa-pause").css({"display":"none"});
        }
        else{
            console.log("再開");
            timer.start();
            $("#timer_pause").children(".fa-play").css({"display":"none"});
            $("#timer_pause").children(".fa-pause").css({"display":"inline"});
        }
    });

    //====================================================-

});
function watch_pre_start(elem){

    let form_elem   = $(elem).parents("form");

    let categories  = $(form_elem).children("[name='category']");
    let length      = categories.length;

    for (let i=0;i<length;i++){
        let dic         = {};

        dic["category"] = categories.eq(i).val();
        dic["name"]     = categories.eq(i).children("option:selected").text();

        if ( dic["category"] === ""){
            return false;
        }
        MENU_DETAILS.push(dic);
    }

    console.log(MENU_DETAILS);

    WATCH   = true;

    menu_start();
}

function menu_pre_start(elem){

    let form_elem   = $(elem).parents("form");

    let categories  = $(form_elem).children("[name='category']");
    let names       = $(form_elem).children("[name='category_name']");
    let times       = $(form_elem).children("[name='time']");

    let length      = categories.length;

    for (let i=0;i<length;i++){
        let dic     = {};

        dic["category"] = categories.eq(i).val();
        dic["name"]     = names.eq(i).val();
        dic["time"]     = times.eq(i).val();

        MENU_DETAILS.push(dic);
    }

    WATCH   = false;

    menu_start();
}
function menu_start(){

    console.log("start");

    //モーダルを表示
    $("#modal_chk").prop("checked",true);

    //メニュー実行時はフロッピーを非表示
    if (WATCH){
        $(".modal_label_save").css({"display":""});
    }
    else{
        $(".modal_label_save").css({"display":"none"});
    }


    //現在実行中のMenuDetailのindex番号がはみ出ている時、0に戻してreturnを実行する
    if ( MENU_DETAILS.length <= DOING_DETAIL ){
        DOING_DETAIL = 0;
        //ここで実行したフィットネスの記録をするAjaxを実行
        fitness_memory_list_submit(MENU_DETAILS);

        //TODO:終わったら初期化して、モーダルを閉じる

        MENU_DETAILS = [];
        DOING_DETAIL = 0;
        $("#modal_chk").prop("checked",false);

        return;
    }

    if (WATCH){
        console.log("ウォッチスタート")

        //メニューを動かした後、タイマーを動かす際、timer_init()を実行しないと動いてくれない問題
        //timer.start({countdown: false,  startValues: {seconds: 0 } });
        timer.start({countdown: false });
    }
    else{
        console.log("実行");
        timer.start({countdown: true, startValues: {seconds: MENU_DETAILS[DOING_DETAIL]["time"] }});
    }

    //時間とカテゴリの表示
    $("#doing_category").html(MENU_DETAILS[DOING_DETAIL]["name"]);
    $('#remain').html(timer.getTimeValues().toString());


}
function play_music(url) {

    //CHECK:Ubuntu20.04にて確認
    //別で音声再生中、音がならないことがある。

    let sound       = new Audio();
    sound.onerror   = function() { console.log("再生できませんでした"); }
    sound.src       = url;
    sound.play();

}
