var sensors = [];
var str = [];
// var buffer = [];
var buffer_x = [];
var buffer_y = [];
var buffer_z = [];

var buffers = [];
var count = 0;
var sensor_charts = [];

/* adjust decimals with floating point in account */
function decimalAdjust(type, value, exp) {
    // Si el exp no está definido o es cero...
    if (typeof exp === 'undefined' || +exp === 0) {
      return Math[type](value);
    }
    value = +value;
    exp = +exp;
    // Si el valor no es un número o el exp no es un entero...
    if (isNaN(value) || !(typeof exp === 'number' && exp % 1 === 0)) {
      return NaN;
    }
    // Shift
    value = value.toString().split('e');
    value = Math[type](+(value[0] + 'e' + (value[1] ? (+value[1] - exp) : -exp)));
    // Shift back
    value = value.toString().split('e');
    return +(value[0] + 'e' + (value[1] ? (+value[1] + exp) : exp));
  }

if (!Math.ceil10) {
    Math.ceil10 = function(value, exp) {
      return decimalAdjust('ceil', value, exp);
    };
  }

$(function () {
    //change example.com with your IP or your host
  var ws = new WebSocket("ws://localhost:7000/ws");
  ws.onopen = function(evt) {
    var conn_status = $('#conn_text');
    conn_status.removeClass('label-danger');
    conn_status.addClass('label-success');
    conn_status.text("Conectado.");
  };
  ws.onmessage = function(evt) {
    var aux = JSON.parse(evt.data);
    console.log(aux);
    var type = aux['type'];
    if (type == 'config') {
      sensors = aux['nombre_sensores'];
      if (sensors) {
        $.each(sensors, function(index, sensor) {
          addTab(index, sensor);
          addContent(index);
          buffers[index] = {};
          buffers[index]['x'] = [];
          buffers[index]['y'] = [];
          buffers[index]['z'] = [];
          sensor_charts[index] = {};
          sensor_charts[index]['x'] = setupGraph(setChartName(index,'x'), "red");
          sensor_charts[index]['y'] = setupGraph(setChartName(index,'y'), "green");
          sensor_charts[index]['z'] = setupGraph(setChartName(index,'z'), "blue");
        });
        ws.send("sensors ok");
      }
    }
    else if (type == 'data') {
      aux = aux['data'];
      var new_x = [];
      var new_y = [];
      var new_z = [];
      var max_x = 0.01;
      var max_y = 0.01;
      var max_z = 0.01;
      $.each(aux, function(index, e) {
        var aux2 = e.split(';');
        var time_stamp = parseFloat(aux2[1]);
        var x = parseFloat(aux2[2]);
        var y = parseFloat(aux2[3]);
        var z = parseFloat(aux2[4]);
        
        if (Math.abs(x) > max_x) max_x = Math.ceil10(x,-2);
        if (Math.abs(y) > max_y) max_y = Math.ceil10(y,-2);
        if (Math.abs(z) > max_z) max_z = Math.ceil10(z,-2);

        new_x.push({x: time_stamp, y: x});
        new_y.push({x: time_stamp, y: y});
        new_z.push({x: time_stamp, y: z});
      });
      buffer_x['data'] = new_x;
      buffer_x['max'] = max_x;
      buffer_y['data'] = new_y;
      buffer_y['max'] = max_y;
      buffer_z['data'] = new_z;
      buffer_z['max'] = max_z;

      // buffers[sensor]['x']['data'] = new_x;
      // buffers[sensor]['y']['data'] = new_y;
      // buffers[sensor]['z']['data'] = new_z;
      // buffers[sensor]['x']['max'] = max_x;
      // buffers[sensor]['y']['max'] = max_y;
      // buffers[sensor]['z']['max'] = max_z;

      updateChart();
      $.each(sensor_charts, function(index, chart) {
        updateChartPlot(chart['x'], buffer_x);
        updateChartPlot(chart['y'], buffer_y);
        updateChartPlot(chart['z'], buffer_z);
      });
    }
    else if (type == 'status') {

    }
    else {

    }
    
  };
  
  ws.onclose = function(evt) {
    var conn_status = $('#conn_text');
    conn_status.removeClass('label-success');
    conn_status.addClass('label-danger');
    conn_status.text("Desconectado.");
  };
  function addTab(number, name) {
    var element = '<li><a data-toggle="tab" href="#sensor' +
                    (number + 1) + '">Sensor ' + name + '</a></li>';
    $(".sensor-tabs").append(element);
  };
  function addContent(number) {
    var element = '<div id="sensor' + (number + 1) + 
                  '" class="tab-pane fade">' + 
                  '<div id="updating-chart'+(number + 1)+'_x" style="height: 200px; width: 100%;"></div>' +
                  '<div id="updating-chart'+(number + 1)+'_y" style="height: 200px; width: 100%;"></div>' +
                  '<div id="updating-chart'+(number + 1)+'_z" style="height: 200px; width: 100%;"></div>' +
                  '</div>';
    $(".sensor-content").append(element);
  };
  $("#button").click(function(evt) {
    evt.preventDefault();
    var message = $("#input_text").val();
    ws.send(message);
    var newMessage = document.createElement('p');
    newMessage.textContent = "Client: " + message;
    document.getElementById('messages_txt').innerHTML = newMessage.textContent;
  });


/* Graficos */
  var refresh_timer = 100; //milliseconds
  var config_axisX = {};
  config_axisX['labelFormatter'] = function(e) {
    return "";
  };

  function setChartName(index, axis) {
    return "updating-chart" + (index + 1) + "_" + axis;
  };

  function setupGraph(canvas_id, color ) {
    var x = [
      {x: 0, y: 2},
      {x: 1, y: 2},
      {x: 2, y: 2},
      {x: 3, y: 2},
      {x: 4, y: 2}];
    var sensor_chart_x = new CanvasJS.Chart(canvas_id, {
      axisX: config_axisX,
      axisY: {            
        title: "Aceleración (g)",
        labelFontSize: 10,
        titleFontSize: 15
      },
      data: [
      {
        type: "line",
        dataPoints : x,
        color: color,
        lineThickness: 1,
      },

      ]
    });
    sensor_chart_x.render();
    return sensor_chart_x;
  }

  function updateChartPlot(chart, dataset) {
    chart.options.data[0]['dataPoints'] = dataset['data'];
    var max = dataset['max'];
    chart.options.axisY['maximum'] = max;
    chart.options.axisY['minimum'] = -1 * max;
    chart.render();
  }

  var x = [
    {x: 0, y: 2},
    {x: 1, y: 2},
    {x: 2, y: 2},
    {x: 3, y: 2},
    {x: 4, y: 2}];   //dataPoints. 
  var y = [
    {x: 0, y: 2},
    {x: 1, y: 2},
    {x: 2, y: 2},
    {x: 3, y: 2},
    {x: 4, y: 2}];   //dataPoints. 
  var z = [
    {x: 0, y: 2},
    {x: 1, y: 2},
    {x: 2, y: 2},
    {x: 3, y: 2},
    {x: 4, y: 2}];   //dataPoints. 

  var chart = new CanvasJS.Chart("updating-chart",{
    axisX: config_axisX,
    axisY: {            
      title: "Aceleración (g)",
      labelFontSize: 10,
      titleFontSize: 15
    },
    data: [
    {
      type: "line",
      dataPoints : x,
      color: "red",
      lineThickness: 1,
    }, 
    {
      type: "line",
      dataPoints : y,
      color: "green",
      lineThickness: 1,
    }, 
    {
      type: "line",
      dataPoints : z,
      color: "blue",
      lineThickness: 1,
    }, 

    ]
  });

  chart.render();

  var updateChart = function () {
    var buf_x = buffer_x;
    var buf_y = buffer_y;
    var buf_z = buffer_z;
    chart.options.data[0]['dataPoints'] = buf_x['data'];
    chart.options.data[1]['dataPoints'] = buf_y['data'];
    chart.options.data[2]['dataPoints'] = buf_z['data'];
    var max = Math.max.apply(Math, [buf_x['max'], buf_y['max'], buf_z['max']]);

    chart.options.axisY['maximum'] = max;
    chart.options.axisY['minimum'] = -1 * max;
    chart.render();
  };
});