window.addEventListener("load" , function (){

    draw_daily_graph();
    draw_month_category_graph();
    

    draw_year_total_graph();


});


function draw_daily_graph(){

    let day_elems    = $(".daily_graph_day")
    let total_elems  = $(".daily_graph_total")

    let days    = [];
    let totals  = [];

    for (let day_elem of day_elems){
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
                label: "運動時間(秒)",
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

    let category_elems  = $(".month_category")
    let time_elems      = $(".month_time")

    let categories  = [];
    let times       = [];

    for (let category_elem of category_elems){
        categories.push(category_elem.innerText);
    }
    for (let time_elem of time_elems){
        times.push(time_elem.innerText);
    }

    const ctx = document.getElementById("month_category_graph").getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categories,
            datasets: [{
                label: "運動時間(秒)",
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




}
