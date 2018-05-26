var canvas = d3.select("#chart_p8").append("svg")
        .attr("width", 500)
        .attr("height", 500)
        .append("g")
        .attr("transform", "translate(50, 50)");

var tree = d3.layout.tree()

d3.json(p8_data, function (data){

        var node = tree.nodes(data)
        console.log(nodes)
})