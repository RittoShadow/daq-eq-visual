var sensorNums = [];
function addSerial(){
  var serialNum = $("[name='new_sensor']")[0].value;
  $.ajax({
    url: '/plot/sensors/',
    type: "POST",
    async: false,
    data: { 'command' : 'add', 'serial' : serialNum },
    dataType: 'json',
    success: function (response) {
      //  $("sensor_table").addElement(serialNum);
      console.log(0)
      switch(response[0]){
        case "duplicated":
          window.alert("No puede haber seriales duplicadas");
          break;
        case "k":
          break;
        default:
          $("#sensor_table").append(newSensorRow(response));
          sensorNums.push(response[0]);
          break;
        }
      }
  });
}

function refreshSerial(refreshButton_reference){
  $(refreshButton_reference).html('<span class="glyphicon glyphicon-hourglass"></span>');
  $(refreshButton_reference).prop("disabled", true);
  $.ajax({
    url: '/plot/sensors/',
    type: "POST",
    async: false,
    data: { 'command' : 'refresh' },
    dataType: 'json',
    success: function (response) {
      //  $("sensor_table").addElement(serialNum);
      var auxSensorNums = [];
      $("#sensor_table").html('<tr>' +
          '<th class="col-xs-1">N° de serie</th>' +
          '<th class="col-xs-1">Posición</th>' +
          '<th class="col-xs-1">Detrend</th>' +
          '<th class="col-xs-3">Trigger(x,y,z):</th>' +
          '<th class="col-xs-3">Detrigger(x,y,z):</th>' +
          '<th class="col-xs-3">Votos:</th>' +
          '<th class="col-xs-1">Trigger máximo(x,y,z):</th>' +
        '</tr>' +
        '<tr>' +
          '<td class="col-xs-1">' +
          '<td class="col-xs-1">' +
          '<td class="col-xs-1">' +
          '<td class="col-xs-3">' +
            '<input type="number" id="id_triggerXYZ" name="triggerXYZ" min=0.01 step=0.001 value=0.01>' +
            '<input type="button" id="id_setTrigger" name="setTrigger" value="Set" onclick="triggerSet()">' +
          '<td class="col-xs-3">' +
            '<input type="number" id="id_detriggerXYZ" name="detriggerXYZ" min=0.01 step=0.001 value=0.01>' +
            '<input type="button" id="id_setDetrigger" name="setDetrigger" value="Set" onclick="detriggerSet()">' +
          '<td class="col-xs-2">' +
            '<input type="number" id="id_votesXYZ" name="votesXYZ" min=0 value=1>' +
            '<input type="button" id="id_setVotes" name="setVotes" value="Set" onclick="votesSet()">' +
          '<td class="col-xs-1">' +
            '<input type="number" id="id_secondTriggerXYZ" name="secondTriggerXYZ" min=0.01 step=0.001 value=0.01>' +
            '<input type="button" id="id_setSecondTrigger" name="setSecondTrigger" value="Set" onclick="secondTriggerSet()">' +
        '</tr>');
      $.each(response, function(i, value){
          console.log(value[0]);
          if(jQuery.inArray(value[0],sensorNums) == -1){
          };
          $("#sensor_table").append(newSensorRow(value));
          auxSensorNums.push(value[0]);
      });
      sensorNums = auxSensorNums;
      $(refreshButton_reference).html('<span class="glyphicon glyphicon-refresh"></span>');
      $(refreshButton_reference).prop("disabled", false);
    }
  });
}

function triggerSet(){
  var r = $("#id_triggerXYZ").val();
  $("[class='trigger-input']").each(function(i, e){
    e.value = r;
  });
}

function detriggerSet(){
  var r = $("#id_detriggerXYZ").val();
  $("[class='detrigger-input']").each(function(i, e){
    e.value = r;
  });
}

function votesSet(){
  var r = $("#id_votesXYZ").val();
  $("[class='votes-input']").each(function(i, e){
    e.value = r;
  });
}

function secondTriggerSet(){
  var r = $("#id_secondTriggerXYZ").val();
  $("[class='secondtrigger-input']").each(function(i, e){
    e.value = r;
  });
}

function newSensorRow(value){
  if (value[15] == "1"){
    if (value[16] == "0"){
      return '<tr>' +
        '<input type="hidden" name="isRed'+value[0]+' "value="false">' +
        '<td class="col-xs-1">' +
          '<label class="checkbox-inline">' +
          '<input type="checkbox" checked="checked" onchange="verify_required_position(this)" name="check' + value[0] + '">' +
          '<input type="text" name="serialNum" readonly="true" value="' + value[0] + '">' +
        '<td class="col-xs-1">' +
          '<input type="text" name="position" data-checkboxName="from-check' + value[0] + '" required value="' + value[1] + '">' +
        '<td class="col-xs-1">' +
          '<input type="number" min=0 name="detrend" value=' + value[8] + '>' +
        '<td class="col-xs-3">' +
          '<input type="number" class="trigger-input" name="triggerX" min=0.01 step=0.001 value=' + value[2] + '>' +
          '<input type="number" class="trigger-input" name="triggerY" min=0.01 step=0.001 value=' + value[3] + '>' +
          '<input type="number" class="trigger-input" name="triggerZ" min=0.01 step=0.001 value=' + value[4] + '>' +
        '<td class="col-xs-3">' +
          '<input type="number" class="detrigger-input" name="detriggerX" min=0.01 step=0.001 value=' + value[5] + '>' +
          '<input type="number" class="detrigger-input" name="detriggerY" min=0.01 step=0.001 value=' + value[6] + '>' +
          '<input type="number" class="detrigger-input" name="detriggerZ" min=0.01 step=0.001 value=' + value[7] + '>' +
        '<td class="col-xs-2">' +
          '<input type="number" class="votes-input" name="votesX" min=0 value=' + value[9] + '>' +
          '<input type="number" class="votes-input" name="votesY" min=0 value=' + value[10] + '>' +
          '<input type="number" class="votes-input" name="votesZ" min=0 value=' + value[11] + '>' +
        '<td class="col-xs-1">' +
            '<input type="number" class="secondtrigger-input" name="secondTriggerX" min=0.01 step=0.001 value=' + value[12] + '>' +
            '<input type="number" class="secondtrigger-input" name="secondTriggerY" min=0.01 step=0.001 value=' + value[13] + '>' +
            '<input type="number" class="secondtrigger-input" name="secondTriggerZ" min=0.01 step=0.001 value=' + value[14] + '>' +
      '</tr>';
    }
    else{
      return '<tr>' +
        '<input type="hidden" name="isRed'+value[0]+' "value="true">' +
        '<td class="col-xs-1">'+
          '<label class="checkbox-inline">' +
          '<input type="checkbox" checked="checked" onchange="verify_required_position(this)" name="check' + value[0] + '">' +
          '<input type="text" class="text-danger" name="serialNum" readonly="true" value="' + value[0] + '">' +
        '<td class="col-xs-1"><input type="text" class="text-danger" name="position" data-checkboxName="from-check' + value[0] + '" required value="' + value[1] + '">' +
        '<td class="col-xs-1"><input type="number" min=0 name="detrend" value=' + value[8] + '>' +
        '<td class="col-xs-3">' +
          '<input type="number" class="trigger-input" name="triggerX" min=0.01 step=0.001 value=' + value[2] + '>' +
          '<input type="number" class="trigger-input" name="triggerY" min=0.01 step=0.001 value=' + value[3] + '>' +
          '<input type="number" class="trigger-input" name="triggerZ" min=0.01 step=0.001 value=' + value[4] + '>' +
        '<td class="col-xs-3">' +
          '<input type="number" class="detrigger-input" name="detriggerX" min=0.01 step=0.001 value=' + value[5] + '>' +
          '<input type="number" class="detrigger-input" name="detriggerY" min=0.01 step=0.001 value=' + value[6] + '>' +
          '<input type="number" class="detrigger-input" name="detriggerZ" min=0.01 step=0.001 value=' + value[7] + '>' +
        '<td class="col-xs-2">' +
          '<input type="number" class="votes-input" name="votesX" min=0 value=' + value[9] + '>' +
          '<input type="number" class="votes-input" name="votesY" min=0 value=' + value[10] + '>' +
          '<input type="number" class="votes-input" name="votesZ" min=0 value=' + value[11] + '>' +
        '<td class="col-xs-1">' +
            '<input type="number" class="secondtrigger-input" name="secondTriggerX" min=0.01 step=0.001 value=' + value[12] + '>' +
            '<input type="number" class="secondtrigger-input" name="secondTriggerY" min=0.01 step=0.001 value=' + value[13] + '>' +
            '<input type="number" class="secondtrigger-input" name="secondTriggerZ" min=0.01 step=0.001 value=' + value[14] + '>' +
      '</tr>';
    }
  }
  else{
    if (value[15] == "0"){
      return '<tr>' +
      '<input type="hidden" name="isRed'+value[0]+' "value="false">' +
      '<td class="col-xs-1"><label class="checkbox-inline">' +
        '<input type="checkbox" onchange="verify_required_position(this)" name="check' + value[0] + '">' +
        '<input type="text" name="serialNum" readonly="true" value="' + value[0] + '">' +
      '<td class="col-xs-1"><input type="text" name="position" data-checkboxName="from-check' + value[0] + '" value="' + value[1] + '">' +
      '<td class="col-xs-1"><input type="number" min=0 name="detrend" value=' + value[8] + '>' +
      '<td class="col-xs-3">' +
        '<input type="number" class="trigger-input" name="triggerX" min=0.01 step=0.001 value=' + value[2] + '>' +
        '<input type="number" class="trigger-input" name="triggerY" min=0.01 step=0.001 value=' + value[3] + '>' +
        '<input type="number" class="trigger-input" name="triggerZ" min=0.01 step=0.001 value=' + value[4] + '>' +
      '<td class="col-xs-3">' +
        '<input type="number" class="detrigger-input" name="detriggerX" min=0.01 step=0.001 value=' + value[5] + '>' +
        '<input type="number" class="detrigger-input" name="detriggerY" min=0.01 step=0.001 value=' + value[6] + '>' +
        '<input type="number" class="detrigger-input" name="detriggerZ" min=0.01 step=0.001 value=' + value[7] + '>' +
      '<td class="col-xs-2">' +
        '<input type="number" class="votes-input" name="votesX" min=0 value=' + value[9] + '>' +
        '<input type="number" class="votes-input" name="votesY" min=0 value=' + value[10] + '>' +
        '<input type="number" class="votes-input" name="votesZ" min=0 value=' + value[11] + '>' +
      '<td class="col-xs-1">' +
        '<input type="number" class="secondtrigger-input" name="secondTriggerX" min=0.01 step=0.001 value=' + value[12] + '>' +
        '<input type="number" class="secondtrigger-input" name="secondTriggerY" min=0.01 step=0.001 value=' + value[13] + '>' +
        '<input type="number" class="secondtrigger-input" name="secondTriggerZ" min=0.01 step=0.001 value=' + value[14] + '>' +
    '</tr>';
    }
    else{
      return "";
    }
  }
}

function verify_required_position(checkbox_element) {
  $("[data-checkboxName='from-" + $(checkbox_element).attr("name") + "']").attr('required', $(checkbox_element).is(":checked"));
}
