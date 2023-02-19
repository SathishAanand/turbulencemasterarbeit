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

  //console.log(co0.length)
  //console.log(co3.length)

  seqlength=Math.floor(seqlengthfloat)
  

  document.getElementById("handle3").checked = "checked";
   
  showDataInfo(-1);

  var sentenceOverview = [];
  for (var i = 0; i < actualValues.length; ++i) {
   sentenceOverview.push({
    "Id":i,
    "Original end values closure terms":actualValues[i],
    "Predicted values closure terms":predictions[i],
    "Error between closure terms":Math.sqrt(((Math.pow((actualValues[i][0]-predictions[i][0]),2))+
      (Math.pow((actualValues[i][1]-predictions[i][1]),2))+
      (Math.pow((actualValues[i][2]-predictions[i][2]),2)))/3),
     "Sequence of Inputs with velocities": testinputs[i]
    });
  }
  
  console.log(sentenceOverview)
  

  d3.select('#page-wrap').selectAll("*").remove();
  createTable(sentenceOverview);
  hiddentsneload()
}

//This fucntion executes when load dataset button is clicked
function showDataInfo(seqId) {

  var id = "dataInfo";
  var idSeq = "dataInfoSeqs";
  var idAcc = "dataInfoAcc";
  var idts = "dataInfots";
  var idinc = "dataInfoinc";
  var nf = "datanfeatures";

  d3.select("#" + id).selectAll("*").remove();

  var dataInfoContainer = d3.select("#" + id + "Container");
  if (seqId >= 0) {
     dataInfoContainer.style("display", "none");
      return;
  }

  dataInfoContainer.style("display", "block");

  //var dataInfoElement = document.getElementById(id);
    
  document.getElementById(idSeq).innerHTML = testinputs.length;
  document.getElementById(idAcc).innerHTML = accuracy;
  document.getElementById(idts).innerHTML = seqlength;
  document.getElementById(idinc).innerHTML = time_increment;
  document.getElementById(nf).innerHTML = nfeatures;

}

//This fucntion executes whenever clciking particular input from the mainviztable
function showSequence(seqId) {

  if(document.getElementById("Tsne").checked){
    hiddentsne(seqId)
    //hidden(seqId)
    hiddenheatmap(seqId)
  }

  if (document.getElementById("pca").checked){
    hiddenpca(seqId)
  }
  
  if (document.getElementById("umap").checked){
    hiddenumap(seqId)
  }
  //if (document.getElementById("mds").checked){
  //  hiddenmds(seqId)
  //}

  if (document.getElementById("zeroth").checked){
    hiddenzero(seqId)
  }

  
}

////This fucntion loads the overall tsne projection when the dataset is loaded 
function hiddentsneload(){

  console.log(projection.length)
  testsample=testinputs.length
  console.log(testsample)

  var myColor = d3.scaleSequential().domain([0,seqlength])
                  .interpolator(d3.interpolateRdYlGn);

  var colourArray = d3.range((seqlength-1)).map(function(d) {
  return myColor(d)
  });;

  console.log(colourArray)


  v1=[]
  c=0
  for(var i=0;i<projection.length-1;++i){
  
  if(c==seqlength){c=0}

  v1.push({
            p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
            col: colourArray[c]
            
          });
          c++
  }

  console.log(v1)
  
  d3.select("#tsne").selectAll("circle").remove();

  d3.select("#tsne").selectAll("*").remove();
  var svg = d3.select("#tsne");
  svg.selectAll("*").remove();
   
    
  var margin = {top: 20, right: 30, bottom: 40, left: 100},
  width = 500 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;
    
    
  var svg = d3.select("#tsne")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + (margin.left+20) + "," + (margin.top+110) + ")");
        
  var lineFunction = d3.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .curve(d3.curveLinear);

  let path= svg.selectAll('.segment')
           .data(v1)
           .enter().append("path")
           .attr('class','segment')
           .attr('d', function(d) { return lineFunction(d.p); })
           .attr('stroke-width', 0.3)
           .attr('stroke', "none")
           .attr('fill',"none")
           .attr('opacity',"0.3")
           .attr("shape-rendering", "crispEdges")
    
  function tweenDash() {

      let l = this.getTotalLength(),
          i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }
    
    
  path.transition()
    .duration(10)
    //.delay(function(d, i) { return i * 200; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
    
}
//end of tsne load

//This fucntion is used for scatterplot visualisation 
function hidden(seqId){
  d3.select("#mainSvg").selectAll("circle").remove();
  d3.select("#mainSvg").selectAll("text").remove();
  d3.select("#mainSvg").selectAll("defs").remove();
  
  d3.select("#mainSvg").selectAll("*").remove();
  var svg = d3.select("#mainSvg");
  svg.selectAll("*").remove();

  //3ts scatterplot
 if(seqlength==3){
  console.log("sequence id:"+ seqId)
  console.log(hiddenStates[seqId][0].length)
  console.log(hiddenStates[seqId][1].length)

  var myColor = d3.scaleSequential().domain([0,seqlength])
  .interpolator(d3.interpolateRainbow);

 var colourArray = d3.range((seqlength)).map(function(d) {
 return myColor(d)
 });;

 console.log(colourArray)
  
  scatterpoints1=[]
  c=1
  for(var i=0;i<hiddenStates[seqId][0].length;++i){
   var v=[]
   v[0]=c
   v[1]=hiddenStates[seqId][0][i]
   scatterpoints1.push(v);
   c++;
  }
  console.log(scatterpoints1)
  console.log(scatterpoints1[0][1])

  scatterpoints2=[]
  c=1
  for(var i=0;i<hiddenStates[seqId][1].length;++i){
  var v=[]
  v[0]=c
  v[1]=hiddenStates[seqId][1][i]
  scatterpoints2.push(v);
  c++;
  }
  console.log(scatterpoints2)
  console.log(scatterpoints2[0][1])

  scatterpoints3=[]
  c=1
  for(var i=0;i<hiddenStates[seqId][2].length;++i){
  var v=[]
  v[0]=c
  v[1]=hiddenStates[seqId][2][i]
  scatterpoints3.push(v);
  c++;
  }

  console.log(scatterpoints3)
  console.log(scatterpoints3[0][1])

  mini=d3.min(hiddenStates[seqId][1])

  console.log(mini)
  console.log(scatterpoints3.length)

  var margin = {top: -10, right: 10, bottom: 0, left: 5},
  width = 220 - margin.left - margin.right,
  height = 100 - margin.top - margin.bottom;


  var SVG = d3.select("#mainSvg")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("id","main")
      .attr("transform",
            "translate(" + (5) + "," + (-25) + ")");

  
  var x1 = d3.scaleLinear()
   .domain([0, (scatterpoints1.length)+1])
   .range([ 0, width ]);
  var x2 = d3.scaleLinear()
   .domain([0, (scatterpoints2.length)+1])
   .range([ 0, width ]);
  var x3 = d3.scaleLinear()
   .domain([0, (scatterpoints3.length)+1])
   .range([ 0, width ]);
  
  var y1 = d3.scaleLinear()
   .domain([-1, 1])
   .range([ height, 0]);
  var y2 = d3.scaleLinear()
   .domain([-1, 1])
   .range([  height, 0]);
  var y3 = d3.scaleLinear()
   .domain([-1, 1])
   .range([  height, 0 ]);
  

  var scatter1 = SVG.append('g')
     
  var scatter2 = SVG.append('g')
     
  var scatter3 = SVG.append('g')
     

  scatter1
   .selectAll("circle")
   .data(scatterpoints1)
   .enter()
   .append("circle")
     .attr("cx", function (d) { return x1(d[0]); } )
     .attr("cy",  function (d) { return y1(d[1]); } )
     .attr("r", 1)
     .style("fill", colourArray[0])
     .style("opacity", 0.8)
   
  scatter2
   .selectAll("circle")
   .data(scatterpoints2)
   .enter()
   .append("circle")
     .attr("cx", function (d) { return x2(d[0]); } )
     .attr("cy",  function (d) { return y2(d[1]); } )
     .attr("r", 1)
     .style("fill", colourArray[1])
     .style("opacity", 0.8)

  scatter3
   .selectAll("circle")
   .data(scatterpoints3)
   .enter()
   .append("circle")
     .attr("cx", function (d) { return x3(d[0]); } )
     .attr("cy",  function (d) { return y3(d[1]); } )
     .attr("r", 1)
     .style("fill", colourArray[2])
     .style("opacity", 0.8)
  }
   
  //////5ts scatterplot
  if(seqlength==5){
    console.log("sequence id:"+ seqId)
    console.log(hiddenStates[seqId][0].length)
    console.log(hiddenStates[seqId][1].length)
  
    var myColor = d3.scaleSequential().domain([0,seqlength])
    .interpolator(d3.interpolateRainbow);
  
   var colourArray = d3.range((seqlength)).map(function(d) {
   return myColor(d)
   });;
  
   console.log(colourArray)
    
    scatterpoints1=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][0].length;++i){
     var v=[]
     v[0]=c
     v[1]=hiddenStates[seqId][0][i]
     scatterpoints1.push(v);
     c++;
    }
    console.log(scatterpoints1)
    console.log(scatterpoints1[0][1])
  
    scatterpoints2=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][1].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][1][i]
    scatterpoints2.push(v);
    c++;
    }
    console.log(scatterpoints2)
    console.log(scatterpoints2[0][1])
  
    scatterpoints3=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][2].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][2][i]
    scatterpoints3.push(v);
    c++;
    }

    scatterpoints4=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][3].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][3][i]
    scatterpoints4.push(v);
    c++;
    }

    scatterpoints5=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][4].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][4][i]
    scatterpoints5.push(v);
    c++;
    }

    
  
    console.log(scatterpoints3)
    console.log(scatterpoints3[0][1])
  
    mini=d3.min(hiddenStates[seqId][1])
  
    console.log(mini)
    console.log(scatterpoints3.length)
  
    var margin = {top: -10, right: 10, bottom: 0, left: 5},
    width = 220 - margin.left - margin.right,
    height = 100 - margin.top - margin.bottom;
  
   
    var SVG = d3.select("#mainSvg")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("id","main")
        .attr("transform",
              "translate(" + (5) + "," + (-25) + ")");
  
    
    var x1 = d3.scaleLinear()
     .domain([0, (scatterpoints1.length)+1])
     .range([ 0, width ]);
    var x2 = d3.scaleLinear()
     .domain([0, (scatterpoints2.length)+1])
     .range([ 0, width ]);
    var x3 = d3.scaleLinear()
     .domain([0, (scatterpoints3.length)+1])
     .range([ 0, width ]);
    var x4 = d3.scaleLinear()
     .domain([0, (scatterpoints4.length)+1])
     .range([ 0, width ]);
    var x5 = d3.scaleLinear()
     .domain([0, (scatterpoints5.length)+1])
     .range([ 0, width ]);
   
   
    var y1 = d3.scaleLinear()
     .domain([-1, 1])
     .range([ height, 0]);
    var y2 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0]);
    var y3 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
    var y4 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
    var y5 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
   
    var scatter1 = SVG.append('g')
      
    var scatter2 = SVG.append('g')
      
    var scatter3 = SVG.append('g')
      
    var scatter4 = SVG.append('g')
    
    var scatter5 = SVG.append('g')
     
    scatter1
     .selectAll("circle")
     .data(scatterpoints1)
     .enter()
     .append("circle")
       .attr("cx", function (d) { return x1(d[0]); } )
       .attr("cy",  function (d) { return y1(d[1]); } )
       .attr("r", 1)
       .style("fill", colourArray[0])
       .style("opacity", 0.8)
     
    scatter2
     .selectAll("circle")
     .data(scatterpoints2)
     .enter()
     .append("circle")
       .attr("cx", function (d) { return x2(d[0]); } )
       .attr("cy",  function (d) { return y2(d[1]); } )
       .attr("r", 1)
       .style("fill", colourArray[1])
       .style("opacity", 0.8)
  
    scatter3
     .selectAll("circle")
     .data(scatterpoints3)
     .enter()
     .append("circle")
       .attr("cx", function (d) { return x3(d[0]); } )
       .attr("cy",  function (d) { return y3(d[1]); } )
       .attr("r", 1)
       .style("fill", colourArray[2])
       .style("opacity", 0.8)

    scatter4
    .selectAll("circle")
    .data(scatterpoints4)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x4(d[0]); } )
      .attr("cy",  function (d) { return y4(d[1]); } )
      .attr("r", 1)
      .style("fill", colourArray[3])
      .style("opacity", 0.8)

    scatter5
    .selectAll("circle")
    .data(scatterpoints5)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x5(d[0]); } )
      .attr("cy",  function (d) { return y5(d[1]); } )
      .attr("r", 1)
      .style("fill", colourArray[4])
      .style("opacity", 0.8)

  }
  //////10ts scatterplot
  if(seqlength==10){
    console.log("sequence id:"+ seqId)
    console.log(hiddenStates[seqId][0].length)
    console.log(hiddenStates[seqId][1].length)
  
   var myColor = d3.scaleSequential().domain([0,seqlength])
    .interpolator(d3.interpolateRainbow);
  
   var colourArray = d3.range((seqlength)).map(function(d) {
   return myColor(d)
   });;
  
   console.log(colourArray)
    
    scatterpoints1=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][0].length;++i){
     var v=[]
     v[0]=c
     v[1]=hiddenStates[seqId][0][i]
     scatterpoints1.push(v);
     c++;
    }
    console.log(scatterpoints1)
    console.log(scatterpoints1[0][1])
  
    scatterpoints2=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][1].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][1][i]
    scatterpoints2.push(v);
    c++;
    }
    console.log(scatterpoints2)
    console.log(scatterpoints2[0][1])
  
    scatterpoints3=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][2].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][2][i]
    scatterpoints3.push(v);
    c++;
    }

    scatterpoints4=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][3].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][3][i]
    scatterpoints4.push(v);
    c++;
    }

    scatterpoints5=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][4].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][4][i]
    scatterpoints5.push(v);
    c++;
    }

    scatterpoints6=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][5].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][5][i]
    scatterpoints6.push(v);
    c++;
    }

    scatterpoints7=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][6].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][6][i]
    scatterpoints7.push(v);
    c++;
    }

    scatterpoints8=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][7].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][7][i]
    scatterpoints8.push(v);
    c++;
    }

    scatterpoints9=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][8].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][8][i]
    scatterpoints9.push(v);
    c++;
    }

    scatterpoints10=[]
    c=1
    for(var i=0;i<hiddenStates[seqId][9].length;++i){
    var v=[]
    v[0]=c
    v[1]=hiddenStates[seqId][9][i]
    scatterpoints10.push(v);
    c++;
    }
  
    console.log(scatterpoints3)
    console.log(scatterpoints3[0][1])
  
    mini=d3.min(hiddenStates[seqId][1])
  
    console.log(mini)
    console.log(scatterpoints3.length)
  
    var margin = {top: -10, right: 10, bottom: 0, left: 5},
    width = 220 - margin.left - margin.right,
    height = 90 - margin.top - margin.bottom;
  
    var SVG = d3.select("#mainSvg")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("id","main")
        .attr("transform",
              "translate(" + (5) + "," + (-20) + ")");
  
    var x1 = d3.scaleLinear()
     .domain([0, (scatterpoints1.length)+1])
     .range([ 0, width ]);
    var x2 = d3.scaleLinear()
     .domain([0, (scatterpoints2.length)+1])
     .range([ 0, width ]);
    var x3 = d3.scaleLinear()
     .domain([0, (scatterpoints3.length)+1])
     .range([ 0, width ]);
    var x4 = d3.scaleLinear()
     .domain([0, (scatterpoints4.length)+1])
     .range([ 0, width ]);
    var x5 = d3.scaleLinear()
     .domain([0, (scatterpoints5.length)+1])
     .range([ 0, width ]);
    var x6 = d3.scaleLinear()
     .domain([0, (scatterpoints6.length)+1])
     .range([ 0, width ]);
    var x7 = d3.scaleLinear()
     .domain([0, (scatterpoints7.length)+1])
     .range([ 0, width ]);
    var x8 = d3.scaleLinear()
     .domain([0, (scatterpoints8.length)+1])
     .range([ 0, width ]);
    var x9 = d3.scaleLinear()
     .domain([0, (scatterpoints9.length)+1])
     .range([ 0, width ]);
    var x10 = d3.scaleLinear()
     .domain([0, (scatterpoints10.length)+1])
     .range([ 0, width ]);
    var xAxis = SVG.append("g")
     .attr("transform", "translate(" + (15) + "," + (-20) + ")")
     .call(d3.axisBottom(x1).ticks(32));
  
  
    // Add Y axis
    var y1 = d3.scaleLinear()
     .domain([-1, 1])
     .range([ height, 0]);
    var y2 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0]);
    var y3 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
    var y4 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
    var y5 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
    var y6 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
    var y7 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
    var y8 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
    var y9 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);
    var y10 = d3.scaleLinear()
     .domain([-1, 1])
     .range([  height, 0 ]);

    var scatter1 = SVG.append('g')

    var scatter2 = SVG.append('g')
      
    var scatter3 = SVG.append('g')
       
    var scatter4 = SVG.append('g')
    
    var scatter5 = SVG.append('g')
    
    var scatter6 = SVG.append('g')
     
    var scatter7 = SVG.append('g')
     
    var scatter8 = SVG.append('g')
     
    var scatter9 = SVG.append('g')
    
    var scatter10 = SVG.append('g')
    
  
    scatter1
     .selectAll("circle")
     .data(scatterpoints1)
     .enter()
     .append("circle")
       .attr("cx", function (d) { return x1(d[0]); } )
       .attr("cy",  function (d) { return y1(d[1]); } )
       .attr("r", 1)
       .style("fill", colourArray[0])
       .style("opacity", 0.8)

     
    scatter2
     .selectAll("circle")
     .data(scatterpoints2)
     .enter()
     .append("circle")
       .attr("cx", function (d) { return x2(d[0]); } )
       .attr("cy",  function (d) { return y2(d[1]); } )
       .attr("r", 1)
       .style("fill", colourArray[1])
       .style("opacity", 0.8)
  
    scatter3
     .selectAll("circle")
     .data(scatterpoints3)
     .enter()
     .append("circle")
       .attr("cx", function (d) { return x3(d[0]); } )
       .attr("cy",  function (d) { return y3(d[1]); } )
       .attr("r", 1)
       .style("fill", colourArray[2])
       .style("opacity", 0.8)

    scatter4
    .selectAll("circle")
    .data(scatterpoints4)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x4(d[0]); } )
      .attr("cy",  function (d) { return y4(d[1]); } )
      .attr("r", 1)
      .style("fill", colourArray[3])
      .style("opacity", 0.8)

    scatter5
    .selectAll("circle")
    .data(scatterpoints5)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x5(d[0]); } )
      .attr("cy",  function (d) { return y5(d[1]); } )
      .attr("r", 1)
      .style("fill", colourArray[4])
      .style("opacity", 0.8)

    scatter6
    .selectAll("circle")
    .data(scatterpoints6)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x6(d[0]); } )
      .attr("cy",  function (d) { return y6(d[1]); } )
      .attr("r", 1)
      .style("fill", colourArray[5])
      .style("opacity", 0.8)
    
    scatter7
    .selectAll("circle")
    .data(scatterpoints7)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x7(d[0]); } )
      .attr("cy",  function (d) { return y7(d[1]); } )
      .attr("r", 1)
      .style("fill", colourArray[6])
      .style("opacity", 0.8)


    scatter8
    .selectAll("circle")
    .data(scatterpoints8)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x8(d[0]); } )
      .attr("cy",  function (d) { return y8(d[1]); } )
      .attr("r", 1)
      .style("fill", colourArray[7])
      .style("opacity", 0.8)

    scatter9
    .selectAll("circle")
    .data(scatterpoints9)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x9(d[0]); } )
      .attr("cy",  function (d) { return y9(d[1]); } )
      .attr("r", 1)
      .style("fill", colourArray[8])
      .style("opacity", 0.8)

    scatter10
    .selectAll("circle")
    .data(scatterpoints10)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x10(d[0]); } )
      .attr("cy",  function (d) { return y10(d[1]); } )
      .attr("r", 1)
      .style("fill", colourArray[9])
      .style("opacity", 0.8)
  }

}

//heatmap function
function hiddenheatmap(seqId){
  
  d3.select("#mainSvg").selectAll("rect").remove();
  d3.select("#mainSvg").selectAll("circle").remove();
  d3.select("#mainSvg").selectAll("text").remove();
  d3.select("#mainSvg").selectAll("defs").remove();
  
  d3.select("#mainSvg").selectAll("*").remove();
  var svg = d3.select("#mainSvg");
  svg.selectAll("*").remove();
  
  //heatmap for 3ts
  if(seqlength==3){

    console.log("sequence id:"+ seqId)

    polylines1=[]
    c=1
    ts=1
    for(var i=0;i<hiddenStates[seqId][0].length;++i){
    var v=[]
    v[0]=c
    v[1]=ts
    v[2]=hiddenStates[seqId][0][i]
    polylines1.push(v);
    c++;
    }
    console.log(polylines1)
    console.log(polylines1[seqId][1])
  
    polylines2=[]
    c=1
    ts=2
    for(var i=0;i<hiddenStates[seqId][1].length;++i){
    var v=[]
    v[0]=c
    v[1]=ts
    v[2]=hiddenStates[seqId][1][i]
    polylines2.push(v);
    c++;
    }
    console.log(polylines2)
    console.log(polylines2[seqId][1])
  
    polylines3=[]
    c=1
    ts=3
    for(var i=0;i<hiddenStates[seqId][2].length;++i){
    var v=[]
    v[0]=c
    v[1]=ts
    v[2]=hiddenStates[seqId][2][i]
    polylines3.push(v);
    c++;
    }
    console.log(polylines3)
    console.log(polylines3[seqId][1])
  
    
  //mini=d3.min(polylines1, function(polylines1){ return polylines1[0][1];})
  //console.log(mini)
  
         
    var margin = {top: 30, right: 30, bottom: 30, left: 30},
      width = 950 - margin.left - margin.right,
      height = 250 ;
  
  // append the svg object to the body of the page
    var svg = d3.select("svg")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left  +")");
          
  
  
    function range(start, end) {
      return Array(end - start + 1).fill().map((_, idx) => start + idx)
    }
    var myGroups = range(1, 64); // [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    console.log(myGroups);
    var myVars = range(1, seqlength); // [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    console.log(myVars);
   
    
    overall=Array.prototype.concat.apply([], [polylines1, polylines2, polylines3]);
    console.log(overall)
    console.log(overall.length)
    
    var x = d3.scaleBand()
      .range([ 0, width ])
      .domain(myGroups)
      .padding(0.001);
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
  
    
    var y = d3.scaleBand()
      .range([ height, 0 ])
      .domain(myVars)
      .padding(0.001);
    svg.append("g")
      .call(d3.axisLeft(y));
  
  
    var myColor = d3.scaleLinear()
      .range(["white", "#b36969"])
      .domain([-1,1])
  
            // Step 5
        svg.selectAll()
        .data(overall)
        .enter()
        .append("rect")
          .attr("x", function(d) { return x(d[0]) })
          .attr("y", function(d) { return y(d[1]) })
          .attr("width", x.bandwidth() )
          .attr("height", y.bandwidth() )
          .style("fill", function(d) { return myColor(d[2])} )
  
     
  }
  

  //heatmap for 10ts
  if(seqlength==10){
  polylines1=[]
  c=1
  ts=1
  for(var i=0;i<hiddenStates[seqId][0].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][0][i]
  polylines1.push(v);
  c++;
  }
  console.log(polylines1)
  //console.log(polylines1[seqId][1])

  polylines2=[]
  c=1
  ts=2
  for(var i=0;i<hiddenStates[seqId][1].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][1][i]
  polylines2.push(v);
  c++;
  }
  console.log(polylines2)
  //console.log(polylines2[seqId][1])

  polylines3=[]
  c=1
  ts=3
  for(var i=0;i<hiddenStates[seqId][2].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][2][i]
  polylines3.push(v);
  c++;
  }
  console.log(polylines3)
  //console.log(polylines3[seqId][1])

  polylines4=[]
  c=1
  ts=4
  for(var i=0;i<hiddenStates[seqId][3].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][3][i]
  polylines4.push(v);
  c++;
  }

  polylines5=[]
  c=1
  ts=5
  for(var i=0;i<hiddenStates[seqId][4].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][4][i]
  polylines5.push(v);
  c++;
  }

  polylines6=[]
  c=1
  ts=6
  for(var i=0;i<hiddenStates[seqId][5].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][5][i]
  polylines6.push(v);
  c++;
  }

  polylines7=[]
  c=1
  ts=7
  for(var i=0;i<hiddenStates[seqId][6].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][6][i]
  polylines7.push(v);
  c++;
  }

  polylines8=[]
  c=1
  ts=8
  for(var i=0;i<hiddenStates[seqId][7].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][7][i]
  polylines8.push(v);
  c++;
  }

  polylines9=[]
  c=1
  ts=9
  for(var i=0;i<hiddenStates[seqId][8].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][8][i]
  polylines9.push(v);
  c++;
  }

  polylines10=[]
  c=1
  ts=10
  for(var i=0;i<hiddenStates[seqId][9].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][9][i]
  polylines10.push(v);
  c++;
  }
//mini=d3.min(polylines1, function(polylines1){ return polylines1[0][1];})
//console.log(mini)

  var margin = {top: 30, right: 30, bottom: 30, left: 30},
    width = 950 - margin.left - margin.right,
    height = 250 - margin.top - margin.bottom;


  var svg = d3.select("svg")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
        


  function range(start, end) {
    return Array(end - start + 1).fill().map((_, idx) => start + idx)
  }
  var myGroups = range(1, 64); // [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
  console.log(myGroups);
  var myVars = range(1, seqlength); // [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
  console.log(myVars);
  
  
  overall=Array.prototype.concat.apply([], [polylines1, polylines2, polylines3,
  polylines4,polylines5,polylines6,polylines7,polylines8,polylines9,polylines10]);
  console.log(overall)
  console.log(overall.length)
 
  var x = d3.scaleBand()
    .range([ 0, width ])
    .domain(myGroups)
    .padding(0.001);
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))

  
  var y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(myVars)
    .padding(0.001);
  svg.append("g")
    .call(d3.axisLeft(y));

 
  var myColor = d3.scaleLinear()
    .range(["white", "#b36969"])
    .domain([-1,1])

         
      svg.selectAll()
      .data(overall)
      .enter()
      .append("rect")
        .attr("x", function(d) { return x(d[0]) })
        .attr("y", function(d) { return y(d[1]) })
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .style("fill", function(d) { return myColor(d[2])} )

}

//heatmap for 20ts
if(seqlength==20){
  polylines1=[]
  c=1
  ts=1
  for(var i=0;i<hiddenStates[seqId][0].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][0][i]
  polylines1.push(v);
  c++;
  }
  console.log(polylines1)
  console.log(polylines1[seqId][1])

  polylines2=[]
  c=1
  ts=2
  for(var i=0;i<hiddenStates[seqId][1].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][1][i]
  polylines2.push(v);
  c++;
  }
  console.log(polylines2)
  console.log(polylines2[seqId][1])

  polylines3=[]
  c=1
  ts=3
  for(var i=0;i<hiddenStates[seqId][2].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][2][i]
  polylines3.push(v);
  c++;
  }
  console.log(polylines3)
  console.log(polylines3[seqId][1])

  polylines4=[]
  c=1
  ts=4
  for(var i=0;i<hiddenStates[seqId][3].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][3][i]
  polylines4.push(v);
  c++;
  }

  polylines5=[]
  c=1
  ts=5
  for(var i=0;i<hiddenStates[seqId][4].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][4][i]
  polylines5.push(v);
  c++;
  }

  polylines6=[]
  c=1
  ts=6
  for(var i=0;i<hiddenStates[seqId][5].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][5][i]
  polylines6.push(v);
  c++;
  }

  polylines7=[]
  c=1
  ts=7
  for(var i=0;i<hiddenStates[seqId][6].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][6][i]
  polylines7.push(v);
  c++;
  }

  polylines8=[]
  c=1
  ts=8
  for(var i=0;i<hiddenStates[seqId][7].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][7][i]
  polylines8.push(v);
  c++;
  }

  polylines9=[]
  c=1
  ts=9
  for(var i=0;i<hiddenStates[seqId][8].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][8][i]
  polylines9.push(v);
  c++;
  }

  polylines10=[]
  c=1
  ts=10
  for(var i=0;i<hiddenStates[seqId][9].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][9][i]
  polylines10.push(v);
  c++;
  }

  polylines11=[]
  c=1
  ts=11
  for(var i=0;i<hiddenStates[seqId][10].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][10][i]
  polylines11.push(v);
  c++;
  }

  polylines12=[]
  c=1
  ts=12
  for(var i=0;i<hiddenStates[seqId][11].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][11][i]
  polylines12.push(v);
  c++;
  }

  polylines13=[]
  c=1
  ts=13
  for(var i=0;i<hiddenStates[seqId][12].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][12][i]
  polylines13.push(v);
  c++;
  }

  polylines14=[]
  c=1
  ts=14
  for(var i=0;i<hiddenStates[seqId][13].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][13][i]
  polylines14.push(v);
  c++;
  }

  polylines15=[]
  c=1
  ts=15
  for(var i=0;i<hiddenStates[seqId][14].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][14][i]
  polylines15.push(v);
  c++;
  }

  polylines16=[]
  c=1
  ts=16
  for(var i=0;i<hiddenStates[seqId][15].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][15][i]
  polylines16.push(v);
  c++;
  }

  polylines17=[]
  c=1
  ts=17
  for(var i=0;i<hiddenStates[seqId][16].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][16][i]
  polylines17.push(v);
  c++;
  }

  polylines18=[]
  c=1
  ts=18
  for(var i=0;i<hiddenStates[seqId][17].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][17][i]
  polylines18.push(v);
  c++;
  }

  polylines19=[]
  c=1
  ts=19
  for(var i=0;i<hiddenStates[seqId][18].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][18][i]
  polylines19.push(v);
  c++;
  }

  polylines20=[]
  c=1
  ts=20
  for(var i=0;i<hiddenStates[seqId][19].length;++i){
  var v=[]
  v[0]=c
  v[1]=ts
  v[2]=hiddenStates[seqId][19][i]
  polylines20.push(v);
  c++;
  }
//mini=d3.min(polylines1, function(polylines1){ return polylines1[0][1];})
//console.log(mini)

        
  var margin = {top: 30, right: 30, bottom: 30, left: 30},
    width = 950 - margin.left - margin.right,
    height = 250 - margin.top - margin.bottom;


  var svg = d3.select("svg")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
        


  function range(start, end) {
    return Array(end - start + 1).fill().map((_, idx) => start + idx)
  }
  var myGroups = range(1, 64); // [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
  console.log(myGroups);
  var myVars = range(1, seqlength); // [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
  console.log(myVars);
  
  
  overall=Array.prototype.concat.apply([], [polylines1, polylines2, polylines3,
  polylines4,polylines5,polylines6,polylines7,polylines8,polylines9,polylines10,
  polylines11,polylines12,polylines13,polylines14,polylines15,polylines16,polylines17,
  polylines18,polylines19,polylines20 ]);
  console.log(overall)
  console.log(overall.length)
  
  var x = d3.scaleBand()
    .range([ 0, width ])
    .domain(myGroups)
    .padding(0.001);
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))

  
  var y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(myVars)
    .padding(0.001);
  svg.append("g")
    .call(d3.axisLeft(y));

  
  var myColor = d3.scaleLinear()
    .range(["white", "#b36969"])
    .domain([-1,1])

          // Step 5
      svg.selectAll()
      .data(overall)
      .enter()
      .append("rect")
        .attr("x", function(d) { return x(d[0]) })
        .attr("y", function(d) { return y(d[1]) })
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .style("fill", function(d) { return myColor(d[2])} )

}
}

//code for porjection of tsne
function hiddentsne(seqId){

  console.log(projection.length)
  testsample=testinputs.length
  console.log(testsample)


  //var colors =  ['#e6194b', '#808080', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#3cb44b', '#00007500', '#000000','#ffffff']
  
  var myColor = d3.scaleSequential().domain([0,seqlength])
                  .interpolator(d3.interpolateRdYlGn);

  var colourArray = d3.range((seqlength-1)).map(function(d) {
  return myColor(d)
  });;

  console.log(colourArray)

  var myColor1 = d3.scaleSequential().domain([0,seqlength])
  .interpolator(d3.interpolateRainbow);

  var colourArray1 = d3.range((seqlength)).map(function(d) {
  return myColor1(d)
  });;
  console.log(colourArray1)

  if (seqlength==3)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }
  if (seqlength==5)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }

  if (seqlength==10)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800","#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }

  if (seqlength==20)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800",
  "#0a0800", "#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#FFAA0000", "#00B000"];
  }
  
  console.log(colors1)

  v1=[]
  c=0
  for(var i=0;i<projection.length-1;++i){
  
  if(c==seqlength){c=0}

  v1.push({
            p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
            col: colourArray[c]
            
          });
          c++
  }

  seqid=seqId

  if(seqid==0){
      min=0
      max=(min+seqlength)-1
      console.log(min)
    console.log(max)
  }

  if(seqid!=0){
  min=seqid*seqlength
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }

  if (seqid==testsample-1){
  v2=[]
  scatterpoints=[]
  b=0
  c=0
  console.log(seqid)

  for(var i=min;i<=max;++i){
  
  if(i!=max){
  if(b==seqlength){b=0}
  if(c==seqlength){c=0}
  v2.push({
          p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
          col: colors1[b]
          
        });
        b++
      }
  scatterpoints.push({
    p:[{x:projection[i][0],y:projection[i][1]}],
    col:colourArray1[c]

    })
    c++;
    }
  }

  if (seqid!=testsample-1){
  v2=[]
  scatterpoints=[]
  b=0
  c=0
  for(var i=min;i<=max;++i){
  
  if(b==seqlength){b=0}
  if(c==seqlength){c=0}
  v2.push({
          p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
          col: colors1[b]
          
        });
        b++
  scatterpoints.push({
    x:projection[i][0],
    y:projection[i][1],
    col:colourArray1[c]

    })
    c++;
    }
  }
    
   
  console.log(v1)
  console.log(v2)
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
    
  var linesegment = d3.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .curve(d3.curveLinear); 

  let path1= svg.selectAll('.segment')
           .data(v2)
           .enter().append("path")
           .attr('class','segment')
           .attr('d', function(d) { return linesegment(d.p); })
           .attr('stroke-width', 1)
           .attr('stroke', "none")
           .attr('fill',"none")
           .attr('opacity',"20")
           .attr("shape-rendering", "crispEdges")
    
  function tweenDash() {

    let l = this.getTotalLength(),
        i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }

  path1.transition()
    .duration(200)
    //.delay(function(d, i) { return 5000 * i; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
        
  var lineFunction = d3.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .curve(d3.curveLinear);

  let path= svg.selectAll('.segment')
           .data(v1)
           .enter().append("path")
           .attr('class','segment')
           .attr('d', function(d) { return lineFunction(d.p); })
           .attr('stroke-width', 0.3)
           .attr('stroke', "none")
           .attr('fill',"none")
           .attr('opacity',"0.1")
           .attr("shape-rendering", "crispEdges")
    
  function tweenDash() {

      let l = this.getTotalLength(),
          i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }
    
    
  path.transition()
    .duration(200)
    //.delay(function(d, i) { return i * 200; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
    
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
  
  
  
  if(seqid==0){
  min=0
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }
          
  if(seqid!=0){
  min=seqid*seqlength
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }

  var k=v1[min]
  var klast=v1[max-1]
  console.log(klast)

  var k1=k.p[0]
  var kl=klast.p[1]
  console.log(k1.x)
  console.log(kl)
  
  /**
  svg.append("circle")
    .transition()
    .duration(8000)
    .attr("cx",k1.x )
    .attr("cy", k1.y)
    .attr("r", 0.5)
    
            
  svg.append("circle")
    .transition()
    .duration(8000)
    .attr("cx",kl.x )
    .attr("cy", kl.y)
    .attr("r", 0.5) */
       
}

//clustering algorithm function from HTML
function loadcluster() {


  if((document.getElementById("cluster0").checked) || (document.getElementById("cluster1").checked) || 
  (document.getElementById("cluster2").checked) || (document.getElementById("cluster3").checked) || 
  (document.getElementById("cluster4").checked) || (document.getElementById("cluster5").checked) || 
  (document.getElementById("cluster6").checked) || (document.getElementById("cluster7").checked) || 
  (document.getElementById("cluster8").checked) || (document.getElementById("cluster9").checked) ||
  (document.getElementById("cluster10").checked) || (document.getElementById("cluster11").checked) ||
  (document.getElementById("cluster12").checked) || (document.getElementById("cluster13").checked) ||
  (document.getElementById("cluster14").checked) || (document.getElementById("cluster15").checked) ||
  (document.getElementById("cluster16").checked) || (document.getElementById("cluster17").checked) ||
  (document.getElementById("cluster18").checked) || (document.getElementById("cluster19").checked)){
   
  let checkboxes = document.querySelectorAll('input[name="clus"]:checked');
  let values = [];
  checkboxes.forEach((checkbox) => {
        values.push(checkbox.value);
  });
  console.log(values)
  console.log(typeof(values))
 

  //values.forEach(clusterchange)
  clusterchange(values)
  //function clusterchange(item){
   // console.log(item)
  //}

  }

}

//clustering of each item from forEach fucntion in function loadcluster()
function clusterchange(item){

  console.log(item)

  

  if (item=='c0'){cc=c0}
  if (item=='c1'){cc=c1}
  if (item=='c2'){cc=c2}
  if (item=='c3'){cc=c3}
  if (item=='c4'){cc=c4}
  if (item=='c5'){cc=c5}
  if (item=='c6'){cc=c6} 
  if (item=='c7'){cc=c7}
  if (item=='c8'){cc=c8}
  if (item=='c9'){cc=c9}
  if (item=='c10'){cc=c10}
  if (item=='c11'){cc=c11}
  if (item=='c12'){cc=c12}
  if (item=='c13'){cc=c13}
  if (item=='c14'){cc=c14}
  if (item=='c15'){cc=c15}
  if (item=='c16'){cc=c16}
  if (item=='c17'){cc=c17}
  if (item=='c18'){cc=c18}
  if (item=='c19'){cc=c19}

  if (item=='co0'){cc=co0}
  if (item=='co1'){cc=co1}
  if (item=='co2'){cc=co2}
  if (item=='co3'){cc=co3}
  if (item=='co4'){cc=co4}
  if (item=='co5'){cc=co5}
  if (item=='co6'){cc=co6} 
  if (item=='co7'){cc=co7}
  if (item=='co8'){cc=co8}
  if (item=='co9'){cc=co9}
  if (item=='co10'){cc=co10}
  if (item=='co11'){cc=co11}
  if (item=='co12'){cc=co12}
  if (item=='co13'){cc=co13}
  if (item=='co14'){cc=co14}
  if (item=='co15'){cc=co15}
  if (item=='co16'){cc=co16}
  if (item=='co17'){cc=co17}
  if (item=='co18'){cc=co18}
  if (item=='co19'){cc=co19}


  console.log(cc.length)
  

  console.log(projection.length)
  testsample=testinputs.length
  console.log(testsample)
  /**console.log(c0.length)
  console.log(c1.length)
  console.log(c2.length)
  console.log(c3.length)
  console.log(c4.length)
  console.log(c5.length)
  console.log(c6.length)
  console.log(c7.length)
  console.log(c8.length)
  console.log(c9.length)**/

  var myColor = d3.scaleSequential().domain([0,seqlength])
  //.interpolator(d3.interpolateCool);
  .interpolator(d3.interpolateRdYlGn)

  var colourArray = d3.range((seqlength-1)).map(function(d) {
  return myColor(d)
  });
  
  if (seqlength==3)
  {
    var colors1 =  ["#0a0800", "#0a0800", "#0a080000", "#0a0800", "#0a080000", "#0a0800", "#0a0800",
    "#0a0800", "#0a0800", "#0a080000", "#0a080000"];
  }
  if (seqlength==5)
  {
    var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a080000", "#0a0800", "#0a0800",
    "#0a0800", "#0a0800", "#0a080000", "#0a080000"];
  }
  if (seqlength==10)
  {
    var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800",
    "#0a0800", "#0a0800", "#0a080000", "#0a080000"];
  }
  if (seqlength==20)
  {
    var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800",
    "#0a0800", "#0a0800", "#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a080000"];
  }

  v1=[]
  c=0
  for(var i=0;i<projection.length-1;++i){

  if(c==seqlength){c=0}
  v1.push({
          p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
          col: colourArray[c]
          
        });
        c++
  }

  v2=[]
  b=0
 
  for(var i=0;i<cc.length-1;++i){
 
   
  if(b==seqlength){b=0}
  v2.push({
           p: [{x:cc[i][0],y:cc[i][1]}, {x:cc[i+1][0],y: cc[i+1][1]}],
           col: colors1[b]
           
         });
         b++
       }
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
  
  var linesegment = d3.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .curve(d3.curveLinear); 

  let path1= svg.selectAll('.segment')
          .data(v2)
          .enter().append("path")
          .attr('class','segment')
          .attr('d', function(d) { return linesegment(d.p); })
          .attr('stroke-width', 1)
          .attr('stroke', "none")
          .attr('fill',"none")
          .attr('opacity',"20")
          .attr("shape-rendering", "crispEdges")
  
  function tweenDash() {

    let l = this.getTotalLength(),
        i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }

  path1.transition()
    .duration(50)
    //.delay(function(d, i) { return 5000 * i; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
      
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
          .attr('stroke', "none")
          .attr('fill',"none")
          .attr('opacity',"0.1")
          .attr("shape-rendering", "crispEdges")
  
  function tweenDash() {

      let l = this.getTotalLength(),
          i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }
  
  
  path.transition()
    .duration(50)
    //.delay(function(d, i) { return i * 800; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)


} 
//code for porjection of pca
function hiddenpca(seqId){
  
  var projection=pca_projection 
  console.log(projection.length)
  testsample=testinputs.length
  console.log(testsample)


  var myColor = d3.scaleSequential().domain([0,seqlength])
                  .interpolator(d3.interpolateRdYlGn);

  var colourArray = d3.range((seqlength-1)).map(function(d) {
  return myColor(d)
  });;

  console.log(colourArray)

  var myColor1 = d3.scaleSequential().domain([0,seqlength])
  .interpolator(d3.interpolateRainbow);

  var colourArray1 = d3.range((seqlength)).map(function(d) {
  return myColor1(d)
  });;
  console.log(colourArray1)

  if (seqlength==3)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }
  if (seqlength==5)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }

  if (seqlength==10)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800","#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }

  if (seqlength==20)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800",
  "#0a0800", "#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#FFAA0000", "#00B000"];
  }

  console.log(colors1)

  v1=[]
  c=0
  for(var i=0;i<projection.length-1;++i){

  if(c==seqlength){c=0}

  v1.push({
            p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
            col: colourArray[c]
            
          });
          c++
  }

  seqid=seqId

  if(seqid==0){
      min=0
      max=(min+seqlength)-1
      console.log(min)
    console.log(max)
  }

  if(seqid!=0){
  min=seqid*seqlength
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }

  if (seqid==testsample-1){
  v2=[]
  scatterpoints=[]
  b=0
  c=0
  console.log(seqid)

  for(var i=min;i<=max;++i){

  if(i!=max){
  if(b==seqlength){b=0}
  if(c==seqlength){c=0}
  v2.push({
          p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
          col: colors1[b]
          
        });
        b++
      }
  scatterpoints.push({
    p:[{x:projection[i][0],y:projection[i][1]}],
    col:colourArray1[c]

    })
    c++;
    }
  }

  if (seqid!=testsample-1){
  v2=[]
  scatterpoints=[]
  b=0
  c=0
  for(var i=min;i<=max;++i){

  if(b==seqlength){b=0}
  if(c==seqlength){c=0}
  v2.push({
          p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
          col: colors1[b]
          
        });
        b++
  scatterpoints.push({
    x:projection[i][0],
    y:projection[i][1],
    col:colourArray1[c]

    })
    c++;
    }
  }
    
  
  console.log(v1)
  console.log(v2)
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
    
  var linesegment = d3.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .curve(d3.curveLinear); 

  let path1= svg.selectAll('.segment')
          .data(v2)
          .enter().append("path")
          .attr('class','segment')
          .attr('d', function(d) { return linesegment(d.p); })
          .attr('stroke-width', 1)
          .attr('stroke', "none")
          .attr('fill',"none")
          .attr('opacity',"20")
          .attr("shape-rendering", "crispEdges")
    
  function tweenDash() {

    let l = this.getTotalLength(),
        i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }

  path1.transition()
    .duration(200)
    //.delay(function(d, i) { return 5000 * i; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
        
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
          .attr('stroke', "none")
          .attr('fill',"none")
          .attr('opacity',"0.1")
          .attr("shape-rendering", "crispEdges")
    
  function tweenDash() {

      let l = this.getTotalLength(),
          i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }
    
    
  path.transition()
    .duration(200)
    //.delay(function(d, i) { return i * 200; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
    
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

  if(seqid==0){
  min=0
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }
          
  if(seqid!=0){
  min=seqid*seqlength
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }

  var k=v1[min]
  var klast=v1[max-1]
  console.log(klast)

  var k1=k.p[0]
  var kl=klast.p[1]
  console.log(k1.x)
  console.log(kl)

  /**
  svg.append("circle")
    .transition()
    .duration(8000)
    .attr("cx",k1.x )
    .attr("cy", k1.y)
    .attr("r", 0.5)
    
            
  svg.append("circle")
    .transition()
    .duration(8000)
    .attr("cx",kl.x )
    .attr("cy", kl.y)
    .attr("r", 0.5) */
}


function hiddenzero(seqId){
  console.log(projectiono.length)
  testsample=testinputs.length
  console.log(testsample)
 
  if (seqlength==10){
  for (var i = 0; i < projectiono.length; i++){
    if ( i % 11 == 0) {
      projectiono.splice(i, 1, projectiono[0])
    }}
  console.log(projectiono.length)
  console.log(projectiono[0])
  //seqlength=11
  //seqid=55
  //testsample=300
  var colors =  ["#FF1F5B", "#00CD6C", "#009ADE", "#AF58BA", "#FFC61E", "#F28522", "#A0B1BA",
                                        "#A6761D", "#E9002D", "#FFAA00", "#00B00000","#0a0800"];
  //var colors1 =  ["#0a0800", "#009ADE", "#FF1F5B", "#AF58BA", "#FFC61E", "#F28522", "#A0B1BA",
                                        // "#A6761D", "#E9002D", "#FFAA0000", "#00B000"];
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800",
                                        "#0a0800", "#0a0800", "#0a0800", "#0a080000"];
  /**v1=[]
  c=1
  for(var i=0;i<9;++i){
  var v={}
  v["x"]=projection[i][0]
  v["y"]=projection[i][1]
  v["color"]=colors[i]
  v1.push(v);
  c++;
  }**/
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
  if(seqid==0){
      min=0
      max=(min+seqlength)-1
      console.log(min)
    console.log(max)
    }
    
  if(seqid!=0){
    min=seqid*seqlength
    max=(min+seqlength)-1
    console.log(min)
    console.log(max)
  }
 
  if (seqid==testsample-1){
    v2=[]
    b=0
   console.log(seqid)
   for(var i=min;i<=max;++i){

    if(i!=max){
   if(b==seqlength){b=0}
   v2.push({
            p: [{x:projectiono[i][0],y:projectiono[i][1]}, {x:projectiono[i+1][0],y: projectiono[i+1][1]}],
            col: colors1[b]
            
          });
          b++
        }

  }
  }
  if (seqid!=testsample-1){
  v2=[]
  b=0
  for(var i=min;i<=max;++i){

  if(b==seqlength){b=0}
  v2.push({
            p: [{x:projectiono[i][0],y:projectiono[i][1]}, {x:projectiono[i+1][0],y: projectiono[i+1][1]}],
            col: colors1[b]
            
          });
          b++
  }
  }

  /**var abc = [];
        for (var i = 0; i < xdata.length-1; i++) {
          abc.push({
            p: [{x:xdata[i],y:ydata[i]}, {x:xdata[i+1],y: ydata[i+1]}],
            col: colorvec[i]
          });
        }**/
  console.log(v1)
  console.log(v2)

  d3.select("#tsne").selectAll("circle").remove();


  d3.select("#tsne").selectAll("*").remove();
  var svg = d3.select("#tsne");
  svg.selectAll("*").remove();


  var margin = {top: 20, right: 30, bottom: 40, left: 100},
  width = 500 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;


  var svg = d3.select("#tsne")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + (margin.left+20) + "," + (margin.top+30) + ")");

  var linesegment = d3.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      //.interpolate('linear');
      //.curve(d3.curveStep); 
      .curve(d3.curveLinear);   
        let path1= svg.selectAll('.segment')
    .data(v2)
    .enter().append("path")
    .attr('class','segment')
    .attr('d', function(d) { return linesegment(d.p); })
    //.transition()
      //.delay(1000)
      //.duration(7000)
      //.ease(d3.easeLinear)
      
    .attr('stroke-width', 0.5)
    .attr('stroke', function(d) { return d.col; })
    .attr('fill',"none")
    .attr('opacity',"1")
    .attr("shape-rendering", "crispEdges")

  function tweenDash() {
    let l = this.getTotalLength(),
        i = d3.interpolateString("0," + l, l + "," + l);
    return function(t) { return i(t) };
  }
  path1.transition()
        .duration(3000)
        .ease(d3.easeLinear)
        .attrTween("stroke-dasharray", tweenDash)
      
  var lineFunction = d3.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      //.interpolate('linear');
      //.curve(d3.curveStep); 
      .curve(d3.curveLinear);
      //.curve(d3.curveNatural);
      //.curve(d3.curveMonotoneX);
      

  /**var lineGraph = svg.append("path")
                          .attr("d", lineFunction(v1))
                          .attr("stroke", "violet")
                          .attr("stroke-width", 0.50)
                          .attr("fill", "none");**/
  

      
    let path= svg.selectAll('.segment')
    .data(v1)
    .enter().append("path")
    .attr('class','segment')
    .attr('d', function(d) { return lineFunction(d.p); })
    //.transition()
      //.delay(1000)
      //.duration(7000)
      //.ease(d3.easeLinear)
      
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
        .duration(10000)
        .ease(d3.easeLinear)
        .attrTween("stroke-dasharray", tweenDash)

    var k=v1[0]
    var klast=v1[v1.length-1]
    var k1=k.p[0]
    var kl=klast.p[1]
    console.log(k1.x)
    console.log(kl)

    svg.append("circle")
        .transition()
          .duration(8000)
          .attr("cx",k1.x )
          .attr("cy", k1.y)
          .attr("r", 0.5)
          
          
    svg.append("circle")
      .transition()
        .duration(8000)
          .attr("cx",kl.x )
          .attr("cy", kl.y)
          .attr("r", 0.5)
        }
}

//code for projection of umap
function  hiddenumap(seqId){

  var projection=umap_projection 
  console.log(projection.length)
  testsample=testinputs.length
  console.log(testsample)

  var myColor = d3.scaleSequential().domain([0,seqlength])
                  .interpolator(d3.interpolateRdYlGn);

  var colourArray = d3.range((seqlength-1)).map(function(d) {
  return myColor(d)
  });;

  console.log(colourArray)

  var myColor1 = d3.scaleSequential().domain([0,seqlength])
  .interpolator(d3.interpolateRainbow);

  var colourArray1 = d3.range((seqlength)).map(function(d) {
  return myColor1(d)
  });;
  console.log(colourArray1)

  if (seqlength==3)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }
  if (seqlength==5)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }

  if (seqlength==10)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800","#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }

  if (seqlength==20)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800",
  "#0a0800", "#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#FFAA0000", "#00B000"];
  }

  console.log(colors1)

  v1=[]
  c=0
  for(var i=0;i<projection.length-1;++i){

  if(c==seqlength){c=0}

  v1.push({
            p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
            col: colourArray[c]
            
          });
          c++
  }

  seqid=seqId

  if(seqid==0){
      min=0
      max=(min+seqlength)-1
      console.log(min)
    console.log(max)
  }

  if(seqid!=0){
  min=seqid*seqlength
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }

  if (seqid==testsample-1){
  v2=[]
  scatterpoints=[]
  b=0
  c=0
  console.log(seqid)

  for(var i=min;i<=max;++i){

  if(i!=max){
  if(b==seqlength){b=0}
  if(c==seqlength){c=0}
  v2.push({
          p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
          col: colors1[b]
          
        });
        b++
      }
  scatterpoints.push({
    p:[{x:projection[i][0],y:projection[i][1]}],
    col:colourArray1[c]

    })
    c++;
    }
  }

  if (seqid!=testsample-1){
  v2=[]
  scatterpoints=[]
  b=0
  c=0
  for(var i=min;i<=max;++i){

  if(b==seqlength){b=0}
  if(c==seqlength){c=0}
  v2.push({
          p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
          col: colors1[b]
          
        });
        b++
  scatterpoints.push({
    x:projection[i][0],
    y:projection[i][1],
    col:colourArray1[c]

    })
    c++;
    }
  }
    
  console.log(v1)
  console.log(v2)
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
    
  var linesegment = d3.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .curve(d3.curveLinear); 

  let path1= svg.selectAll('.segment')
          .data(v2)
          .enter().append("path")
          .attr('class','segment')
          .attr('d', function(d) { return linesegment(d.p); })
          .attr('stroke-width', 1)
          .attr('stroke', "none")
          .attr('fill',"none")
          .attr('opacity',"20")
          .attr("shape-rendering", "crispEdges")
    
  function tweenDash() {

    let l = this.getTotalLength(),
        i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }

  path1.transition()
    .duration(200)
    //.delay(function(d, i) { return 5000 * i; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
        
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
          .attr('stroke', "none")
          .attr('fill',"none")
          .attr('opacity',"0.1")
          .attr("shape-rendering", "crispEdges")
    
  function tweenDash() {

      let l = this.getTotalLength(),
          i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }
    
    
  path.transition()
    .duration(200)
    //.delay(function(d, i) { return i * 200; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
    
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

  if(seqid==0){
  min=0
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }
          
  if(seqid!=0){
  min=seqid*seqlength
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }

  var k=v1[min]
  var klast=v1[max-1]
  console.log(klast)

  var k1=k.p[0]
  var kl=klast.p[1]
  console.log(k1.x)
  console.log(kl)

  /**
  svg.append("circle")
    .transition()
    .duration(8000)
    .attr("cx",k1.x )
    .attr("cy", k1.y)
    .attr("r", 0.5)
    
            
  svg.append("circle")
    .transition()
    .duration(8000)
    .attr("cx",kl.x )
    .attr("cy", kl.y)
    .attr("r", 0.5) */

}

//removing repeated code for mds
/** 
function hiddenmds(seqId){
var projection=mds_projection 
    console.log(projection.length)
    testsample=testinputs.length
    console.log(testsample)

var myColor = d3.scaleSequential().domain([0,seqlength])
    .interpolator(d3.interpolateRdYlGn);

var colourArray = d3.range((seqlength-1)).map(function(d) {
return myColor(d)
});;

console.log(colourArray)

var myColor1 = d3.scaleSequential().domain([0,seqlength])
.interpolator(d3.interpolateRainbow);

var colourArray1 = d3.range((seqlength)).map(function(d) {
return myColor1(d)
});;
console.log(colourArray1)

if (seqlength==3)
{
var colors1 =  ["#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
}
if (seqlength==5)
{
var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
}

if (seqlength==10)
{
var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800","#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
}

if (seqlength==20)
{
var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800",
"#0a0800", "#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#FFAA0000", "#00B000"];
}

console.log(colors1)

v1=[]
c=0
for(var i=0;i<projection.length-1;++i){

if(c==seqlength){c=0}

v1.push({
p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
col: colourArray[c]

});
c++
}

seqid=seqId

if(seqid==0){
min=0
max=(min+seqlength)-1
console.log(min)
console.log(max)
}

if(seqid!=0){
min=seqid*seqlength
max=(min+seqlength)-1
console.log(min)
console.log(max)
}

if (seqid==testsample-1){
v2=[]
scatterpoints=[]
b=0
c=0
console.log(seqid)

for(var i=min;i<=max;++i){

if(i!=max){
if(b==seqlength){b=0}
if(c==seqlength){c=0}
v2.push({
p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
col: colors1[b]

});
b++
}
scatterpoints.push({
p:[{x:projection[i][0],y:projection[i][1]}],
col:colourArray1[c]

})
c++;
}
}

if (seqid!=testsample-1){
v2=[]
scatterpoints=[]
b=0
c=0
for(var i=min;i<=max;++i){

if(b==seqlength){b=0}
if(c==seqlength){c=0}
v2.push({
p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
col: colors1[b]

});
b++
scatterpoints.push({
x:projection[i][0],
y:projection[i][1],
col:colourArray1[c]

})
c++;
}
}


console.log(v1)
console.log(v2)
console.log(scatterpoints)

d3.select("#tsne").selectAll("circle").remove();


d3.select("#tsne").selectAll("*").remove();
var svg = d3.select("#tsne");
svg.selectAll("*").remove();


var margin = {top: 20, right: 30, bottom: 40, left: 100},
width = 800 - margin.left - margin.right,
height = 600 - margin.top - margin.bottom;


// append the SVG object to the body of the page
var svg = d3.select("#tsne")
.append("svg")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom)
.append("g")
.attr("transform",
"translate(" + (margin.left+20) + "," + (margin.top+110) + ")");

var linesegment = d3.line()
.x(function(d) { return d.x; })
.y(function(d) { return d.y; })
.curve(d3.curveLinear); 

let path1= svg.selectAll('.segment')
.data(v2)
.enter().append("path")
.attr('class','segment')
.attr('d', function(d) { return linesegment(d.p); })
.attr('stroke-width', 1)
.attr('stroke', "none")
.attr('fill',"none")
.attr('opacity',"20")
.attr("shape-rendering", "crispEdges")

function tweenDash() {

let l = this.getTotalLength(),
i = d3.interpolateString("0," + l, l + "," + l);
return function(t) { return i(t) };
}

path1.transition()
.duration(200)
//.delay(function(d, i) { return 5000 * i; })
.ease(d3.easeLinear)
.attr('stroke', function(d) { return d.col; })
.attrTween("stroke-dasharray", tweenDash)

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
.attr('stroke', "none")
.attr('fill',"none")
.attr('opacity',"0.1")
.attr("shape-rendering", "crispEdges")

function tweenDash() {

let l = this.getTotalLength(),
i = d3.interpolateString("0," + l, l + "," + l);
return function(t) { return i(t) };
}


path.transition()
.duration(200)
//.delay(function(d, i) { return i * 200; })
.ease(d3.easeLinear)
.attr('stroke', function(d) { return d.col; })
.attrTween("stroke-dasharray", tweenDash)

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

if(seqid==0){
min=0
max=(min+seqlength)-1
console.log(min)
console.log(max)
}

if(seqid!=0){
min=seqid*seqlength
max=(min+seqlength)-1
console.log(min)
console.log(max)
}

var k=v1[min]
var klast=v1[max-1]
console.log(klast)

var k1=k.p[0]
var kl=klast.p[1]
console.log(k1.x)
console.log(kl)


svg.append("circle")
.transition()
.duration(8000)
.attr("cx",k1.x )
.attr("cy", k1.y)
.attr("r", 0.5)


svg.append("circle")
.transition()
.duration(8000)
.attr("cx",kl.x )
.attr("cy", kl.y)
.attr("r", 0.5) 
}*/

////animation function from HTML
function loadanimate() {


  if(document.getElementById("animate").checked) 
 {
   
  let checkboxes = document.querySelectorAll('input[name="animate"]:checked');
  let animates = [];
  checkboxes.forEach((checkbox) => {
    animates.push(checkbox.value);
  });
  console.log(animates)
  console.log(typeof(animates))
 

  animates.forEach(animate)

  //function clusterchange(item){
   // console.log(item)
  //}

  }

}

//this fucntion animates the overall tsne projection
function animate(seqId){

  console.log(projection.length)
  testsample=testinputs.length
  console.log(testsample)


  //var colors =  ['#e6194b', '#808080', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#3cb44b', '#00007500', '#000000','#ffffff']
  
  var myColor = d3.scaleSequential().domain([0,seqlength])
                  //.interpolator(d3.interpolateCool);
                  .interpolator(d3.interpolateRdYlGn)

  var colourArray = d3.range((seqlength-1)).map(function(d) {
  return myColor(d)
  });;

  console.log(colourArray)

  if (seqlength==3)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }
  if (seqlength==5)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }

  if (seqlength==10)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800","#0a0800", "#0a0800", "#FFAA0000", "#00B000"];
  }

  if (seqlength==20)
  {
  var colors1 =  ["#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800", "#0a0800",
  "#0a0800", "#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800", "#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#0a0800","#FFAA0000", "#00B000"];
  }
  
  console.log(colors1)

  v1=[]
  c=0
  for(var i=0;i<projection.length-1;++i){
  
  if(c==seqlength){c=0}

  v1.push({
            p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
            col: colourArray[c]
            
          });
          c++
  }

  seqid=seqId

  if(seqid==0){
      min=0
      max=(min+seqlength)-1
      console.log(min)
    console.log(max)
  }

  if(seqid!=0){
  min=seqid*seqlength
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }

  if (seqid==testsample-1){
  v2=[]
  b=0
  console.log(seqid)

  for(var i=min;i<=max;++i){
  
  if(i!=max){
  if(b==seqlength){b=0}
  v2.push({
          p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
          col: colors1[b]
          
        });
        b++
      }
  }
  }

  if (seqid!=testsample-1){
  v2=[]
  b=0
  for(var i=min;i<=max;++i){
  
  if(b==seqlength){b=0}
  v2.push({
          p: [{x:projection[i][0],y:projection[i][1]}, {x:projection[i+1][0],y: projection[i+1][1]}],
          col: colors1[b]
          
        });
        b++
  }
  }
    
   
  console.log(v1)
  console.log(v2)

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
    
  var linesegment = d3.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .curve(d3.curveLinear); 

  let path1= svg.selectAll('.segment')
           .data(v2)
           .enter().append("path")
           .attr('class','segment')
           .attr('d', function(d) { return linesegment(d.p); })
           .attr('stroke-width', 1)
           .attr('stroke', "none")
           .attr('fill',"none")
           .attr('opacity',"20")
           .attr("shape-rendering", "crispEdges")
    
  function tweenDash() {

    let l = this.getTotalLength(),
        i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }

  path1.transition()
    .duration(1000)
    .delay(function(d, i) { return 1000 * i; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
        
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
           .attr('stroke', "none")
           .attr('fill',"none")
           .attr('opacity',"0.5")
           .attr("shape-rendering", "crispEdges")
    
  function tweenDash() {

      let l = this.getTotalLength(),
          i = d3.interpolateString("0," + l, l + "," + l);
      return function(t) { return i(t) };
  }
    
    
  path.transition()
    .duration(200)
    .delay(function(d, i) { return i * 200; })
    .ease(d3.easeLinear)
    .attr('stroke', function(d) { return d.col; })
    .attrTween("stroke-dasharray", tweenDash)
    
 
  if(seqid==0){
  min=0
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }
          
  if(seqid!=0){
  min=seqid*seqlength
  max=(min+seqlength)-1
  console.log(min)
  console.log(max)
  }

  var k=v1[min]
  var klast=v1[max-1]
  console.log(klast)

  var k1=k.p[0]
  var kl=klast.p[1]
  console.log(k1.x)
  console.log(kl)
    
  svg.append("circle")
    .transition()
    .duration(8000)
    .attr("cx",k1.x )
    .attr("cy", k1.y)
    .attr("r", 0.5)
    
            
  svg.append("circle")
    .transition()
    .duration(8000)
    .attr("cx",kl.x )
    .attr("cy", kl.y)
    .attr("r", 0.5)
       
}

//this function shows all the sactterpoints
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

  console.log(projection.length)
  testsample=testinputs.length
  console.log(testsample)
 
  var myColor1 = d3.scaleSequential().domain([0,seqlength])
  .interpolator(d3.interpolateRainbow);

  var colourArray1 = d3.range((seqlength)).map(function(d) {
    return myColor1(d)
    });;

  console.log(colourArray1)
  scatterpoints=[]
  c=0
  for(var i=0;i<projection.length-1;++i){
  
  if(c==seqlength){c=0}


  scatterpoints.push({
    x:projection[i][0],
    y:projection[i][1],
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