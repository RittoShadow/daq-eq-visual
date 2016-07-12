
// Validacion para boton de obtener varios archivos
$(function(){
  $('#multifile-form').submit(function(){
    var checked_checkboxes = $('[name="selection-checkbox"]:checked');
    if(checked_checkboxes.length > 0) {
      var required_files = [];
      checked_checkboxes.each(function(){
        required_files.push($(this).attr("value"));
      });
      $('#files_array').attr('value', JSON.stringify(required_files));
      return true;
    }

    return false;
  });
});

// Cambiar colores de tr's de tabla
$(function(){
  $('.localfile-tr').hover(function(){
    $(this).css("background-color", "#ffcccc");
  }, function(){
    $(this).css("background-color", "white");
  });
});
