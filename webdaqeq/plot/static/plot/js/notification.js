$(function () {

  if (!$('#id_sendRecord')[0].checked) {
    $('#id_username')[0].disabled = true;
    $('#id_password')[0].disabled = true;
    $('#id_structure')[0].disabled = true;
    $('#id_email')[0].disabled = true;
    $('#id_phoneNumber')[0].disabled = true;
    $('#id_sendSMS')[0].disabled = true;
    $('#id_compressRecord')[0].disabled = true;
    $('#id_authenticationURL')[0].disabled = true;
    $('#id_recordURL')[0].disabled = true;
  }

  if (!$('#id_sendStructHealth')[0].checked) {
    $('#id_structHealthURL')[0].disabled = true;
    $('#id_sendFrequency')[0].disabled = true;
    $('#id_verificationFrequency')[0].disabled = true;
  }

  $('#id_sendRecord').change(function() {
    if(this.checked) {
        //Do stuff
      $('#id_username')[0].disabled = false;
      $('#id_password')[0].disabled = false;
      $('#id_structure')[0].disabled = false;
      $('#id_email')[0].disabled = false;
      $('#id_phoneNumber')[0].disabled = false;
      $('#id_sendSMS')[0].disabled = false;
      $('#id_compressRecord')[0].disabled = false;
      $('#id_authenticationURL')[0].disabled = false;
      $('#id_recordURL')[0].disabled = false;
    } else {
      $('#id_username')[0].disabled = true;
      $('#id_password')[0].disabled = true;
      $('#id_structure')[0].disabled = true;
      $('#id_email')[0].disabled = true;
      $('#id_phoneNumber')[0].disabled = true;
      $('#id_sendSMS')[0].disabled = true;
      $('#id_compressRecord')[0].disabled = true;
      $('#id_authenticationURL')[0].disabled = true;
      $('#id_recordURL')[0].disabled = true;
    }
  });

  $('#id_sendStructHealth').change(function () {
    if(this.checked) {
      $('#id_structHealthURL')[0].disabled = false;
      $('#id_sendFrequency')[0].disabled = false;
      $('#id_verificationFrequency')[0].disabled = false;
    } else {
      $('#id_structHealthURL')[0].disabled = true;
      $('#id_sendFrequency')[0].disabled = true;
      $('#id_verificationFrequency')[0].disabled = true;
    }
  });

  $('#notification_form').submit(function(event) {
    // Obtener icon antiguo y reemplazar por reloj
    disable_submit_span();
    // event.preventDefault();
    // alert('hola');

    //notificaciones

    // Devolver a icon anterior si no funciona correctamente (reemplazar cond en if por la de return false)
    if (false) {
      enable_submit_span();
      return false
    }

    return true;
  });

});
