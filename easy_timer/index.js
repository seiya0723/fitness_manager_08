//グローバル変数に、MenuDetailのカテゴリと時間を入れる。
MENU_DETAILS    = [
    {"category":"スクワット","timer": 10},
    {"category":"腕立て伏せ","timer": 15},
];
//現在実行中のMenuDetailのindex番号
DOING_DETAIL    = 0;



window.addEventListener("load" , function (){

    $(document).on("click", "#start_menu" , function(){ start_menu(); });

    

});

function start_menu(){

    timer = new Timer();

    $(document).on("click", "#cancel_menu" , function(){ 
        DOING_DETAIL = 0;
        timer.stop();
    });
    $(document).on("click", "#pause_menu" , function(){ 
        console.log("ポーズ")
        timer.pause();
    });

    //現在実行中のMenuDetailのindex番号がはみ出ている時、0に戻してreturnを実行する
    if ( MENU_DETAILS.length <= DOING_DETAIL ){
        DOING_DETAIL = 0;
        return;
    }

    //タイマーのセット
    timer.start({countdown: true, startValues: {seconds: MENU_DETAILS[DOING_DETAIL]["timer"] }});

    //設定した時間とカテゴリの表示
    $("#doing_category").html(MENU_DETAILS[DOING_DETAIL]["category"]);
    $('#remain').html(timer.getTimeValues().toString());

    //カウントダウン時のイベント
    timer.addEventListener('secondsUpdated', function (e) {
        $('#remain').html(timer.getTimeValues().toString());
    });

    //カウントダウン終了時のイベント
    timer.addEventListener('targetAchieved', function (e) {

        //1個のMenuDetail終了時、次のMenuDetailに行くため、DOING_DETAILを1加算して、start_menu()を実行する
        DOING_DETAIL += 1;
        start_menu();

        //ここで音楽を鳴らす
        play_music("button.mp3");
    });



}
function play_music(url) {
    let sound       = new Audio();
    sound.onerror   = function() { console.log("再生できませんでした"); }
    sound.src       = url;
    sound.play();
}


