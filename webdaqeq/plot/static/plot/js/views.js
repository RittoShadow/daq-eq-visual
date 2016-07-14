function sendSignal(value){
  // Desactivar botones daqeq
  $('#daqeq-start-btn').attr('disabled', true);
  $('#daqeq-stop-btn').attr('disabled', true);
  $('#daqeq-trigger-btn').attr('disabled', true);

  $.ajax({
    url: '/plot/signal/',
    type: "POST",
    async: false,
    data: {'command' : value, 'this_url' : $('#views-data').attr('data-url')},
    success: function (response) {
      switch (value) {
        case 'start':
        case 'trigger':
          $('#daqeq-stop-btn').attr('disabled', false);
          $('#daqeq-trigger-btn').attr('disabled', false);
          break;
        case 'stop':
          $('#daqeq-start-btn').attr('disabled', false);
          break;
      }
    },
    error: function (response) {
      switch (value) {
        case 'start':
          $('#daqeq-start-btn').attr('disabled', false);
          break;
        case 'stop':
        case 'trigger':
          $('#daqeq-stop-btn').attr('disabled', false);
          $('#daqeq-trigger-btn').attr('disabled', false);
          break;
      }
    }
  });
  }

// On Ready
$(function(){
  // Ver como se muestran botones arriba al cargar primera vez
  if($('#views-data').attr('data-running') == 'True') {
    $('#daqeq-start-btn').attr('disabled', true);
  } else {
    $('#daqeq-stop-btn').attr('disabled', true);
    $('#daqeq-trigger-btn').prop('disabled', true);
  }
});
