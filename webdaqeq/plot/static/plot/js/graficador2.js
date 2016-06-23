// var count = 0;
// var sensor_charts = [];
// $(function () {
//   var x = [
//     {x: 0, y: 2},
//     {x: 1, y: 2},
//     {x: 2, y: 2},
//     {x: 3, y: 2},
//     {x: 4, y: 2}];   //dataPoints. 
//   var y = [
//     {x: 0, y: 2},
//     {x: 1, y: 2},
//     {x: 2, y: 2},
//     {x: 3, y: 2},
//     {x: 4, y: 2}];   //dataPoints. 
//   var z = [
//     {x: 0, y: 2},
//     {x: 1, y: 2},
//     {x: 2, y: 2},
//     {x: 3, y: 2},
//     {x: 4, y: 2}];   //dataPoints. 

//   var chart = new CanvasJS.Chart("updating-chart",{
//     axisX: {            
//       title: "Time",
//       labelAutoFit: true,
//       labelFontSize: 10,
//       labelAngle: -89,
//       titleFontSize: 15
//     },
//     axisY: {            
//       title: "Aceleracion",
//       labelFontSize: 10,
//       titleFontSize: 15
//     },
//     data: [
//     {
//       type: "line",
//       dataPoints : x,
//       color: "red",
//       lineThickness: 1,
//     }, 
//     {
//       type: "line",
//       dataPoints : y,
//       color: "green",
//       lineThickness: 1,
//     }, 
//     {
//       type: "line",
//       dataPoints : z,
//       color: "blue",
//       lineThickness: 1,
//     }, 

//     ]
//   });

//   $.each(sensors, function(index, sensor) {
//     var sensor_chart_x = new CanvasJS.Chart("updating-chart" + (index + 1), {
//       axisX: {            
//         title: "Time",
//         labelAutoFit: true,
//         labelFontSize: 10,
//         labelAngle: -89,
//         titleFontSize: 15
//       },
//       axisY: {            
//         title: "Aceleracion",
//         labelFontSize: 10,
//         titleFontSize: 15
//       },
//       data: [
//       {
//         type: "line",
//         dataPoints : x,
//         color: "red",
//         lineThickness: 1,
//       },

//       ]
//     });
//     sensor_chart_x.render();
//     console.log(sensor_chart_x);

//     var updateChart1 = function() {
//       sensor_charts[0][0].options.data[0]['dataPoints'] = buffer_x;
//       sensor_charts[0][0].render();
//     };

//     setInterval(function(){updateChart1()}, 100);
//   });

//   chart.render();
//   console.log(sensor_charts);
//   var updateInterval = 20;

//   var updateChart = function () {
//     chart.options.data[0]['dataPoints'] = buffer_x['data'];
//     chart.options.data[1]['dataPoints'] = buffer_y['data'];
//     chart.options.data[2]['dataPoints'] = buffer_z['data'];
//     var max = Math.max.apply(Math, [buffer_x['max'], buffer_y['max'], buffer_z['max']]);
//     max = max + 0.05*max;

//     chart.options.axisY['maximum'] = max;
//     chart.options.axisY['minimum'] = -1 * max;
//     // chart.options.axisY['viewportMaximum'] = max;
//     // chart.options.axisY['viewportMinimum'] = -1 * max;
//     chart.render();
//   };

//   var updateChart1 = function() {
//     sensor_charts[0][0].options.data[0]['dataPoints'] = buffer_x;
//     sensor_charts[0][0].render();
//   };

// // setInterval(function(){updateChart()}, updateInterval); 
// // setInterval(function(){updateChart1()}, updateInterval);
// });