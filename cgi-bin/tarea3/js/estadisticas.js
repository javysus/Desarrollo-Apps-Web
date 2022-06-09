function grafico_1(datos){
    const ctx = document.getElementById('actividades-dia-graph').getContext('2d');

    var dias = datos[0]
    var acts = datos[1]
    var actividades_dia = {
        labels: dias,
        datasets: [{
          label: "Cantidad de actividades",
          data: acts,
          borderColor: '#3399FF',
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
        },
        plugins: {
            title: {
            display: true,
            text: 'Cantidad de actividades en los últimos 10 días'
        }
        },
      };

    var lineChart = new Chart(ctx, {
        type: 'line',
        data: actividades_dia,
        options: chartOptions
    });
}

function grafico_2(datos){
    var ctx = document.getElementById("actividades-tipo-graph");
    var temas = datos[0];
    var acts = datos[1];
    //Chart.defaults.global.defaultFontFamily = "Lato";
    //Chart.defaults.global.defaultFontSize = 18;

    var tipoActividades = {
        labels: temas,
        datasets: [
            {
                data: acts,
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
        maintainAspectRatio: false,
        plugins: {
            title: {
            display: true,
            text: 'Total de actividades por tipo'
        }
        }
    }
    });
}

function grafico_3(datos){
    const ctx = document.getElementById('actividades-mes-graph').getContext('2d');
    var meses = datos[0];
    var mañanas = datos[1];
    var mediodias = datos[2];
    var tardes = datos[3];

    var mananaData = {
        label: 'Actividades en la mañana',
        data: mañanas,
        backgroundColor: '#E374D2', 
    };

    var mediodiaData = {
        label: 'Actividades en el mediodía',
        data: mediodias,
        backgroundColor: '#B538A2',

    };

    var tardeData = {
        label: 'Actividades en la tarde',
        data: tardes,
        backgroundColor: '#4F0644'
    };

    var graphData = {
        labels: meses,
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
            plugins: {
                title: {
                display: true,
                text: 'Cantidad de actividades en la mañana, mediodía y tarde según mes'
                }
            }
            
        }
    });
}

function prepararGraficos(){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(xhr.readyState===4 && xhr.status===200){
            let response = xhr.responseText;
            response = JSON.parse(response);

            datos_grafuno = response[0];
            datos_grafdos = response[1];
            datos_graftres = response[2];

            grafico_1(datos_grafuno);
            grafico_2(datos_grafdos);
            grafico_3(datos_graftres);
        }
    }
    
    //Enviar solicitud
    xhr.open("GET", '/cgi-bin/graficos.py');
    xhr.send();
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
    prepararGraficos();
    //grafico_1();
    //grafico_2();
    //grafico_3();
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