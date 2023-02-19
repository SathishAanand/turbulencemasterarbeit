function createTable(data) {
    // modified from http://bl.ocks.org/AMDS/4a61497182b8fcb05906
    var sortAscending = true;
    var table = d3.select('#page-wrap').append('table');
    var titles = Object.keys(data[0]);
    var headers = table.append('thead').append('tr')
                    .selectAll('th')
                    .data(titles).enter()
                    .append('th')
                    .text(function (d) {
                         return d;
                    })
                    

    var rows = table.append('tbody').selectAll('tr')
                    .data(data).enter()
                    .append('tr');
    rows.on('click', function (d) {
        if (this.id == 'selectedRow') {
            rows.attr('class', 'row');
            rows.attr('id', null);
            hideSequences();
        }
        else {
            rows.attr('class', 'row');
            rows.attr('id', null);
            this.className = 'selectedRow';
            this.id = 'selectedRow';
            showSequence(d["Id"]);
        }
    });
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