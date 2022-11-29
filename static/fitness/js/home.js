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
    
    //モーダルを表示した状態で更新すると表示されっぱなしになるので、ロードした時点で消しておく。
    $("#modal_chk").prop("checked", false);

    //メニューの編集もチェックを消しておく。
    $(".menu_edit_chk").prop("checked",false);


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

    let config_dt = { 
        locale: "ja",
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        defaultDate: date,
    }
    //TODO:クラス名で指定する flatpickr_dt
    //flatpickr("[name='exe_dt']",config_dt);
    flatpickr(".flatpickr_dt",config_dt);

    let config_date = { 
        locale: "ja",
        dateFormat: "Y-m-d",
        defaultDate: date,
    }
    //TODO:クラス名で指定する flatpickr_date
    //flatpickr("[name='date']",config_date);
    flatpickr(".flatpickr_date",config_date);

    $(document).on("click", "#fitness_memory_submit", function() { fitness_memory_submit(this) });


    //TODO:カレンダーの日付をクリックした時、日ごとのページへジャンプする
    $(document).on("click",".calendar_day_exist", function(){
        //日付を抜き取る
        let day = $(this).children(".calendar_day").text();

        //日ごとにチェックを入れる
        $("#tab_radio_2").prop("checked",true);

        //スクロールする
        //参照元: https://qiita.com/yamaguchi_takashi/items/edce735e825631993a74
        $("html,body").animate({scrollTop:$("#day_"+day).offset().top}, 100);
    });


    $(document).on("click", ".target_done", function(){ target_done(this); });
    $(document).on("click", ".target_submit", function(){ target_submit(this); });

    //音量の調整
    $(document).on("change",".volume_input", function(){ volume_input(this)  });


    //DjangoMessageFrameworkは5秒経ったら自動的に消える
    setTimeout(function(){
        $(".message_body").css({"display":"none"});
    }, 5000);

    //idが被るので、いつものcheckboxは通用しない
    //DjangoMessageFrameworkの削除
    $(document).on("click", ".message_delete", function(){ 
        $(this).parents(".message_body").css({"display":"none"});
    });


    //TODO:inputタグでEnterキーが押されたら無効化する。
    $("input").on("keydown", function(e) {
        if ((e.keyCode && e.keyCode === 13)) {
            return false;
        }
    });

});

function menu_create(elem){

    let form_elem   = $(elem).parents("form")

    let data        = new FormData( $(form_elem).get(0) );
    let url         = $(form_elem).prop("action");
    let method      = $(form_elem).prop("method");


    //===========================

    //複数ある hours minutes seconds を組み合わせる。
    let hours_list      = data.getAll("hours");
    let minutes_list    = data.getAll("minutes");
    let seconds_list    = data.getAll("seconds");

    let length          = hours_list.length;

    let time_list       = [];
    for (let i=0;i<length;i++){
        time_list.push( Number(hours_list[i])*3600 + Number(minutes_list[i])*60 + Number(seconds_list[i]) );
    }

    //timeをリストにするには、.set()で上書きするのではなく、.appendで追加する。
    for (let time of time_list){
        data.append("time", time);
    }

    //===========================



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


//手動記録用
function fitness_memory_submit(elem){

    let form_elem   = $(elem).parents("form")

    let data        = new FormData( $(form_elem).get(0) );
    let url         = $(form_elem).prop("action");
    let method      = $(form_elem).prop("method");

    //TODO:ここでhours minutes secondsを修正する。
    data.set("time" , Number(data.get("hours"))*3600 + Number(data.get("minutes"))*60 + Number(data.get("seconds")) );

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
            window.location.replace("");
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
    let second  = ("0" + String(today.getSeconds()) ).slice(-2);

    let exe_dt  = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second;


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
            console.log("投稿完了");

            //TODO:selected_dateをどうやって表現するか？それができないのであればJS側から更新したほうが良い
            window.location.replace("");
        }
        else{
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 

}


function target_submit(elem){

    let form_elem   = $(elem).parents("form");


    let data    = new FormData( $(form_elem).get(0) );
    let url     = $(form_elem).prop("action");
    let method  = $(form_elem).prop("method");

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (!data.error){
            $("#target_area").html(data.content);
        }
        else{
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 
}

//目標を完了にさせる
function target_done(form_elem){

    let data        = new FormData( $(form_elem).get(0) );
    let url         = $(form_elem).prop("action");
    let method      = "PATCH";

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
            
            $("#target_area").html(data.content);

        }
        else{
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 
}


//TODO:音量のセット
function volume_input(elem){
    //Cookieをセットする。 SameSiteをセットしておく。
    document.cookie = "volume=" + String($(elem).val()) + ";SameSite=strict";
    console.log(document.cookie)
}
