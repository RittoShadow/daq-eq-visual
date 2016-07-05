function disable_submit_span() {
  $('.submit-span').attr('old-class', $('.submit-span').attr('class'));
  $('.submit-span').attr('class', "glyphicon glyphicon-hourglass submit-span");
  $(".submit-span").parent().prop("disabled", true);
}

function enable_submit_span() {
  $('.submit-span').attr('class', $('.submit-span').attr('old-class'));
  $(".submit-span").parent().prop("disabled", false);
}

$(function () {

  $('#config_form').submit(function(event) {
    // Obtener icon antiguo y reemplazar por reloj
    disable_submit_span();
    // event.preventDefault();
    // alert('hola');

    //notificaciones



    // config

    // Devolver a icon anterior si no funciona correctamente (reemplazar cond en if por la de return false)
    if (false) {
      enable_submit_span();
      return false
    }

    // $('#config_form').submit();
    return true;
  });

});
