var sensors = [];
var str = [];
// var buffer = [];
var buffer_x = [];
var buffer_y = [];
var buffer_z = [];

var buffers = [];
var count = 0;
var sensor_charts = [];
var chart = null;
var should_show_plot = true;

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

function setShowPlot() {
  console.log(should_show_plot);
  if (should_show_plot) {
    $('#pause-btn').css('display', 'none');
    $('#start-btn').css('display', 'inline-block');
  } else {
    $('#pause-btn').css('display', 'inline-block');
    $('#start-btn').css('display', 'none');
  }
  should_show_plot = !should_show_plot;
}

$(function () {
    //change example.com with your IP or your host
  var ws = new WebSocket("ws://" + $("#websocket-ip").val() + ":7000/ws");
  ws.onopen = function(evt) {
    var conn_status = $('#conn_text');
    conn_status.removeClass('label-danger');
    conn_status.addClass('label-success');
    conn_status.text("Conectado.");
  };
  ws.onmessage = function(evt) {
    var aux = JSON.parse(evt.data);
 
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
        chart = setupMainGraph("updating-chart", sensors);
      }

    }
    else if (type == 'data') {
      aux = aux['data'];
      var time_stamp_array = [];
      $.each(aux, function(index, e) {
        var new_x = [];
        var new_y = [];
        var new_z = [];
        var max_x = 0.01;
        var max_y = 0.01;
        var max_z = 0.01;
        var first_timestamp = true;
        var i = 0;
        $.each(e, function(index2, s_data) {
          var aux2 = s_data.split(';');
          var time_stamp = parseFloat(aux2[1]);
          if (first_timestamp) {
            time_stamp_array.push(parseFloat(aux2[1]));
            
          }
          var x = parseFloat(aux2[2]);
          var y = parseFloat(aux2[3]);
          var z = parseFloat(aux2[4]);

          if (Math.abs(x) > max_x) max_x = Math.ceil10(x,-2);
          if (Math.abs(y) > max_y) max_y = Math.ceil10(y,-2);
          if (Math.abs(z) > max_z) max_z = Math.ceil10(z,-2);

          // new_x.push({x: time_stamp, y: x});
          // new_y.push({x: time_stamp, y: y});
          // new_z.push({x: time_stamp, y: z});
          new_x.push({x: time_stamp_array[i], y: x});
          new_y.push({x: time_stamp_array[i], y: y});
          new_z.push({x: time_stamp_array[i], y: z});
          i ++;
        });
        buffers[index] = {};
        buffers[index]['x'] = {};
        buffers[index]['y'] = {};
        buffers[index]['z'] = {};
        buffers[index]['x']['data'] = new_x;
        buffers[index]['y']['data'] = new_y;
        buffers[index]['z']['data'] = new_z;
        buffers[index]['x']['max'] = max_x;
        buffers[index]['y']['max'] = max_y;
        buffers[index]['z']['max'] = max_z;
        i = i + 1;
        first_timestamp = false;
      });
      first_timestamp = false;
      if (should_show_plot) {
        if ($("#main-chart").hasClass("active")) {
          updateChart();
        }
        // updateChart();
        var i = 0;
        // updateMainChart(chart, sensors);
        // updateChart();
        $.each(sensor_charts, function(index, chart) {     
          var sensor_name = sensors[i];
          if ($("#" + sensor_name).hasClass("active")) {
            updateChartPlot(chart['x'], buffers[sensor_name]['x']);
            updateChartPlot(chart['y'], buffers[sensor_name]['y']);
            updateChartPlot(chart['z'], buffers[sensor_name]['z']);
          }
          
          i = i + 1;
        });
      }
      // if ($("#main-chart").hasClass("active")) {
      //   updateChart();
      // }
      // updateChart();
      // var i = 0;
      // // updateMainChart(chart, sensors);
      // // updateChart();
      // $.each(sensor_charts, function(index, chart) {     
      //   var sensor_name = sensors[i];
      //   if ($("#" + sensor_name).hasClass("active")) {
      //     updateChartPlot(chart['x'], buffers[sensor_name]['x']);
      //     updateChartPlot(chart['y'], buffers[sensor_name]['y']);
      //     updateChartPlot(chart['z'], buffers[sensor_name]['z']);
      //   }
        
      //   i = i + 1;
      // });
      
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
    var element = '<li id="'+ name +'"><a data-toggle="tab" href="#sensor' +
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
    var x = [];
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
  };

  function genInitData(sensors) {
    var data = [];
    var i = 0;
    while (i < sensors.length) {
      var obj_x = {
        type: "line",
        dataPoints: [],
        color: "red",
        lineThickness: 1,
      };
      var obj_y = {
        type: "line",
        dataPoints: [],
        color: "green",
        lineThickness: 1,
      };
      var obj_z = {
        type: "line",
        dataPoints: [],
        color: "blue",
        lineThickness: 1,
      };
      data.push(obj_x);
      data.push(obj_y);
      data.push(obj_z);
      i = i + 1;
    }
    return data;
  };

  function setupMainGraph(canvas_id, sensors) {
    var mainChart = new CanvasJS.Chart(canvas_id, {
      axisX: config_axisX,
      axisY: {
        title: "Aceleración (g)",
        labelFontSize: 10,
        titleFontSize: 15,
      },
      data: genInitData(sensors),

    });
    mainChart.render();
    return mainChart;
  };

  function updateMainChart(chart, sensor_array) {

    $.each(sensor_array, function(index, sensor) {
      // chart.options.data[0]['dataPoints'] = buffers[sensor]['x']['data'];
      // chart.options.data[1]['dataPoints'] = buffers[sensor]['y']['data'];
      // chart.options.data[2]['dataPoints'] = buffers[sensor]['z']['data'];
      chart.options.data[index*3]['dataPoints'] = buffers[sensor]['x']['data'];
      chart.options.data[index*3 + 1]['dataPoints'] = buffers[sensor]['y']['data'];
      chart.options.data[index*3 + 2]['dataPoints'] = buffers[sensor]['z']['data'];
    });
    // chart.options.data[0]['dataPoints'] = buffers[sensor_array[0]]['x']['data'];
    // chart.options.data[1]['dataPoints'] = buffers[sensor_array[0]]['y']['data'];
    // chart.options.data[2]['dataPoints'] = buffers[sensor_array[0]]['z']['data'];
    chart.render();
  }

  function updateChartPlot(chart, dataset) {
    chart.options.data[0]['dataPoints'] = dataset['data'];
    var max = dataset['max'];
    chart.options.axisY['maximum'] = max;
    chart.options.axisY['minimum'] = -1 * max;
    chart.render();
  }

  var data_main = [];
  // $.each(sensors, function())

  // var chart = new CanvasJS.Chart("updating-chart",{
  //   axisX: config_axisX,
  //   axisY: {            
  //     title: "Aceleración (g)",
  //     labelFontSize: 10,
  //     titleFontSize: 15
  //   },
  //   data: [
  //   {
  //     type: "line",
  //     dataPoints : [],
  //     color: "red",
  //     lineThickness: 1,
  //   }, 
  //   {
  //     type: "line",
  //     dataPoints : [],
  //     color: "green",
  //     lineThickness: 1,
  //   }, 
  //   {
  //     type: "line",
  //     dataPoints : [],
  //     color: "blue",
  //     lineThickness: 1,
  //   }, 

  //   ]
  // });

  // chart.render();

  // var chart = setupMainGraph()

  var updateChart = function () {
    // var buf_x = buffer_x;
    // var buf_y = buffer_y;
    // var buf_z = buffer_z;
    // chart.options.data[0]['dataPoints'] = buf_x['data'];
    // chart.options.data[1]['dataPoints'] = buf_y['data'];
    // chart.options.data[2]['dataPoints'] = buf_z['data'];
    // var max = Math.max.apply(Math, [buf_x['max'], buf_y['max'], buf_z['max']]);

    // chart.options.axisY['maximum'] = max;
    // chart.options.axisY['minimum'] = -1 * max;
    // chart.render();
    updateMainChart(chart, sensors);
  };
});