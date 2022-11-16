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
    flatpickr("[name='exe_dt']",config_dt);

    let config_date = { 
        locale: "ja",
        dateFormat: "Y-m-d",
        defaultDate: date,
    }
    flatpickr("[name='date']",config_date);

    $(document).on("click", "#fitness_memory_submit", function() { fitness_memory_submit(this) });


    //TODO:カレンダーの日付をクリックした時、日ごとのページへジャンプする
    $(document).on("click",".calendar_day_area", function(){
        //日付を抜き取る
        let day = $(this).children(".calendar_day").text();

        //データがない場合はアーリーリターン
        if (!$("#day_"+day).length){ return false; }

        //日ごとにチェックを入れる
        $("#tab_radio_2").prop("checked",true);

        //スクロールする
        //参照元: https://qiita.com/yamaguchi_takashi/items/edce735e825631993a74
        $("html,body").animate({scrollTop:$("#day_"+day).offset().top}, 100);
    });



    $(document).on("click", ".target_done", function(){ target_done(this); });


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
            console.log("投稿完了")
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
        }
        else{
            console.log("ERROR");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 


}
