// current sequence
var currentSequence = -1;
//This fucntion is to initiate the selected dataset
function init() {
  currentSequence = -1;
  document.getElementsByName("datasets1")[0].selectedIndex = "0";
  document.getElementsByName("datasets2")[0].selectedIndex = "0";
  }
//This fucntion is to load data set from json file
function compareData() {
  currentSequence = -1;
  d3.select("#selectedRow").attr("class", "row");

  //var parameters1 = {
    //"dataset1": document.getElementsByName("datasets1")[0].value
  //};
  //var parameters2 = {
  //  "dataset2": document.getElementsByName("datasets2")[0].value
  //};
  var data ={
      "dataset1": document.getElementsByName("datasets1")[0].value,
      "dataset2": document.getElementsByName("datasets2")[0].value
  }

  //console.log(parameters1)
  //console.log(parameters2)
  console.log(data)

  var request = new XMLHttpRequest();
  request.open('POST', '/comparing', false);
  request.setRequestHeader("Content-Type", "application/json");
  request.send(JSON.stringify(data));
  
  
  var content = JSON.parse(request.responseText.trim());
  console.log(content)

  seqlengthfloat1 = content["seqlength1"];
  time_increment1 = content["time_increment1"];
  accuracy1 = content["accuracy1"];
  hiddenStates1 = content["hiddenStatesgru1"];
  gruweights1 = content["gruweights1"];
  zerohidden1=content["zerohidden1"];
  hiddenStatesreshape1 = content["hiddenStatesreshape1"];
  hiddenstateo1 = content["hiddenstateo1"];
  testinputs1 = content["testinputs1"];
  actualValues1 = content["actualValues1"];
  predictions1 = content["predictions1"];
  pca_projection1 = content["pcaprojection1"];
  projection1 = content["projection1"];
  nfeatures1=content["nfeatures1"];
  projectiono1 = content["projectiono1"];
  //mds_projection1 = content1["mdsprojection1"];
  umap_projection1 = content["umapprojection1"];


  c01=content["c01"];
  c11=content["c11"];
  c21=content["c21"];
  c31=content["c31"];
  c41=content["c41"];
  c51=content["c51"];
  c61=content["c61"];
  c71=content["c71"];
  c81=content["c81"];
  c91=content["c91"];
  c101=content["c101"];
  c111=content["c111"];
  c121=content["c121"];
  c131=content["c131"];
  c141=content["c141"];
  c151=content["c151"];
  c161=content["c161"];
  c171=content["c171"];
  c181=content["c181"];
  c191=content["c191"];

  co01=content["co01"];
  co11=content["co11"];
  co21=content["co21"];
  co31=content["co31"];
  co41=content["co41"];
  co51=content["co51"];
  co61=content["co61"];
  co71=content["co71"];
  co81=content["co81"];
  co91=content["co91"];
  co101=content["co101"];
  co111=content["co111"];
  co121=content["co121"];
  co131=content["co131"];
  co141=content["co141"];
  co151=content["co151"];
  co161=content["co161"];
  co171=content["co171"];
  co181=content["co181"];
  co191=content["co191"];


  seqlengthfloat2 = content["seqlength2"];
  time_increment2 = content["time_increment2"];
  accuracy2 = content["accuracy2"];
  hiddenStates2 = content["hiddenStatesgru2"];
  gruweights2 = content["gruweights2"];
  zerohidden2=content["zerohidden2"];
  hiddenStatesreshape2 = content["hiddenStatesreshape2"];
  hiddenstateo2 = content["hiddenstateo2"];
  testinputs2 = content["testinputs2"];
  actualValues2 = content["actualValues2"];
  predictions2 = content["predictions2"];
  pca_projection2 = content["pcaprojection2"];
  projection2 = content["projection2"];
  nfeatures2=content["nfeatures2"];
  projectiono2 = content["projectiono2"];
  //mds_projection2 = content["mdsprojection2"];
  umap_projection2 = content["umapprojection2"];


  c02=content["c02"];
  c12=content["c12"];
  c22=content["c22"];
  c32=content["c32"];
  c42=content["c42"];
  c52=content["c52"];
  c62=content["c62"];
  c72=content["c72"];
  c82=content["c82"];
  c92=content["c92"];
  c102=content["c102"];
  c112=content["c112"];
  c122=content["c122"];
  c132=content["c132"];
  c142=content["c142"];
  c152=content["c152"];
  c162=content["c162"];
  c172=content["c172"];
  c182=content["c182"];
  c192=content["c192"];

  co02=content["co02"];
  co12=content["co12"];
  co22=content["co22"];
  co32=content["co32"];
  co42=content["co42"];
  co52=content["co52"];
  co62=content["co62"];
  co72=content["co72"];
  co82=content["co82"];
  co92=content["co92"];
  co102=content["co102"];
  co112=content["co112"];
  co122=content["co122"];
  co132=content["co132"];
  co142=content["co142"];
  co152=content["co152"];
  co162=content["co162"];
  co172=content["co172"];
  co182=content["co182"];
  co192=content["co192"];

  
  
  seqlength1=Math.floor(seqlengthfloat1)
  seqlength2=Math.floor(seqlengthfloat2)
  

  document.getElementById("handle3").checked = "checked";
    
  showDataInfo1(-1);
  showDataInfo2(-1);

  var sentenceOverview1 = [];
  for (var i = 0; i < actualValues1.length; ++i) {
    sentenceOverview1.push({
    "Id":i,
    "Original end values closure terms":actualValues1[i],
    "Predicted values closure terms":predictions1[i],
    "Error between closure terms":Math.sqrt((Math.pow((actualValues1[i][0]-predictions1[i][0]),2))+
      (Math.pow((actualValues1[i][1]-predictions1[i][1]),2))+
      (Math.pow((actualValues1[i][2]-predictions1[i][2]),2))),
      "Sequence of Inputs with velocities": testinputs1[i]
    });
  }
  
  //console.log(sentenceOverview1)

  var sentenceOverview2 = [];
  for (var i = 0; i < actualValues2.length; ++i) {
    sentenceOverview2.push({
    "Id":i,
    "Original end values closure terms":actualValues2[i],
    "Predicted values closure terms":predictions2[i],
    "Error between closure terms":Math.sqrt((Math.pow((actualValues2[i][0]-predictions2[i][0]),2))+
      (Math.pow((actualValues2[i][1]-predictions2[i][1]),2))+
      (Math.pow((actualValues2[i][2]-predictions2[i][2]),2))),
      "Sequence of Inputs with velocities": testinputs2[i]
    });
  }
  
  //onsole.log(sentenceOverview2)

  //d3.select('#page-wrap1').selectAll("*").remove();
  //d3.select('#page-wrap2').selectAll("*").remove();
  //sentenceOverview1.push('#page-wrap1');
  //sentenceOverview2.push('#page-wrap2');
  //createTable(sentenceOverview1);
  //createTable(sentenceOverview2);
  hiddentsneload1()
  hiddentsneload2()
  
}

function showDataInfo1(seqId) {

  var id = "dataInfo1";
  var idSeq1 = "dataInfoSeqs1";
  var idAcc1 = "dataInfoAcc1";
  var idts1 = "dataInfots1";
  var idinc1 = "dataInfoinc1";
  var nf1 = "datanfeatures1";

  d3.select("#" + id).selectAll("*").remove();

  var dataInfoContainer = d3.select("#" + id + "Container");
  if (seqId >= 0) {
      dataInfoContainer.style("display", "none");
      return;
  }

  dataInfoContainer.style("display", "block");
  console.log(nf1)

  //var dataInfoElement = document.getElementById(id);
    
  document.getElementById(idSeq1).innerHTML = testinputs1.length;
  document.getElementById(idAcc1).innerHTML = accuracy1;
  document.getElementById(idts1).innerHTML = seqlength1;
  document.getElementById(idinc1).innerHTML = time_increment1;
  document.getElementById(nf1).innerHTML = nfeatures1;
  
}

function showDataInfo2(seqId) {

  var id2 = "dataInfo2";
  var idSeq2 = "dataInfoSeqs2";
  var idAcc2 = "dataInfoAcc2";
  var idts2 = "dataInfots2";
  var idinc2 = "dataInfoinc2";
  var nf2 = "datanfeatures2";

  d3.select("#" + id2).selectAll("*").remove();

  var dataInfoContainer2 = d3.select("#" + id2 + "Container");
  if (seqId >= 0) {
      dataInfoContainer2.style("display", "none");
      return;
  }

  dataInfoContainer2.style("display", "block");
  console.log(nf2)
  //var dataInfoElement = document.getElementById(id);
    
  document.getElementById(idSeq2).innerHTML = testinputs2.length;
  document.getElementById(idAcc2).innerHTML = accuracy2;
  document.getElementById(idts2).innerHTML = seqlength2;
  document.getElementById(idinc2).innerHTML = time_increment2;
  document.getElementById(nf2).innerHTML = nfeatures2;
}


//This fucntion loads the overall tsne projection when the dataset1 is loaded 
function hiddentsneload1(){

  console.log(projection1.length)
  testsample1=testinputs1.length
  console.log(testsample1)

  var myColor = d3.scaleSequential().domain([0,seqlength1])
                  .interpolator(d3.interpolateRdYlGn);

  var colourArray = d3.range((seqlength1-1)).map(function(d) {
  return myColor(d)
  });;

  console.log(colourArray)


  v1=[]
  c=0
  for(var i=0;i<projection1.length-1;++i){
  
  if(c==seqlength1){c=0}

  v1.push({
            p: [{x:projection1[i][0],y:projection1[i][1]}, {x:projection1[i+1][0],y: projection1[i+1][1]}],
            col: colourArray[c]
            
          });
          c++
  }

  console.log(v1)
  
  d3.select("#tsne1").selectAll("circle").remove();

  d3.select("#tsne1").selectAll("*").remove();
  var svg = d3.select("#tsne1");
  svg.selectAll("*").remove();
   
    
  var margin = {top: 20, right: 30, bottom: 40, left: 100},
  width = 500 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;
    
    
  var svg = d3.select("#tsne1")
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
           .attr('stroke-width', 0.5)
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
//end of tsne load1

//This fucntion loads the overall tsne projection when the dataset2 is loaded 
function hiddentsneload2(){

  console.log(projection2.length)
  testsample2=testinputs2.length
  console.log(testsample2)

  var myColor = d3.scaleSequential().domain([0,seqlength2])
                  .interpolator(d3.interpolateRdYlGn);

  var colourArray = d3.range((seqlength2-1)).map(function(d) {
  return myColor(d)
  });;

  console.log(colourArray)


  v1=[]
  c=0
  for(var i=0;i<projection2.length-1;++i){
  
  if(c==seqlength2){c=0}

  v1.push({
            p: [{x:projection2[i][0],y:projection2[i][1]}, {x:projection2[i+1][0],y: projection2[i+1][1]}],
            col: colourArray[c]
            
          });
          c++
  }

  console.log(v1)
  
  d3.select("#tsne2").selectAll("circle").remove();

  d3.select("#tsne2").selectAll("*").remove();
  var svg = d3.select("#tsne2");
  svg.selectAll("*").remove();
   
    
  var margin = {top: 20, right: 30, bottom: 40, left: 100},
  width = 500 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;
    
  var svg = d3.select("#tsne2")
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
           .attr('stroke-width', 0.5)
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
//end of tsne2 load