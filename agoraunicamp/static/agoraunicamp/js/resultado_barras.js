var res = "{% static 'agoraunicamp/data.json' %}"; 

d3.json(res, function (error, data) {
    var chartDiv = document.getElementById("chart{{relatorio.pk}}")

    var margin = { top: 30, right: 10, bottom: 100, left: 35 },
            width = chartDiv.clientWidth - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1, .3);

    var y = d3.scale.linear()
            .range([height, 0]);

    var test = d3.select("#chart{{relatorio.pk}}").append("div")
            .text("{{relatorio.questao.question_text}}")
            .style('text-align', 'center')
            .style('font-weight', 'bold');


    var svg = d3.select("#chart{{relatorio.pk}}").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .style('display', 'block')
            .style('margin', '0 auto')
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");



    var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

    var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(8, "%");

    var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function (d) {
                    return "<strong>" + d.value + "%</strong><span style='color:red'></span>";
            })
    svg.call(tip);

    x.domain(data.map(function (d) { return d.name; }));
    y.domain([0, d3.max(data, function (d) { return d.value; })]);


    svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .selectAll(".tick text")
            .call(wrap, x.rangeBand());



    svg.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function (d) { return x(d.name); })
            .attr("width", x.rangeBand())
            .attr("y", function (d) { return y(d.value); })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide)
            .attr("height", function (d) { return height - y(d.value); });

});

function wrap(text, width) {
    text.each(function () {
            var text = d3.select(this),
                    words = text.text().split(/\s+/).reverse(),
                    word,
                    line = [],
                    lineNumber = 0,
                    lineHeight = 1.1, // ems
                    y = text.attr("y"),
                    dy = parseFloat(text.attr("dy")),
                    tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
            while (word = words.pop()) {
                    line.push(word);
                    tspan.text(line.join(" "));
                    if (tspan.node().getComputedTextLength() > width) {
                            line.pop();
                            tspan.text(line.join(" "));
                            line = [word];
                            tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
                    }
            }
    });
}
function type(d) {
    d.value = +d.value;
    return d;
}