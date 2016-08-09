// Main javascript
// Globales --------------------------------------------------------------------
var message_duration = 5000; // <-- time in milliseconds, 1000 =  1 sec

// OnReady ---------------------------------------------------------------------
$(function(){
  
  // Desaparecer mensajes flash pasados "message_duration" segundos
  setTimeout(function() {
    $('.alert').fadeOut('slow');
  }, message_duration);

});


// Funciones -------------------------------------------------------------------

// Deshabilitar button perteneciente a un span, y cambiar icono
function disable_submit_span() {
  $('.submit-span').attr('old-class', $('.submit-span').attr('class'));
  $('.submit-span').attr('class', "glyphicon glyphicon-hourglass submit-span");
  $(".submit-span").parent().prop("disabled", true);
}

// Habilitar button perteneciente a un span, y recuperar icono
function enable_submit_span() {
  $('.submit-span').attr('class', $('.submit-span').attr('old-class'));
  $(".submit-span").parent().prop("disabled", false);
}
