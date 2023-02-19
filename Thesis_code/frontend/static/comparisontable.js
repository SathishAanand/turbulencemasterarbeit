function createTable(data) {
    // modified from http://bl.ocks.org/AMDS/4a61497182b8fcb05906
    var sortAscending = true;
    var dummy = d3.select(data[data.length-1])
    var table = dummy.append('table');
    var titles = Object.keys(data[0]);
    var headers = table.append('thead').append('tr')
                    .selectAll('th')
                    .data(titles).enter()
                    .append('th')
                    .text(function (d) {
                            return d;
                    });
            

    var rows = table.append('tbody').selectAll('tr')
                    .data(data).enter()
                    .append('tr');

    rows.selectAll('td')
        .data(function (d) {
            return titles.map(function (k) {
                return { 'value': d[k], 'name': k};
            });
        }).enter()
        .append('td')
        .attr('data-th', function (d) {
            return d.name;
        })
        .text(function (d) {
            return d.value;
        });
}

    