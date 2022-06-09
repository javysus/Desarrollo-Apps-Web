function agregarPopUp(marker, response){
    var html = `<table class="table table-hover align-middle">
    <thead>
        <tr>
            
            <th>Inicio</th>
            <th>Tema</th>
            <th>Sector</th>
            <th>Fotos</th>
            <th></th>
        </tr>
    </thead>

    <tbody>`;

    
    for (i in response){
        var fecha_inicio = response[i][1];
        var tema = response[i][2];
        var sector = response[i][3];
        var fila = `<tr class="position-relative">
                <th>${fecha_inicio}</th> <th>${tema}</th> <th>${sector}</th>
                `
        var fotos = response[i][4];
        for(foto in fotos){
            foto_hash = fotos[foto][1];
            foto_nombre = fotos[foto][2];
            fila = fila + `<th> <img src="../../../media/${foto_hash}" class="rounded img-ultramini" alt="${foto_nombre}"></th>`;

        }

        fila = fila + `<th><a href="../cgi-bin/actividad.py?metodo=index&f=${foto_hash}" id="${foto_hash}" class="btn btn-primary btn-sm stretched-link">Ver más</a></th></tr>`;
        html = html + fila;
    }

    html = html + '</tbody></table>';
    marker.bindPopup(html, {maxWidth: "auto"});

    
}

function obtenerComunas(){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(xhr.readyState===4 && xhr.status===200){
            let response = xhr.responseText;
            response = JSON.parse(response);

            

            lat_inicial = response[0][2];
            long_inicial = response[0][3];
            titulo_inicial = response[0][1] + ' fotos';
            var map = L.map('map').setView([lat_inicial, long_inicial],5);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
            }).addTo(map);

            var marker = L.marker([lat_inicial, long_inicial],{title: titulo_inicial}).addTo(map);
            agregarPopUp(marker, response[0][5]);
            response.shift();
           
            for(i in response){
                lat = response[i][2];
                long = response[i][3];
                titulo = response[i][1] + ' fotos';
                actividades = response[i][5]
                var marker = L.marker([lat, long],{title: titulo}).addTo(map);
                //agregarPopUp(marker, response[0][5]);

                var html = `<table class="table table-hover align-middle">
                <thead>
                    <tr>
                        
                        <th>Inicio</th>
                        <th>Tema</th>
                        <th>Sector</th>
                        <th>Fotos</th>
                        <th></th>
                    </tr>
                </thead>

                <tbody>`;

                
                for (i in actividades){
                    var fecha_inicio = actividades[i][1];
                    var tema = actividades[i][2];
                    var sector = actividades[i][3];
                    var fila = `<tr class="position-relative">
                            <th>${fecha_inicio}</th> <th>${tema}</th> <th>${sector}</th>
                            `
                    var fotos = actividades[i][4];
                    for(foto in fotos){
                        foto_hash = fotos[foto][1];
                        foto_nombre = fotos[foto][2];
                        fila = fila + `<th> <img src="../../../media/${foto_hash}" class="rounded img-ultramini" alt="${foto_nombre}"></th>`;

                    }

                    fila = fila + `<th><a href="../cgi-bin/actividad.py?metodo=index&f=${foto_hash}" id="${foto_hash}" class="btn btn-primary btn-sm stretched-link">Ver más</a></th></tr>`;
                    html = html + fila;
                }

                html = html + '</tbody></table>';
                marker.bindPopup(html, {maxWidth: "auto", maxHeight:300});
            }

        }
    }

    //Enviar solicitud
    xhr.open("GET", '../cgi-bin/mapa.py');
    xhr.send();
}

$(document).ready(function(){
    /*var map = L.map('map').
    setView([41.66, -4.72],
    15);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
    maxZoom: 18
    }).addTo(map);*/
    
    obtenerComunas();
    //verActividad();
    
})