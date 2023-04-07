function getTrendByBlock(block) {
    d3.json(BlockTrendUrl).then(function(data) {
    genBlockTrend(data[block],'#time_trend');
    });
}

function toggle(el){
    var value = el.options[el.selectedIndex].value;
    getTrendByBlock(value);
}


function barChart(jsonData, selectedId, yScaleDomain) {
    d3.json(jsonData).then(function(data) {
        const margin = {top: 35, right: 35, bottom: 35, left: 35},
              width = 600 - margin.left - margin.right,
              height = 350 - margin.top - margin.bottom,
              svg = d3.select(selectedId)
                      .append("svg")
                      .attr("width", width + margin.left + margin.right)
                      .attr("height", height + margin.top + margin.bottom)
                      .append("g")
                      .attr("transform", `translate(${margin.left}, ${margin.top})`);
        const yScale = d3.scaleLinear()
                         .range([height, 0])
                         .domain(yScaleDomain);
        const xScale = d3.scaleBand()
                         .range([0, width])
                         .domain(data.map((d) => d.start))
                         .padding(0.1);
        svg.append('g')
           .call(d3.axisLeft(yScale));
        svg.append('g')
           .attr('transform', `translate(0, ${height})`)
           .call(d3.axisBottom(xScale));
        svg.append('g')
           .attr('class', 'grid')
           .attr('opacity', 0.5)
           .call(d3.axisLeft()
                   .scale(yScale)
                   .tickSize(-width, 0, 0)
                   .tickFormat(''));
        svg.selectAll()
           .data(data)
           .enter()
           .append('rect')
           .style('fill', 'green')
           .attr('x', (s) => xScale(s.start))
           .attr('y', (s) => yScale(s.duration))
           .attr('height', (s) => height - yScale(s.duration))
           .attr('width', xScale.bandwidth());
        svg.selectAll()
           .data(data)
           .enter()
           .append('text')
           .style("font-size", 12)
           .attr('class', 'divergence')
           .attr('x', (a) => xScale(a.start) + xScale.bandwidth() / 2)
           .attr('y', (a) => yScale(a.duration) + 30)
           .attr('fill', 'white')
           .attr('text-anchor', 'middle')
           .text((a) => a.duration);


    })
}

function genHeatMap(jsonData, selectedId, colorsRange) {
d3.json(jsonData).then(function(data) {
const margin = {top: 35, right: 35, bottom: 35, left: 35},
      width = 550 - margin.left - margin.right,
      height = 350 - margin.top - margin.bottom,
      svg = d3.select(selectedId)
              .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);
  // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
  const points = ['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q']

  // Build X scales and axis:
  const x = d3.scaleBand()
    .range([ 0, width ])
    .domain(points)
    .padding(0.02);
  svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "middle")
    .attr("x", width/2)
    .attr("y", height + margin.bottom)
    .text("TO")
  svg.append("g")
    .style("font-size", 12)
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x).tickSize(0))
    .select(".domain").remove()


  // Build Y scales and axis:
  const y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(points)
    .padding(0.02);
  svg.append("text")
    .attr("class", "y label")
    .attr("text-anchor", "middle")
    .attr("x", -height/2)
    .attr("y", -margin.left)
    .attr("dy", ".75em")
    .attr("transform", "rotate(-90)")
    .text("FROM");
  svg.append("g")
    .style("font-size", 12)
    .call(d3.axisLeft(y).tickSize(0))
    .select(".domain").remove()

  // Build color scale
  const myColor = d3.scaleSequential()
    .interpolator(d3.interpolateRdYlGn)
    .domain(colorsRange)

  // create a tooltip
  const tooltip = d3.select(selectedId)
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
}

function genBlockTrend(data, selectedId) {
    d3.select(selectedId).selectAll("*").remove();
    var margin = {top: 35, right: 35, bottom: 35, left: 35},
            width = 1000 - margin.left - margin.right,
            height = 400 - margin.top - margin.bottom,
            svg = d3.select(selectedId)
                    .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")"),
            x = d3.scaleTime().range([0, width]),
            y = d3.scaleLinear().range([height, 0]),
            parseDate = d3.utcParse("%Y-%m-%d"),
            formatDate = d3.timeFormat("%d-%m"),
            lineMean = d3.line()
                         .x(function(d) { return x(d.date); })
                         .y(function(d) { return y(d.mean); }),
            lineQ1 = d3.line()
                       .x(function(d) { return x(d.date); })
                       .y(function(d) { return y(d.q1); }),
            lineQ3 = d3.line()
                       .x(function(d) { return x(d.date); })
                       .y(function(d) { return y(d.q3); });



        data.forEach(function(d) {
        d.date = parseDate(d.date);
        d.mean = +d.mean;
        d.q1 = +d.q1;
        d.q3 = +d.q3;
        });



        // Scale the range of the data
        x.domain(d3.extent(data, function(d) {  return d.date; }));
        y.domain([d3.min(data, function(d) {  return d.q1; })-0.5, d3.max(data, function(d) {  return d.q3; })]);

        // Add the x axis
        svg.append("g")
           .attr("class", "x axis")
           .attr("transform", "translate(0," + height + ")")
           .call(d3.axisBottom(x).ticks(d3.timeWeek.every(2)));

        // Add the y axis
        svg.append("g")
           .attr("class", "y axis")
           .call(d3.axisLeft(y));

        svg.append("path")
           .datum(data)
           .attr("fill", "none")
           .attr("stroke", "steelblue")
           .style("stroke-dasharray", ("3, 3"))
           .attr("stroke-width", 1)
           .attr("d", lineQ3);
        svg.append("path")
           .datum(data)
           .attr("fill", "none")
           .attr("stroke", "steelblue")
           .style("stroke-dasharray", ("3, 3"))
           .attr("stroke-width", 1)
           .attr("d", lineQ1);
        svg.append("path")
           .datum(data)
           .attr("fill", "none")
           .attr("stroke", "steelblue")
           .attr("stroke-width", 1.5)
           .attr("d", lineMean);}