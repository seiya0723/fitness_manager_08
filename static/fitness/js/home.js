//グローバル変数に、MenuDetailのカテゴリと時間を入れる。
MENU_DETAILS    = [];
//現在実行中のMenuDetailのindex番号
DOING_DETAIL    = 0;

window.addEventListener("load" , function (){

    //フィットネスメニューの追加と削除
    $(document).on("click",".menu_detail_create_row_add", function(){
        $(this).next(".menu_detail_create_form").append( $("#menu_detail_create_init").html() );
    });

    $(document).on("click",".menu_detail_create_delete",function(){ 
        //.remove()で要素自身を消す
        $(this).parents(".menu_detail_create_row").remove();
    });

    //MenuとMenuDetailの削除(この.menu_deleteも動的に追加される要素なので、documentから始める)
    $(document).on("click", "#menu_create_submit", function(){ menu_create(this); });
    $(document).on("click", ".menu_delete", function(){ menu_delete(this); });
    $(document).on("click", ".menu_edit_submit", function(){ menu_edit(this); });

    
    //Menuを始める(MenuDetailを取得して、モーダルを表示、タイマー発動)
    $(document).on("click", ".menu_start", function(){ menu_pre_start(this); });

    //TODO:ストップウォッチで始める。タイマーと共存させることで書く量を減らせるのでは？
    $(document).on("click", "#watch_start", function(){ watch_pre_start(this); });


    //新規作成時・編集時の並び替え
    let elem    = document.getElementById('fitness_menu_area');
    let target  = new MutationObserver(function(){ detail_sortable() });
    target.observe(elem, { "childList":true });

    function detail_sortable(){
        console.log("並び替え化");
        let sort_area = $(".menu_detail_create_form");
        for (let area of sort_area ){
            new Sortable(area, {
                handle: '.handle', 
                animation: 150,
                ghostClass: 'menu_detail_dragging', //ドラッグ中のクラス名
            });
        }
    }
    detail_sortable()


    //手動記録追加時の日付フォーム
    let today   = new Date();

    let year    = String(today.getFullYear());
    let month   = ("0" + String(today.getMonth() + 1) ).slice(-2);
    let day     = ("0" + String(today.getDate()) ).slice(-2);
    let hour    = ("0" + String(today.getHours()) ).slice(-2);
    let minute  = ("0" + String(today.getMinutes()) ).slice(-2);

    let date    = year + "-" + month + "-" + day + " " + hour + ":" + minute;

    let config_date = { 
        locale: "ja",
                enableTime: true,
        dateFormat: "Y-m-d H:i",
        defaultDate: date,
    }
    flatpickr("[name='exe_dt']",config_date);


    $(document).on("click", "#fitness_memory_submit", function() { fitness_memory_submit(this) });

});

function menu_create(elem){

    let form_elem   = $(elem).parents("form")

    let data        = new FormData( $(form_elem).get(0) );
    let url         = $(form_elem).prop("action");
    let method      = $(form_elem).prop("method");

    console.log("create")

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (!data.error){
            console.log("新規作成");
            $("#fitness_menu_area").html(data.content)
        }
        else{
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 

}
function menu_delete(elem){

    if (!confirm("削除しますか？")){
        return false;
    }

    let form_elem   = $(elem).parents("form")

    let url         = $(form_elem).prop("action");
    let method      = "DELETE";

    $.ajax({
        url: url,
        type: method,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (!data.error){
            console.log("削除");
            $("#fitness_menu_area").html(data.content)
        }
        else{
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 
}

function menu_edit(elem){

    let form_elem   = $(elem).parents("form")

    let data        = new FormData( $(form_elem).get(0) );
    let url         = $(form_elem).prop("action");
    let method      = "PUT";

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (!data.error){
            console.log("編集");
            $("#fitness_menu_area").html(data.content)
        }
        else{
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 

}

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
        console.log(dic)
        MENU_DETAILS.push(dic);
    }
    console.log(MENU_DETAILS);

    //モーダルを表示
    $("#modal_chk").prop("checked",true);

    menu_start(watch=true);
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

    console.log(MENU_DETAILS);

    //モーダルを表示
    $("#modal_chk").prop("checked",true);

    menu_start();
}
function menu_start(watch=false){

    //Timerオブジェクトを作る
    let timer = new Timer();

    //モーダルを閉じる時、タイマーをストップして初期化。
    $(document).on("click", ".modal_label" , function(){ 
        //watchであれば閉じる時に記録しておく
        if (watch){
            MENU_DETAILS[DOING_DETAIL]["time"] = $('#remain').text();
            fitness_memory_list_submit(MENU_DETAILS);
        }
        DOING_DETAIL = 0;
        MENU_DETAILS = [];
        timer.stop();
    }); 
    
    //ポーズするときのイベント
    $(document).on("click", "#timer_pause" , function(){ 
        //参照元: https://stackoverflow.com/questions/58050820/how-to-know-if-easytimer-is-stopped-or-not
        //isRunning()で動作中かどうかを判定できる
        if (timer.isRunning()){
            timer.pause();
            $(this).val("再開"); // TODO:ここでfontawesomeの再生と一時停止のアイコンを表示非表示させる
            //次回レッスンまでにfontawesomeの実装
        }
        else{
            timer.start();
            $(this).val("一時停止");
        }
    });

    //現在実行中のMenuDetailのindex番号がはみ出ている時、0に戻してreturnを実行する
    if ( MENU_DETAILS.length <= DOING_DETAIL ){
        DOING_DETAIL = 0;

        //TODO:ここで実行したフィットネスの記録をするAjaxを実行
        fitness_memory_list_submit(MENU_DETAILS);
        return;
    }

    //timerのセット
    if (watch){
        timer.start();
    }
    else{
        timer.start({countdown: true, startValues: {seconds: MENU_DETAILS[DOING_DETAIL]["time"] }});
    }

    //時間とカテゴリの表示
    $("#doing_category").html(MENU_DETAILS[DOING_DETAIL]["name"]);
    $('#remain').html(timer.getTimeValues().toString());

    //時間経過したときのイベント
    timer.addEventListener('secondsUpdated', function (e) {
        $('#remain').html(timer.getTimeValues().toString());
    });

    //カウントダウン終了時のイベント
    timer.addEventListener('targetAchieved', function (e) {
        //1個のMenuDetail終了時、次のMenuDetailに行くため、DOING_DETAILを1加算して、start_menu()を実行する
        DOING_DETAIL += 1;
        menu_start();

        //TODO:もしメニュー1個完了時の時刻を記録したい場合は、ここにMENU_DETAILS[DOING_DETAIL]["exe_dt"]に実行時間を記録する

        //ここで音楽を鳴らす
        play_music(ALARM);
    });

}
function play_music(url) {
    let sound       = new Audio();
    sound.onerror   = function() { console.log("再生できませんでした"); }   
    sound.src       = url;
    sound.play();
}


//手動記録用
function fitness_memory_submit(elem){

    let form_elem   = $(elem).parents("form")

    let data        = new FormData( $(form_elem).get(0) );
    let url         = $(form_elem).prop("action");
    let method      = $(form_elem).prop("method");

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (!data.error){
            console.log("投稿完了")
        }
        else{
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 

}

//ストップウォッチ+タイマー用
function fitness_memory_list_submit(details){

    let data        = new FormData();

    //現在時刻を入れる。
    let today   = new Date();
    let year    = String(today.getFullYear());
    let month   = ("0" + String(today.getMonth() + 1) ).slice(-2);
    let day     = ("0" + String(today.getDate()) ).slice(-2);
    let hour    = ("0" + String(today.getHours()) ).slice(-2);
    let minute  = ("0" + String(today.getMinutes()) ).slice(-2);

    let exe_dt  = year + "-" + month + "-" + day + " " + hour + ":" + minute;


    for (let detail of details){

        //ここはsetではなくappend(複数のcategory,time,exe_dtを入れることができる)
        // https://noauto-nolife.com/post/javascript-formdata-obj-set/
        data.append("category",detail["category"]);
        data.append("time",detail["time"]);
        data.append("exe_dt",exe_dt);
    }

    //FitnessMemory追加のビューへ
    let form_elem   = $("#fitness_memory_submit").parents("form")
    let url         = $(form_elem).prop("action");
    let method      = $(form_elem).prop("method");

    for (let v of data ){ console.log(v); }

    console.log(url   )
    console.log(method)

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (!data.error){
            console.log("投稿完了")
        }
        else{
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 

}

