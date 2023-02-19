// current sequence
var currentSequence = -1;

//This fucntion is to initiate the selected dataset
function init() {
  currentSequence = -1;
  document.getElementsByName("datasets")[0].selectedIndex = "0";
}

//This fucntion is to load data set from json file
function loadData() {
  currentSequence = -1;
  d3.select("#selectedRow").attr("class", "row");

  var parameters = {
    "dataset": document.getElementsByName("datasets")[0].value
  };

  console.log(parameters)

  var request = new XMLHttpRequest();
  request.open('POST', '/dimRed', false);
  request.setRequestHeader("Content-Type", "application/json");
  request.send(JSON.stringify(parameters));
  
  var content = JSON.parse(request.responseText.trim());
  console.log(content)

  seqlengthfloat = content["seqlength"];
  time_increment = content["time_increment"];
  accuracy = content["accuracy"];
  hiddenStates = content["hiddenStatesgru"];
  gruweights = content["gruweights"];
  zerohidden=content["zerohidden"];
  hiddenStatesreshape = content["hiddenStatesreshape"];
  hiddenstateo = content["hiddenstateo"];
  testinputs = content["testinputs"];
  actualValues = content["actualValues"];
  predictions = content["predictions"];
  pca_projection = content["pcaprojection"];
  projection = content["projection"];
  nfeatures=content["nfeatures"];
  projectiono = content["projectiono"];
  //mds_projection = content["mdsprojection"];
  umap_projection = content["umapprojection"];


  c0=content["c0"];
  c1=content["c1"];
  c2=content["c2"];
  c3=content["c3"];
  c4=content["c4"];
  c5=content["c5"];
  c6=content["c6"];
  c7=content["c7"];
  c8=content["c8"];
  c9=content["c9"];
  c10=content["c10"];
  c11=content["c11"];
  c12=content["c12"];
  c13=content["c13"];
  c14=content["c14"];
  c15=content["c15"];
  c16=content["c16"];
  c17=content["c17"];
  c18=content["c18"];
  c19=content["c19"];

  co0=content["co0"];
  co1=content["co1"];
  co2=content["co2"];
  co3=content["co3"];
  co4=content["co4"];
  co5=content["co5"];
  co6=content["co6"];
  co7=content["co7"];
  co8=content["co8"];
  co9=content["co9"];
  co10=content["co10"];
  co11=content["co11"];
  co12=content["co12"];
  co13=content["co13"];
  co14=content["co14"];
  co15=content["co15"];
  co16=content["co16"];
  co17=content["co17"];
  co18=content["co18"];
  co19=content["co19"];

  seqlength=Math.floor(seqlengthfloat)
  
  document.getElementById("handle3").checked = "checked";
  
  var sentenceOverview = [];
  for (var i = 0; i < actualValues.length; ++i) {
   sentenceOverview.push({
    "Id":i,
    "Original end values closure terms":actualValues[i],
    "Predicted values closure terms":predictions[i],
    "Error between closure terms":Math.sqrt((Math.pow((actualValues[i][0]-predictions[i][0]),2))+
      (Math.pow((actualValues[i][1]-predictions[i][1]),2))+
      (Math.pow((actualValues[i][2]-predictions[i][2]),2))),
     "Sequence of Inputs with 3 velocities": testinputs[i]
    });
  }
  
  console.log(sentenceOverview)

  d3.select('#page-wrap').selectAll("*").remove();
  createTable(sentenceOverview);
 
}
//This fucntion executes whenever clciking particular input from the mainviztable
function showSequence(seqId) {
    if (document.getElementById("zeroth").checked){
        zeroth(seqId)
      }
}


function zeroth(seqId){
    console.log(projectiono.length)
    testsample=testinputs.length
    console.log(testsample)

    var myColor = d3.scaleSequential().domain([0,seqlength])
    .interpolator(d3.interpolateCool);

    var colourArray = d3.range((seqlength-1)).map(function(d) {
    return myColor(d)
    });;

    console.log(colourArray)
   
    if (seqlength==3){
        for (var i = 0; i < projectiono.length; i++){
            if ( i % 4 == 0) {
            projectiono.splice(i, 1, projectiono[0])
            }}
        console.log(projectiono.length)
        console.log(projectiono[0])
    
        var colors =  ["#FF1F5B", "#00CD6C", "#009ADE", "#AF58BA00", "#FFC61E", "#F28522", "#A0B1BA",
                                                "#A6761D", "#E9002D", "#FFAA00", "#00B00000","#0a0800"];
    
        seqid=seqId
        v1=[]
        c=0
        for(var i=0;i<projectiono.length-1;++i){
        
        if(c==4){c=0}
        v1.push({
                    p: [{x:projectiono[i][0],y:projectiono[i][1]}, {x:projectiono[i+1][0],y: projectiono[i+1][1]}],
                    col: colors[c]
                    
                });
                c++
        }
        
        d3.select("#tsne").selectAll("circle").remove();
        
        
        d3.select("#tsne").selectAll("*").remove();
        var svg = d3.select("#tsne");
        svg.selectAll("*").remove();
        
        
        var margin = {top: 100, right: 30, bottom: 40, left: 100},
        width = 500 - margin.left - margin.right,
        height = 1000 - margin.top - margin.bottom;
        
        var svg = d3.select("#tsne")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                    "translate(" + (margin.left+20) + "," + (margin.top+30) + ")");
      
                
          
        var lineFunction = d3.line()
            .x(function(d) { return d.x; })
            .y(function(d) { return d.y; })
            .curve(d3.curveLinear);
            
        let path= svg.selectAll('.segment')
            .data(v1)
            .enter().append("path")
            .attr('class','segment')
            .attr('d', function(d) { return lineFunction(d.p); })
            .attr('stroke-width', 0.5)
            .attr('stroke', function(d) { return d.col; })
            .attr('fill',"none")
            .attr('opacity',"0.5")
            .attr("shape-rendering", "crispEdges")
      
             function tweenDash() {
        let l = this.getTotalLength(),
            i = d3.interpolateString("0," + l, l + "," + l);
        return function(t) { return i(t) };
        }
        path.transition()
            .duration(10)
            .ease(d3.easeLinear)
            .attrTween("stroke-dasharray", tweenDash)      
    }
    
    if (seqlength==5){
        for (var i = 0; i < projectiono.length; i++){
            if ( i % 6 == 0) {
            projectiono.splice(i, 1, projectiono[0])
            }}
        console.log(projectiono.length)
        console.log(projectiono[0])
    
        var colors =  ["#FF1F5B", "#00CD6C", "#009ADE", "#AF58BA00", "#FFC61E", "#F2852200", "#A0B1BA",
                                                "#A6761D", "#E9002D", "#FFAA00", "#00B00000","#0a0800"];
    
        seqid=seqId
        v1=[]
        c=0
        for(var i=0;i<projectiono.length-1;++i){
        
        if(c==6){c=0}
        v1.push({
                    p: [{x:projectiono[i][0],y:projectiono[i][1]}, {x:projectiono[i+1][0],y: projectiono[i+1][1]}],
                    col: colors[c]
                    
                });
                c++
        }
        
        d3.select("#tsne").selectAll("circle").remove();
        
        
        d3.select("#tsne").selectAll("*").remove();
        var svg = d3.select("#tsne");
        svg.selectAll("*").remove();
        
        
        var margin = {top: 100, right: 30, bottom: 40, left: 100},
        width = 500 - margin.left - margin.right,
        height = 1000 - margin.top - margin.bottom;
        
        var svg = d3.select("#tsne")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                    "translate(" + (margin.left+20) + "," + (margin.top+30) + ")");
    
                
        
        var lineFunction = d3.line()
            .x(function(d) { return d.x; })
            .y(function(d) { return d.y; })
            .curve(d3.curveLinear);
            
        let path= svg.selectAll('.segment')
            .data(v1)
            .enter().append("path")
            .attr('class','segment')
            .attr('d', function(d) { return lineFunction(d.p); })
            .attr('stroke-width', 0.5)
            .attr('stroke', function(d) { return d.col; })
            .attr('fill',"none")
            .attr('opacity',"0.5")
            .attr("shape-rendering", "crispEdges")
    
            function tweenDash() {
        let l = this.getTotalLength(),
            i = d3.interpolateString("0," + l, l + "," + l);
        return function(t) { return i(t) };
        }
        path.transition()
            .duration(10)
            .ease(d3.easeLinear)
            .attrTween("stroke-dasharray", tweenDash)      
    }
    
    if (seqlength==10){
    for (var i = 0; i < projectiono.length; i++){
        if ( i % 11 == 0) {
        projectiono.splice(i, 1, projectiono[0])
        }}
    console.log(projectiono.length)
    console.log(projectiono[0])

    var colors =  ["#FF1F5B", "#00CD6C", "#009ADE", "#AF58BA", "#FFC61E", "#F28522", "#A0B1BA",
                                            "#A6761D", "#E9002D", "#FFAA00", "#00B00000","#0a0800"];

    seqid=seqId
    v1=[]
    c=0
    for(var i=0;i<projectiono.length-1;++i){
    
    if(c==11){c=0}
    v1.push({
                p: [{x:projectiono[i][0],y:projectiono[i][1]}, {x:projectiono[i+1][0],y: projectiono[i+1][1]}],
                col: colors[c]
                
            });
            c++
    }
    
    d3.select("#tsne").selectAll("circle").remove();
    
    
    d3.select("#tsne").selectAll("*").remove();
    var svg = d3.select("#tsne");
    svg.selectAll("*").remove();
    
    
    var margin = {top: 100, right: 30, bottom: 40, left: 100},
    width = 500 - margin.left - margin.right,
    height = 1000 - margin.top - margin.bottom;
    
    var svg = d3.select("#tsne")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
                "translate(" + (margin.left+20) + "," + (margin.top+30) + ")");
  
            
      
    var lineFunction = d3.line()
        .x(function(d) { return d.x; })
        .y(function(d) { return d.y; })
        .curve(d3.curveLinear);
        
    let path= svg.selectAll('.segment')
        .data(v1)
        .enter().append("path")
        .attr('class','segment')
        .attr('d', function(d) { return lineFunction(d.p); })
        .attr('stroke-width', 0.5)
        .attr('stroke', function(d) { return d.col; })
        .attr('fill',"none")
        .attr('opacity',"0.5")
        .attr("shape-rendering", "crispEdges")
  
         function tweenDash() {
    let l = this.getTotalLength(),
        i = d3.interpolateString("0," + l, l + "," + l);
    return function(t) { return i(t) };
    }
    path.transition()
        .duration(10)
        .ease(d3.easeLinear)
        .attrTween("stroke-dasharray", tweenDash)      
    }

    if (seqlength==20){
        for (var i = 0; i < projectiono.length; i++){
            if ( i % 21 == 0) {
            projectiono.splice(i, 1, projectiono[0])
            }}
        console.log(projectiono.length)
        console.log(projectiono[0])
    
        //var colors =  ["#FF1F5B", "#00CD6C", "#009ADE", "#AF58BA", "#FFC61E", "#F28522", "#A0B1BA",
         //                                       "#A6761D", "#E9002D", "#FFAA00", "#00B00000","#0a0800"];
         var colors =  ['#e6194b', '#000075', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', 
         '#800000', '#aaffc3', '#808000', '#ffd8b1', '#3cb44b', '#808080', '#00000000','#ffffff']
        seqid=seqId
        v1=[]
        c=0
        for(var i=0;i<projectiono.length-1;++i){
        
        if(c==21){c=0}
        v1.push({
                    p: [{x:projectiono[i][0],y:projectiono[i][1]}, {x:projectiono[i+1][0],y: projectiono[i+1][1]}],
                    col: colors[c]
                    
                });
                c++
        }
        
        d3.select("#tsne").selectAll("circle").remove();
        
        
        d3.select("#tsne").selectAll("*").remove();
        var svg = d3.select("#tsne");
        svg.selectAll("*").remove();
        
        
        var margin = {top: 100, right: 30, bottom: 40, left: 100},
        width = 500 - margin.left - margin.right,
        height = 1000 - margin.top - margin.bottom;
        
        var svg = d3.select("#tsne")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                    "translate(" + (margin.left+20) + "," + (margin.top+30) + ")");
      
                
          
        var lineFunction = d3.line()
            .x(function(d) { return d.x; })
            .y(function(d) { return d.y; })
            .curve(d3.curveLinear);
            
        let path= svg.selectAll('.segment')
            .data(v1)
            .enter().append("path")
            .attr('class','segment')
            .attr('d', function(d) { return lineFunction(d.p); })
            .attr('stroke-width', 0.5)
            .attr('stroke', function(d) { return d.col; })
            .attr('fill',"none")
            .attr('opacity',"0.5")
            .attr("shape-rendering", "crispEdges")
      
             function tweenDash() {
        let l = this.getTotalLength(),
            i = d3.interpolateString("0," + l, l + "," + l);
        return function(t) { return i(t) };
        }
        path.transition()
            .duration(10)
            .ease(d3.easeLinear)
            .attrTween("stroke-dasharray", tweenDash)      
    }
}

//this function shows all the scatterpoints
function loadscatter() {


    if(document.getElementById("scatterpoints").checked) 
   {
     
    let checkboxes = document.querySelectorAll('input[name="scatterpoints"]:checked');
    let scatters = [];
    checkboxes.forEach((checkbox) => {
      scatters.push(checkbox.value);
    });
    console.log(scatters)
    console.log(typeof(scatters))
   
  
    scatters.forEach(scatter)
  
    //function clusterchange(item){
     // console.log(item)
    //}
  
    }
}
  
function scatter(seqId){
  
    console.log(projectiono.length)
    testsample=testinputs.length
    console.log(testsample)
   
    var myColor1 = d3.scaleSequential().domain([0,seqlength])
    .interpolator(d3.interpolateRainbow);
  
    var colourArray1 = d3.range((seqlength)).map(function(d) {
      return myColor1(d)
      });;
  
    
    scatterpoints=[]
    c=0
    for(var i=0;i<projectiono.length-1;++i){
    
    if(c==seqlength+1){c=0}
  
  
    scatterpoints.push({
      x:projectiono[i][0],
      y:projectiono[i][1],
      col:colourArray1[c]
    })
    c++;
    }
   
    console.log(scatterpoints)
  
    d3.select("#tsne").selectAll("circle").remove();
  
  
    d3.select("#tsne").selectAll("*").remove();
    var svg = d3.select("#tsne");
    svg.selectAll("*").remove();
     
      
    var margin = {top: 20, right: 30, bottom: 40, left: 100},
    width = 800 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;
      
      
    var svg = d3.select("#tsne")
        .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform",
                "translate(" + (margin.left+20) + "," + (margin.top+110) + ")");
  
    var scatter=svg.append('g')
    scatter
      .selectAll("circle")
      .data(scatterpoints)
      .enter()
      .append("circle")
        .attr("cx", function (d) { return d.x; } )
        .attr("cy",  function (d) { return d.y; } )
        .attr("r", 1)
        .style("fill", function(d) { return d.col; })
        .style("opacity", 1)
  
}