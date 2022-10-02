window.addEventListener("load" , function (){

    //タイマーのイベントリスナ
    $("#timer_start").on("click",function(){ 
        if (TIMER){
            //一時停止する時
            TIMER=false;
            $("#timer_reset").css({"display":"inline-block"});
        }
        else{
            //開始もしくは一時停止から復帰する時
            timer();
            $("#timer_reset").css({"display":"none"});
        }
    });
    $("#timer_reset").on("click",function(){ timer_reset(); });

    //グローバル変数を初期化
    timer_reset();

    //ストップウォッチのイベントリスナ
    $("#watch_start").on("click",function(){ 
        //動作中で停止、停止中で動作
        if (WATCH){
            WATCH=false;
            $("#watch_reset").css({"display":"inline-block"});
        }
        else{
            watch();
            $("#watch_reset").css({"display":"none"});
            $("#watch_rap").css({"display":"inline-block"});
        }
    });
    $("#watch_rap"  ).on("click",function(){ watch_rap(); });
    $("#watch_reset").on("click",function(){ watch_reset(); });
    //グローバル変数を初期化
    watch_reset();

});





//TODO:新しいタイマーの仕組みを作る
/*
    - 複数のDetailを含んだ配列(グローバル変数)を作る
    - カウントダウンの処理は↓のtimer関数を踏襲
    - setIntervalを使用する(関数実行中に自身の関数を呼び出す構図はやや複雑)
    - タイマーが終了する時、配列の添字を1追加(この時、配列の長さを超過する時、)

    
    */

//TODO:しかし、この複雑な仕組みを今から一から作るとなると、あまりにも時間がかかりすぎる。
//ストップウォッチ、タイマー系ライブラリであるEasyTimer.jsを使っても良いのでは？
//https://albert-gonzalez.github.io/easytimer.js/



function timer(){

    TIMER_OLD_TIME  = Date.now();

    //セットされたタイマーの時間を計算する(ミリ秒)
    //let set_remain  = ( Number($("#timer_hour").val())*60*60 + Number($("#timer_minute").val())*60 + Number($("#timer_second").val()) )*1000 + 1000;  // 1000ミリ秒追加するだけで良いのでは？

    let set_remain  = ( Number($("#timer_second").val()) )*1000 + 1000;

    console.log(set_remain);

    function remain_calc(){

        //タイムアウトIDを作っておく(clearTimeout用)
        let timeout_id  = setTimeout(remain_calc, 10);

        //現在時刻から過去時刻を引く
        let progress        = TIMER_TEMP + Date.now() - TIMER_OLD_TIME;

        //経過ミリ秒
        let TIMER_REMAIN    = set_remain - progress;

        //残り時間表示処理(Math.floorで小数は切り捨て)←切り上げだと、hourとminuteはズレる。
        let remain_hour     = ("0" + String(Math.floor(TIMER_REMAIN/3600000))).slice(-2);
        let remain_minute   = ("0" + String(Math.floor((TIMER_REMAIN%3600000)/60000))).slice(-2);
        let remain_second   = ("0" + String(Math.floor((TIMER_REMAIN%60000)/1000))).slice(-2);

        //時間が経ったかどうかの判定
        if (TIMER_REMAIN <= 1000){
            console.log("時間が経ちました");
            TIMER   = false;
            clearTimeout(timeout_id);
        }

        //停止
        if (!TIMER){
            //現在の進捗状況をTIMER_TEMPに入れる。
            TIMER_TEMP  = TIMER_TEMP + Date.now() - TIMER_OLD_TIME;

            //TIPS:setTimeoutを終了させる時は、returnではなくclearTimeoutを使う。
            clearTimeout(timeout_id);
        }

        //残り時間を描画する(残り0秒未満は描画しない)
        if (TIMER_REMAIN >= 0){
            remain_str  = remain_hour + "時間" + remain_minute + "分" + remain_second + "秒";
            $("#remain").html(remain_str);
        }
    }

    //開始(既にスタートしている場合は実行しない)
    if (!TIMER && set_remain > 0){
        TIMER   = true;
        remain_calc();
    }
}

function timer_reset(){
    //タイマー動作チェックグローバル変数(falseで停止中)
    TIMER           = false;
    TIMER_REMAIN    = 0;
    TIMER_TEMP      = 0;
    TIMER_OLD_TIME  = 0;

    $("#remain").html("00時間00分00秒");
    $("#timer_reset").css({"display":"none"});
}

function watch(){

    WATCH_OLD_TIME  = Date.now();

    function count_calc(){

        //タイムアウトIDを作っておく(clearTimeout用)
        let timeout_id  = setTimeout(count_calc, 10);

        //現在時刻から過去時刻を引く
        let progress    = WATCH_TEMP + Date.now() - WATCH_OLD_TIME;

        //経過時間表示処理(小数は切り捨て)
        let progress_hour           = ("0" + String( Math.floor(progress/3600000) )         ).slice(-2);
        let progress_minute         = ("0" + String( Math.floor((progress%3600000)/60000) ) ).slice(-2);
        let progress_second         = ("0" + String( Math.floor((progress%60000)/1000) )    ).slice(-2);
        let progress_millisecond    = ("0" + String( Math.floor((progress%1000)/10) )       ).slice(-2);

        //停止
        if (!WATCH){
            //現在の進捗状況をWATCH_TEMPに入れる。
            WATCH_TEMP  = WATCH_TEMP + Date.now() - WATCH_OLD_TIME;

            //TIPS:setTimeoutを終了させる時は、returnではなくclearTimeoutを使う。
            clearTimeout(timeout_id);
        }

        //描画
        WATCH_STR   = progress_hour + "時間" + progress_minute + "分" + progress_second + "秒" + progress_millisecond + "ミリ秒";
        $("#progress").html(WATCH_STR);
    }

    //開始(既にスタートしている場合は実行しない)
    if (!WATCH){
        WATCH   = true;
        count_calc();
    }

}
//リセット処理
function watch_reset(){
    console.log("リセット");

    //ストップウォッチの動作チェックグローバル変数(falseで停止中)
    WATCH           = false;
    WATCH_TEMP      = 0;
    WATCH_OLD_TIME  = 0;
    //ラップ用
    WATCH_RAP_COUNT = 0;
    WATCH_STR       = "";

    $("#rap_area").html("");
    $("#progress").html("00時間00分00秒00ミリ秒");

    $("#watch_reset").css({"display":"none"});
    $("#watch_rap").css({"display":"none"});
}
//ラップ処理
function watch_rap(){
    WATCH_RAP_COUNT += 1;
    $("#rap_area").append("<div>ラップ:#" + String(WATCH_RAP_COUNT) + " " + WATCH_STR + "</div>");
}

