<script>
var color = d3.scale.category10();

var width = 800,
    height = 500;

var canvas = d3.select("resultados").append("svg")
    .attr("width", width)
    .attr("height", height)


d3.json("{% static 'agora/json/p5_json_temas_subtemas.json' %}", function (data) {

    var treemap = d3.layout.treemap()
        .size([width, height])
        .nodes(data)

    var parents = treemap.filter(function (d) {
        return d.children;
    });

    var cells = canvas.selectAll("g")
        .data(treemap)
        .enter()
        .append("g")
        .attr("class", "cell")


    cells.append("rect")
        .attr("x", function (d) { return d.x; })
        .attr("y", function (d) { return d.y; })
        .attr("width", function (d) { return d.dx; })
        .attr("height", function (d) { return d.dy; })
        .attr("fill", function (d) { return d.children ? null : color(d.parent.name); })
        .attr("stroke", "#fff")
        .attr("ident", function (d) { return d.children ? null : d.parent.name + ' ' + d.parent.size + '%' })


    cells.append("text")
        .attr("x", function (d) { return d.x + d.dx / 2 })
        .attr("y", function (d) { return d.y + d.dy / 2 })
        .attr("text-anchor", "middle")
        .text(function (d) { return d.name + "\n\r" + d.size + '%' })


    var i;
    parents_list = []
    for (i = 0; i < parents.length; i++) {
        parents_list.push(parents[i].name)
    }

    cores_distintas = []
    cores_distintas_test = []
    d3.selectAll("rect").each(function (d) {
        var b = d3.select(this).attr("fill")
        var a = d3.select(this).attr("ident")

        if (cores_distintas_test.indexOf(b) >= 0) {
            console.log(b)
        } else {
            if (a) {
                var tuple = [b, a]
                cores_distintas.push(tuple)
                cores_distintas_test.push(b)
            }
        }

    })

    var legenda = d3.select("#legend")
        .selectAll('div')
        .data(cores_distintas)

    legenda.enter('div')
        .append('div')
        .style("position", "relative")
        .style("width", 200 + "px")
        .style("height", 30 + "px")
        .style("background", function (d) { { return d[0] } })
        .style("text-align", "center")
        .style("vertical-align", "middle")
        .style("color", "black")
        .style("line-height", "30px");

    legenda.append("text")
        .text(function (d) { { return d[1] } })
});

</script>
