
function drawNetwork(json_file){
  $.get(json_file,
     function(data) {
       console.log(data);
       loadCytoGraph(data);
       $("#cy").cy(function(){
         $("#cy").cytoscapePanzoom();
       });

     }, "json");
}

function loadCytoGraph(xylem_all){

  $("#cy").cytoscape({
    layout: {
      name: 'preset',
      fit: true,
   },

   style: cytoscape.stylesheet()
      .selector('node')
        .css({
          'shape': 'data(faveShape)',
          'height': 'data(h)',
          'width': 'data(w)',
          'content': 'data(name)',
          'text-valign': 'center',
          'text-outline-width': 2,
          'text-outline-color': '#000000',
          'background-color': 'data(faveColor)',
          'color': '#fff'
        })
      .selector(':selected')
        .css({
          'border-width': 3,
          'border-color': '#333'
        })
      .selector('edge')
        .css({
          'width': 'data(line-width)',
          'target-arrow-shape': 'data(targetArrowShape)',
          'source-arrow-shape': 'data(sourceArrowShape)',
          'line-color': 'data(faveColor)',
          'source-arrow-color': 'data(faveColor)',
          'target-arrow-color': 'data(faveColor)',
          'line-style': 'data(lineStyle)'
        })
      .selector('.faded')
        .css({
          'opacity': 0.25,
          'text-opacity': 0
        }),

    elements: xylem_all,


    ready: function(){
      window.cy = this;
      window.cy.resize();

      var csv_output;

      function highlightNetwork(node){
        //fade all genes not assocated with selected node
          var neighborhood = node.neighborhood().add(node);
          cy.elements().addClass('faded');
          neighborhood.removeClass('faded'); }
      function isEven(value) {
        if (value%2 == 0)
          return true;
        else
          return false;
       }


      function loadGeneName(node){
        //find name of selected node and display in gene_name tag
        var gene_name = (node.element().data().name);
        var neighborhood = node.neighborhood();
        csv_output = gene_name + "\n";
        $.each(neighborhood, function(i,n) {
          if (isEven(i)) {
                var ele = n.element().data();
                //console.log(ele.name,i );
                csv_output += ele.name + "," + ele.node_type + "\n"
          }   
         });
        console.log(csv_output);
   

      $('#gene_name').html(gene_name); }

      $('#search-box').keyup(function(){
        // highlight the gene entered in the search box and displays it in the key
        var gene_name = $(this).val();
        if (gene_name == 'Enter Gene Name'){
          return }
          // if default text function stops here
        else if (gene_name == ''){
          cy.elements().removeClass('faded')}
          // if no text function removes the faded class from all genes
        else {
          var node = cy.elements("node[name='"+ gene_name.toUpperCase() + "']");
          highlightNetwork(node);
          loadGeneName(node);
        }
        }).keyup();

      cy.elements().unselectify();
      
      cy.on('tap', 'node', function(e){
        // when click on the gene highlights other connected genes and loads in key
        var node = e.cyTarget;
        highlightNetwork(node);
        loadGeneName(node);
       });


      cy.on('tap', function(e){
        // when tap background removed fadedness from all genes
        if( e.cyTarget === cy ){
          cy.elements().removeClass('faded');
            }
      });

     $("#csv_output").click(function(){ SaveasTXT(csv_output);});

      function SaveasTXT(element,gene_name) {
        if (typeof element == "string"){
          var csvContent = "data:text/csv;charset=utf-8," + encodeURIComponent(element); 
          console.log(csvContent,gene_name)
          var link = document.createElement("a");
          var gene_name = element.split("\n")[0]
          var y = link.setAttribute("href", csvContent); link.setAttribute("download", gene_name + "_interactions.csv");
          var x = link.click();
        }
      };
    }
  });
}


console.log("end");
