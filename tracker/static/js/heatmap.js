    // set the dimensions and margins of the graph
const margin = {top: 35, right: 35, bottom: 35, left: 35},
  width = 650 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

//Read the data
d3.json(data_url).then(function(data) {

  // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
  const points = ['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22']

  // Build X scales and axis:
  const x = d3.scaleBand()
    .range([ 0, width ])
    .domain(points)
    .padding(0.05);
  svg.append("g")
    .style("font-size", 8)
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x).tickSize(0))
    .select(".domain").remove()

  // Build Y scales and axis:
  const y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(points)
    .padding(0.05);
  svg.append("g")
    .style("font-size", 8)
    .call(d3.axisLeft(y).tickSize(0))
    .select(".domain").remove()

  // Build color scale
  const myColor = d3.scaleSequential()
    .interpolator(d3.interpolateRdYlGn)
    .domain([-2,0])

  // create a tooltip
  const tooltip = d3.select("#my_dataviz")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

  // Three function that change the tooltip when user hover / move / leave a cell
  const mouseover = function(event,d) {
    tooltip
      .style("opacity", 1)
    d3.select(this)
      .style("stroke", "black")
      .style("opacity", 1)
  }
  const mousemove = function(event,d) {
    tooltip
      .html("Transition 'from -> to': " + d.start + " -> " + d.end + "<br>Average time executed: " + d.duration + "s")
      .style("left", (event.x) + "px")
      .style("top", (event.y) + "px")
  }
  const mouseleave = function(event,d) {
    tooltip
      .style("opacity", 0)
    d3.select(this)
      .style("stroke", "none")
      .style("opacity", 0.8)
  }

  // add the squares
  svg.selectAll()
    .data(data, function(d) {return d.start+':'+d.end;})
    .join("rect")
      .attr("x", function(d) { return x(d.end) })
      .attr("y", function(d) { return y(d.start) })
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { return myColor(-d.duration)} )
      .style("stroke-width", 4)
      .style("stroke", "none")
      .style("opacity", 0.8)
    .on("mouseover", mouseover)
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)
})