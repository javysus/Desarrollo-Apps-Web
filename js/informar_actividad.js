
function agregarRegionesyComunas(){
    $("#region").change(function(){
        var region_value = $(this).val();
        html_comuna = "<option value= '' selected>Seleccione una comuna</option>";
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function(){
            if(xhr.readyState===4 && xhr.status===200){
                let response = xhr.responseText;
                // 
                // 
                response = JSON.parse(response);
                for(i in response){
                    $("#comuna").append(`<option value=${response[i][0]}>${response[i][1]}</option>`);
                }
            }
        }

        if(region_value > 0){
            $("#comuna").html(html_comuna);
            xhr.open("GET", '../cgi-bin/comunas.py?id_region='+region_value);
            xhr.send();
        } else{
            $("#comuna").html(html_comuna);
        }

        
    })
}

function fechayHora(){
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    var hh = String(today.getHours()).padStart(2, '0');
    var min = String(today.getMinutes()).padStart(2, '0');

    var fecha_inicio = document.getElementsByName('dia-hora-inicio');

    fecha_inicio[0].placeholder = yyyy+"-"+mm+"-"+dd+" "+hh+":"+min;
    var end = new Date(today);
    end.setHours(end.getHours() + 3);
    var fecha_termino = document.getElementsByName('dia-hora-termino');

    var dd_t = String(end.getDate()).padStart(2, '0');
    var mm_t = String(end.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy_t = end.getFullYear();
    var hh_t = String(end.getHours()).padStart(2, '0');
    var min_t = String(end.getMinutes()).padStart(2, '0');
    fecha_termino[0].placeholder = yyyy_t+"-"+mm_t+"-"+dd_t+" "+hh_t+":"+min_t;

    //Validacion y luego modificar placeholder de fecha termino
    $("#dia-hora-inicio").one("click", function () {
        fecha_inicio[0].value = yyyy+"-"+mm+"-"+dd+" "+hh+":"+min;
        fecha_termino[0].value = yyyy_t+"-"+mm_t+"-"+dd_t+" "+hh_t+":"+min_t;
    });

    $('#dia-hora-inicio').change(function(){
        var fecha_inicio_ingresada = $(this).val();
        console.log(fecha_inicio_ingresada);

        if(validarFecha(fecha_inicio_ingresada)){
            document.getElementsByName('dia-hora-inicio')[0].style.borderColor="";
            var fecha_ingresada = new Date(fecha_inicio_ingresada);
            console.log(fecha_ingresada);

            end = new Date(fecha_ingresada);
            end.setHours(end.getHours() + 3);
            fecha_termino = document.getElementsByName('dia-hora-termino');

            dd_t = String(end.getDate()).padStart(2, '0');
            mm_t = String(end.getMonth() + 1).padStart(2, '0'); //January is 0!
            yyyy_t = end.getFullYear();
            hh_t = String(end.getHours()).padStart(2, '0');
            min_t = String(end.getMinutes()).padStart(2, '0');
            fecha_termino[0].placeholder = yyyy_t+"-"+mm_t+"-"+dd_t+" "+hh_t+":"+min_t;
            fecha_termino[0].value = yyyy_t+"-"+mm_t+"-"+dd_t+" "+hh_t+":"+min_t;
        }else{
            document.getElementsByName('dia-hora-inicio')[0].style.borderColor="red";
        }

    })

    $('#dia-hora-termino').change(function(){
        if(!validarFecha(fecha_inicio_ingresada)){
            document.getElementById("#dia-hora-termino").style.borderColor = "red";
        } else{
            document.getElementById("#dia-hora-termino").style.borderColor = "";
        }
    })
}
function inicializarContactos(){
    const all_redes = ['whatsapp', 'telegram', 'twitter', 'instagram', 'facebook', 'tiktok', 'otra'];

    for (let red in all_redes){
        if(document.getElementById(all_redes[red]).checked){
            document.getElementById(all_redes[red]+"-link").disabled = false;
        }
    }
}
function contactar_por(){
    var redes_check = 0;
    const all_redes = ['whatsapp', 'telegram', 'twitter', 'instagram', 'facebook', 'tiktok', 'otra'];
    $(".form-check-input").change(function() {
        var id_check = $(this).attr("id");
        var disabled = document.getElementById(id_check+"-link").disabled;

        if(disabled){
            redes_check++;
            if(redes_check < 5){
                document.getElementById(id_check+"-link").disabled = false;
            } else if (redes_check==5){
                document.getElementById(id_check+"-link").disabled = false;
                $("#maximo-redes").append('<div class="alert alert-info" role="alert">Máximo de 5 redes alcanzado</div>');

                for (let red in all_redes){
                    if(!document.getElementById(all_redes[red]).checked){
                        document.getElementById(all_redes[red]).disabled = true;
                    }
                }
            }
            
        } else{
            document.getElementById(id_check+"-link").disabled = true;
            document.getElementById(id_check+"-link").style.borderColor = "";
            if(redes_check==5){
                $("#maximo-redes").html("");
                for (let red in all_redes){
                    if(!document.getElementById(all_redes[red]).checked){
                        document.getElementById(all_redes[red]).disabled = false;
                    }
                }
            }
            redes_check--;
            
        }
      });
}

function agregarFotos(){
    var fotos = 1;
    $("#agregar-archivo").click(function (){
        fotos++;
        var html;
        if(fotos <= 4){
            $("#archivos-fotos").append("<div class='col-auto align-self-center'><label for='foto-actividad-"+fotos+"' class='form-label'>Foto "+fotos+ "</label></div><div class='col-6'><input class='form-control' type='file' id='foto-actividad-"+fotos+"' name='foto-actividad'></div><div class='w-100'></div>")
        }

        else if(fotos == 5){
            $("#archivos-fotos").append("<div class='col-auto align-self-center'><label for='foto-actividad-"+fotos+"' class='form-label'>Foto "+fotos+ "</label></div><div class='col-6'><input class='form-control' type='file' id='foto-actividad-"+fotos+"' name='foto-actividad'></div>")
        }
        else if (fotos==6){
            $("#maximo-fotos").append('<div class="alert alert-info" role="alert">Máximo de 5 fotos alcanzado</div>')
        }
    })
}

function temaOtro(){
    $("#tema").change(function (){
        var tema = $(this).val();
        console.log(tema)
        if(tema == 0){
            $("#otroTema").html('<label for="otro" class="col-sm-2 col-form-label">Descripción de otro tema </label><div class="col-sm-10"><input type="text" name="otro" id="otro" class="form-control"></div>');
            validarotroTemaReal();
        } else{
            $("#otroTema").html("");
        }
    })
}
/*Validacion*/
function validarFormulario(){
    let region = document.getElementById('region').value;
    let comuna = document.getElementById('comuna').value;
    let sector = document.getElementById('sector').value;
    let nombre = document.getElementById('nombre').value;
    let email = document.getElementById('email').value;
    let celular = document.getElementById('celular').value;
    let dia_hora_inicio = document.getElementById('dia-hora-inicio').value;
    let dia_hora_termino = document.getElementById('dia-hora-termino').value;
    let tema = document.getElementById('tema').value;
    
    const all_redes = ['whatsapp', 'telegram', 'twitter', 'instagram', 'facebook', 'tiktok', 'other'];
    var errores = false;

    if(!validarRegion(region)){
        $("#error-region").html('<div class="alert alert-danger" role="alert">Seleccione una región</div>');
        errores = true;
    } else{
        $("#error-region").html('');
    }

    if (!validarComuna(comuna)){
        $("#error-comuna").html('<div class="alert alert-danger" role="alert">Seleccione una comuna</div>');
        errores = true;
    }else{
        $("#error-comuna").html('');
    }


    if (!validarSector(sector)){
        $("#error-sector").html('<div class="alert alert-danger" role="alert">Ingrese un sector valido de largo máximo 100 caracteres</div>');
        errores = true;
    }else{
        $("#error-sector").html('');
    }

    if (!validarNombre(nombre)){
        $("#error-nombre").html('<div class="alert alert-danger" role="alert">Ingrese un nombre válido de largo máximo 200 caracteres</div>');
        errores = true;
    }else{
        $("#error-nombre").html('');
    }

    if (!validarMail(email)){
        $("#error-email").html('<div class="alert alert-danger" role="alert">Ingrese un correo válido</div>');
        errores = true;
    }else{
        $("#error-email").html('');
    }

    if (!validarCelular(celular)){
        $("#error-celular").html('<div class="alert alert-danger" role="alert">Ingrese un número de celular válido en formato +569</div>');
        errores = true;
    }else{
        $("#error-celular").html('');
    }

    if(!validarFecha(dia_hora_inicio)){
        $("#error-dia-hora-inicio").html('<div class="alert alert-danger" role="alert">Ingrese una fecha válida</div>');
        errores = true;
    }else{
        $("#error-dia-hora-inicio").html('');
    }

    if(dia_hora_termino.length != 0 && !validarFecha(dia_hora_termino)){
        $("#error-dia-hora-termino").html('<div class="alert alert-danger" role="alert">Ingrese una fecha válida</div>');
        errores = true;
    }else{
        $("#error-dia-hora-termino").html('');
    }

    existe_tema = false;
    if (!validarTema(tema)){
        $("#error-tema").html('<div class="alert alert-danger" role="alert">Seleccione un tema</div>');
        errores = true;
    }else{
        $("#error-tema").html('');
        existe_tema = true;
    }

    if (tema == 10 && !validarOtroTema(document.getElementById('otro').value)){
        $("#error-tema").html('<div class="alert alert-danger" role="alert">Ingrese una descripción valida de mínimo 3 y máximo 15 caracteres</div>');
        errores = true;
        quitar_error_tema = false;
    } else if (existe_tema){
        $("#error-tema").html('');
    }

    if (!validarFotos()){
        $("#maximo-fotos").html('<div class="alert alert-danger" role="alert">Ingrese mínimo 1 foto y máximo 5 fotos</div>');
        errores = true;
    }else{
        $("#maximo-fotos").html('');
    }

    var agregar_error = true;
    for (let pos in all_redes){
        let input = document.getElementById(all_redes[pos]+'-link').value;
        var checked = document.getElementById(all_redes[pos]).checked;
        if (!validarRedInput(input) && agregar_error && checked){
            $("#maximo-redes").html('<div class="alert alert-danger" role="alert">Ingrese una URL o ID válido</div>');
            agregar_error = false;
            errores = true;
        }
    }
    if (agregar_error){
        $("#maximo-redes").html('');
        
    }

    if (!errores){
        return true;
    }
    else{
        $('#validacion-form').modal('show');
        return false;
    }
    


}

/*Fecha:
- Formato yyy-MM-dd hh:mm*/
function validarFecha(fecha){
    let regex_fecha = /^([0-9]{4})-([0-1][0-9])-([0-3][0-9])\s([0-1][0-9]|[2][0-3]):([0-5][0-9])$/;

    if (!regex_fecha.test(fecha) | fecha.length > 20){
        return false;
    }

    return true;
}

/*Region:
- Selección obligatoria
*/
function validarRegion(region){
    if (region == ''){
        return false;
    }
    return true;
}

/*Comuna:
- Selección obligatoria
*/
function validarComuna(comuna){
    if (comuna == ''){
        return false;
    }
    return true;
}

/*Sector:
- Largo máximo de 100
*/
function validarSector(sector){
    if (sector.length > 100){
        return false;
    }
    return true;
}

function validarSectorReal(){
    $("#sector").change(function(){
        sector = $(this).val();

        if (!validarSector(sector)){
            document.getElementById("sector").style.borderColor = "red";
        }
        else{
            document.getElementById("sector").style.borderColor = "";
        }
    })
}

/*Nombre:
- Formato de nombre
- Largo máximo de 200
*/
function validarNombre(nombre){
    let regex_nombre = /^[a-zA-Z ]*$/;

    if (!regex_nombre.test(nombre) | nombre.length == 0 | nombre.length > 200){
        return false;
    }

    return true;
}

function validarNombreReal(){
    $("#nombre").change(function(){
        nombre = $(this).val();
        if (!validarNombre(nombre)){
            document.getElementById("nombre").style.borderColor = "red";
        }
        else{
            document.getElementById("nombre").style.borderColor = "";
        }
    })

}

/*Email:
- Formato de dirección de email
*/
function validarMail(email){
    let regex_email = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/;

    if (!regex_email.test(email)){
        return false;
    }

    return true;
}

function validarMailReal(){
    $("#email").change(function(){
        email = $(this).val();
        
        if (!validarMail(email)){
            document.getElementById("email").style.borderColor = "red";
        }
        else{
            document.getElementById("email").style.borderColor = "";
        }
    })
}
/*Celular:
- Formato de número de teléfono de móvil ^\+[1-9]\d{1,14}$
*/

function validarCelular(cel){
    let regex_cel = /^\+[1-9]\d{1,14}$/;

    if (!regex_cel.test(cel) && cel.length != 0){
        return false;
    }

    return true;
}

function validarCelReal(){
    $("#celular").change(function(){
        cel = $(this).val();
        
        if (!validarCelular(cel)){
            document.getElementById("celular").style.borderColor = "red";
        }
        else{
            document.getElementById("celular").style.borderColor = "";
        }
    })
}
/*Contactar por:
- Máximo 5 redes (Hecho en contactar_por)
- Input de información debe permitir mínimo 4 caracteres y maximo 50
*/

function validarRedInput(red_link_value){
    if(red_link_value.length < 4 | red_link_value.length > 50){
        return false;
    }
    return true;
}
function validarRedesInput(){
    contactar_por();
    $(".redes-input").change(function(){
        red_link_value = $(this).val();
        red = $(this).attr("id");
        if(!validarRedInput(red_link_value)){
            document.getElementById(red).style.borderColor = "red";
        } else{
            document.getElementById(red).style.borderColor = "";
        }
    })
}

/*Tema:
- Selección de al menos una opción
- Otro: Input debe permitir como mínimo 3 carácteres y máximo 15
*/
function validarTema(tema){
    if (tema==''){
        return false;
    }

    return true;
}

function validarOtroTema(otro){
    if(otro.length < 3 | otro.length > 15){
        return false;
    }

    return true;
}
function validarotroTemaReal(){
    $("#otro").change(function(){
        otro = $(this).val();
        if(!validarOtroTema(otro)){
            document.getElementById("otro").style.borderColor = "red";
        } else{
            document.getElementById("otro").style.borderColor = "";
        }
    })
}

/*Foto:
- Subida obligatoria
- Mínimo 1 foto y máximo 5 fotos
*/
function validarFotos(){
    var fotos = 0;
    const id_fotos = ["", "2", "3", "4", "5"];

    for (let pos in id_fotos){
        var foto = document.getElementById("foto-actividad"+id_fotos[pos]);

        if (foto != null && foto.value != ""){
            fotos++;
        }
    }

    if(fotos < 1 | fotos > 5){
        return false;
    }

    return true;
}
/*Validacion en tiempo real*/
function validacionTiempoReal(){
    fechayHora();
    
    agregarFotos();

    temaOtro();

    validarRedesInput();

    validarSectorReal();

    validarNombreReal();

    validarCelReal();

    validarMailReal();

    //validarotroTemaReal();
}
$(document).ready(function(){
    agregarRegionesyComunas();
    validacionTiempoReal();
    

});
