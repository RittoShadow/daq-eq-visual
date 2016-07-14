// Main javascript

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
