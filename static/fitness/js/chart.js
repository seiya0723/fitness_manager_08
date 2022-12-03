window.addEventListener("load" , function (){

    draw_daily_graph();
    draw_month_category_graph();
    draw_year_total_graph();

});
function draw_daily_graph(){

    let day_elems    = $(".daily_graph_day");
    let total_elems  = $(".daily_graph_total");

    //chart.jsに入れるラベルとデータ
    let days    = [];
    let totals  = [];

    //day_elemsはjQueryのオブジェクトだが、取り出すとJavaScriptのオブジェクトになる
    for (let day_elem of day_elems){
        //innerText属性で参照する
        days.push(day_elem.innerText);
    }
    for (let total_elem of total_elems){
        totals.push(total_elem.innerText);
    }

    const ctx = document.getElementById('daily_graph').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: days,
            datasets: [{
                label: "運動時間(分)",
                data: totals,
                backgroundColor: "orange",
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

}

//今月のカテゴリごとのグラフ(円グラフ)
function draw_month_category_graph(){

    let category_elems  = $(".month_category");
    let time_elems      = $(".month_time");

    //TODO:オブジェクトの配列を作る
    let data_label      = [];
    for (let i=0;i<category_elems.length;i++){
        data_label.push( { category : category_elems.eq(i).text(), time : Number(time_elems.eq(i).text()) } );
    }

    //並び替える
    data_label.sort( (a, b) => { return a.time - b.time; });

    //大きいほうが先
    //data_label.sort( (a, b) => { return b.time - a.time; });

    console.log(data_label);

    //分離させる
    let categories  = [];
    let times       = [];
    for (let data of data_label){
        categories.push(data.category);
        times.push(data.time);
    }

    /*
    let categories  = []; // A,B,C
    let times       = []; // 10,5,9


    for (let category_elem of category_elems){
        categories.push(category_elem.innerText);
    }
    for (let time_elem of time_elems){
        times.push(time_elem.innerText);
    }
    */


    const ctx = document.getElementById("month_category_graph").getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categories,
            datasets: [{
                label: "運動時間(分)",
                data: times,
                backgroundColor: "orange",
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

}


//同じ要領で年間のグラフを生成する。
function draw_year_total_graph(){

    let month_elems = $(".year_total_month");
    let total_elems = $(".year_total_time");

    //chart.jsに入れるラベルとデータ
    let months  = [];
    let totals  = [];

    //month_elemsはjQueryのオブジェクトだが、取り出すとJavaScriptのオブジェクトになる
    for (let month_elem of month_elems){
        //innerText属性で参照する
        months.push(month_elem.innerText);
    }
    for (let total_elem of total_elems){
        totals.push(total_elem.innerText);
    }

    const ctx = document.getElementById('year_graph').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: "運動時間(分)",
                data: totals,
                backgroundColor: "orange",
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

}
