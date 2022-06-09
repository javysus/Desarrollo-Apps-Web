var inicial = true;
var current_page = 1;
var max_page;
function cambiarPagina(){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(xhr.readyState===4 && xhr.status===200){
            let response = xhr.responseText;
            // 
            // 
            response = JSON.parse(response);
            max_page = response.pop();
            filas_tabla = ""
            
            if(current_page == max_page){
                $('#next-class').addClass('disabled')
            } else if($('#next-class').hasClass('disabled')){
                $('#next-class').removeClass('disabled')
            }
            for(i in response){
                var cantidad_fotos = response[i][10]
                var comuna = response[i][1]
                var sector = response[i][2]
                var nombre = response[i][3]
                var fecha_inicio = response[i][6]
                var fecha_termino = response[i][7]
                //var descripcion = response[i][8]
                var tema = response[i][9]
                var fila = `<tr class="position-relative">
                '<th>${fecha_inicio}</th> <th>${fecha_termino}</th> <th>${comuna}</th> <th>${sector}</th> <th>${tema}</th> 
                <th>${nombre}</th> <th>${cantidad_fotos}</th> <th><a href="#" id="act-${i}-pag-${current_page}" class="btn btn-primary btn-sm stretched-link">Ver más</a></th>'
                </tr>
                `

                filas_tabla += fila
            }

            $('#actividades-pagina').html(filas_tabla)
            verActividad();
        }
    }
    $(".page-link").click(function () {
        inicial = false;
        var pagina = $(this).attr("id");
        var numero_pagina;
        if(pagina=="next"){
            numero_pagina = current_page + 1;
        } else if(pagina=="prev"){
            numero_pagina = current_page - 1;
        } else{
            numero_pagina = parseInt(pagina);
        }
        //Cambiar pagina activa
        $('#activar-'+current_page).removeClass('active');
        $('#activar-'+numero_pagina).addClass('active');
        current_page = numero_pagina;

        console.log(current_page)
        if (current_page==1){
            $('#prev-class').addClass('disabled')
        } else{
            $('#prev-class').removeClass('disabled')
        }  /*else if(current_page == ){

        }*/
        //Enviar solicitud
        xhr.open("GET", '../cgi-bin/pagination.py?pagina='+current_page);
        xhr.send();
    });
}

function verActividad(){
    /*var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(xhr.readyState===4 && xhr.status===200){
            document.open();
            document.write(xhr.responseText);
        }
    }*/
    $(".stretched-link").click(function (){
        console.log("Click!");
        var id = $(this).attr("id");
        id = id.split('-');
        var act = id[1];
        var pag = id[3];

        var params = `act=${act}&pag=${pag}`;
        

        //xhr.open('POST', '../cgi-bin/actividad.py', true);
        //xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        //xhr.send(params);
        window.location = "actividad.py?"+params;
    })
}

$(document).ready(function(){
    cambiarPagina();
    if(inicial){
        verActividad();
    }
    
})