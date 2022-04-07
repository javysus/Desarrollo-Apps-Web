function grafico_1(){
    const ctx = document.getElementById('actividades-dia-graph').getContext('2d');
    var actividades_dia = {
        labels: ["25/03/2022","26/03/2022", "27/03/2022","28/03/2022","29/03/2022", "30/03/2022", "31/03/2022", "01/04/2022", "02/04/2022", "03/04/2022"],
        datasets: [{
          label: "Actividades",
          data: [10, 8, 15, 30, 53, 82, 74, 50, 34, 11, 6],
          borderColor: 'orange',
        backgroundColor: 'transparent',
        }]
    };

    var chartOptions = {
        responsive:true,
        maintainAspectRatio: false,
        legend: {
          display: true,
          position: 'top',
          labels: {
            boxWidth: 1,
            fontColor: 'black'
          }
        }
      };

    var lineChart = new Chart(ctx, {
        type: 'line',
        data: actividades_dia,
        options: chartOptions
    });
}

function grafico_2(){
    var ctx = document.getElementById("actividades-tipo-graph");

    //Chart.defaults.global.defaultFontFamily = "Lato";
    //Chart.defaults.global.defaultFontSize = 18;

    var tipoActividades = {
        labels: [
            "Música",
            "Deporte",
            "Ciencias",
            "Religión",
            "Política",
            "Tecnología",
            "Juegos",
            "Baile",
            "Comida",
            "Otro"
        ],
        datasets: [
            {
                data: [105, 98, 70, 68, 59, 94, 86, 63, 43, 32],
                backgroundColor: [
                    "#FF6384",
                    "#63FF84",
                    "#D7FFAB",
                    "#8463FF",
                    "#6384FF",
                    "Purple",
                    "#F0D2D1",
                    "#42CAFD",
                    "#F6EFA6",
                    "#D89D6A"
                ]
            }]
    };

    var pieChart = new Chart(ctx, {
    type: 'pie',
    data: tipoActividades,
    options: {responsive:true,
        maintainAspectRatio: false}
    });
}

function grafico_3(){
    const ctx = document.getElementById('actividades-mes-graph').getContext('2d');
    var mananaData = {
        label: 'Actividades en la mañana',
        data: [1,1,1,1,1,1,1,1,1,1,1,1],
        backgroundColor: '#E374D2', 
    };

    var mediodiaData = {
        label: 'Actividades en el mediodía',
        data: [2,2,2,2,2,2,2,2,2,2,2,2],
        backgroundColor: '#B538A2',

    };

    var tardeData = {
        label: 'Actividades en la tarde',
        data: [3,3,3,3,3,3,3,3,3,3,3,3],
        backgroundColor: '#4F0644'
    };

    var graphData = {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        datasets: [mananaData, mediodiaData, tardeData]
      };
    
    /*var chartOptions = {
        scales: {
            xAxes: [{
            barPercentage: 1,
            categoryPercentage: 0.6
            }],
            yAxes: [{
            id: "y-axis-manana"
            }, {
            id: "y-axis-mediodia"
            }, {
            id: "y-axis-tarde"
            }]
        }
        };*/
    var barChart = new Chart(ctx, {
        type: 'bar',
        data: graphData,
        options: {
            responsive:true,
            maintainAspectRatio: false,
            barValueSpacing: 20,
            
        }
    });
}

function modificarIcon(){
    $(".button-icon").click(function(){
        var expansion = $(this).attr("aria-expanded");
        if(expansion=="true"){
            $(this).html('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-up" viewBox="0 0 16 16"><path d="M3.204 11h9.592L8 5.519 3.204 11zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659z"/></svg>');
        } else{
            $(this).html('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down" viewBox="0 0 16 16"><path d="M3.204 5h9.592L8 10.481 3.204 5zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659z"/></svg>');
        }

    })
}
$(document).ready(function(){
    modificarIcon();
    grafico_1();
    grafico_2();
    grafico_3();
    /*
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
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
    });*/
});