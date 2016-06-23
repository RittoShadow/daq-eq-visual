// $(function() {
//   var canvas = document.getElementById('updating-chart'),
//       ctx = canvas.getContext('2d'),
//       startingData = {
//         labels: [1, 2, 3, 4, 5, 6, 7],
//         datasets: [
//             {
//                 fillColor: "rgba(220,220,220,0.2)",
//                 strokeColor: "rgba(220,220,220,1)",
//                 pointColor: "rgba(220,220,220,1)",
//                 pointStrokeColor: "#fff",
//                 data: [65, 59, 80, 81, 56, 55, 40]
//             },
//             {
//                 fillColor: "rgba(151,187,205,0.2)",
//                 strokeColor: "rgba(151,187,205,1)",
//                 pointColor: "rgba(151,187,205,1)",
//                 pointStrokeColor: "#fff",
//                 data: [28, 48, 40, 19, 86, 27, 90]
//             }
//         ]
//       },
//       latestLabel = startingData.labels[6];

//   // Reduce the animation steps for demo clarity.
//   // var myLiveChart = new Chart(ctx).Line(startingData, {animationSteps: 15});

//   var myLiveChart = new Chart(ctx, {
//     type: "line",
//     data: startingData
//   });
//   console.log(myLiveChart);
//   var i = 10;
//   var bool = false;
//   setInterval(function(){
//     // Add two random numbers for each dataset
//     // myLiveChart.addData([Math.random() * 100, Math.random() * 100], ++latestLabel);
//     // // Remove the first point so we dont just add values forever
//     // myLiveChart.removeData();
//     var newData1 = myLiveChart.data.datasets[0]['data'];
//     var newData2 = myLiveChart.data.datasets[1]['data'];
//     $.each(newData1, function(index, value) {
//       if(bool) {
//         newData1[index] = value + i;
//         newData2[index] = value + i;
//       } else {
//         newData1[index] = value - i;
//         newData2[index] = value - i;
//       }
//       bool = !bool;
//     });
//     myLiveChart.data.datasets[0]['data'] = newData1;
//     myLiveChart.data.datasets[1]['data'] = newData2;
//     myLiveChart.update();
//   }, 100);

// });



var count = 0;
var starve = false;
// var str = [];
var sensor = "";
  var data = {
    labels : ["0"],
    datasets : [
      {
        label: "X",
        fillColor : "rgba(66,133,244,0)",
        strokeColor : "rgba(66,133,244,1)",
        pointColor : "rgba(66,69,244,1)",
        pointStrokeColor : "#fff",
        data : [0]
      },
      {
        label: "Y",
        fillColor : "rgba(187,24,119,0)",
        strokeColor : "rgba(187,24,119,1)",
        pointColor : "rgba(187,24,180,1)",
        pointStrokeColor : "#fff",
        data: [0]
      },
      {
        label: "Z",
        fillColor : "rgba(61,187,24,0)",
        strokeColor : "rgba(61,187,24,1)",
        pointColor : "rgba(24,187,46,1)",
        pointStrokeColor : "#fff",
        data: [0]
      },

    ]
  }
$(function(){
  // this is ugly, don't judge me
  var updateData = function(oldData, oldStr){
    if (str != [] && str.length > 1) {
      if (count == 0) {
        sensor = str[0];
      }
      if (str[0] != sensor) {
        return false;
      }
      if (!starve) {
        count++;
      }
      var labels = oldData["labels"];
      var dataSetX = oldData["datasets"][0]["data"];
      var dataSetY = oldData["datasets"][1]["data"];
      var dataSetZ = oldData["datasets"][2]["data"];

      var arr = str;
      labels.push(arr[1].toString());
      var newDataX = arr[2];
      var newDataY = arr[3];
      var newDataZ = arr[4];
      dataSetX.push(newDataX);
      dataSetY.push(newDataY);
      dataSetZ.push(newDataZ);
      if (count > 100) {
        starve = true;
      }
      if (starve) {
        labels.shift();
        dataSetX.shift();
        dataSetY.shift();
        dataSetZ.shift();
      }
    }

    return true;
  };

  var optionsAnimation = {
    //Boolean - If we want to override with a hard coded scale
    scaleOverride : true,
    showTooltip: true,
    responsive: true,
    //** Required if scaleOverride is true **
    //Number - The number of steps in a hard coded scale
    scaleSteps : 10,
    //Number - The value jump in the hard coded scale
    scaleStepWidth : 10,
    //Number - The scale starting value
    scaleStartValue : 0
  }

  // Not sure why the scaleOverride isn't working...
  var optionsNoAnimation = {
    animation : false,
    //Boolean - If we want to override with a hard coded scale
    scaleOverride : true,
    showTooltip: true,
    responsive: true,
    //** Required if scaleOverride is true **
    //Number - The number of steps in a hard coded scale
    scaleSteps : 10,
    //Number - The value jump in the hard coded scale
    scaleStepWidth : 10,
    //Number - The scale starting value
    scaleStartValue : 0
  }
  var canvas = $('#updating-chart')[0],
      ctx = canvas.getContext('2d'),
      startingData = data,
      latestLabel = data.labels[0];

  var myLiveChart = new Chart(ctx, {
    type: "line",
    data: startingData, 
    options: optionsNoAnimation
  });

  setInterval(function(){
    if(updateData(data,str)) {
      myLiveChart.data = data;
      myLiveChart.update();
    }
    ;}, 100
    // setInterval(function(){
    // updateData(data,str);
    // myNewChart.Line(data, optionsNoAnimation)
    // ;}, 100
  );
});