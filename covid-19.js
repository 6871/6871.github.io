function loadGraph(graphDivFile, graphTitle, documentTitle) {
    $('#title').html(graphTitle);
    let graph_div = $('#graph');
    graph_div.fadeOut('slow');
    graph_div.html('<div class="loading"><div class="spinner"></div></div>');
    graph_div.fadeIn().load(graphDivFile);
    $('#timestamp').load('./update_timestamp.txt');
    document.title = documentTitle
}

$(document).ready(function(){
    let btn_0_avg = $('#btn_0_avg');

    btn_0_avg.click(function(){
        loadGraph(
            './graph_0_avg.div',
            'COVID-19 Daily Deaths - no moving average',
            'COVID: 0d avg'
        )
    });

    $('#btn_0_avg_pct').click(function(){
        loadGraph(
            './graph_0_avg_pct.div',
            'COVID-19 Daily Deaths as population % - no moving average',
            'COVID: 0d avg % pop'
        )
    });

    $('#btn_3_avg').click(function(){
        loadGraph(
            './graph_3_avg.div',
            'COVID-19 Daily Deaths - 3 day moving average',
            'COVID: 3d avg'
        )
    });

    $('#btn_3_avg_pct').click(function(){
        loadGraph(
            './graph_3_avg_pct.div',
            'COVID-19 Daily Deaths as population % - 3 day moving average',
            'COVID: 3d avg % pop'
        )
    });

    $('#btn_5_avg').click(function(){
        loadGraph(
            './graph_5_avg.div',
            'COVID-19 Daily Deaths - 5 day moving average',
            'COVID: 5d avg'
        )
    });

    $('#btn_5_avg_pct').click(function(){
        loadGraph(
            './graph_5_avg_pct.div',
            'COVID-19 Daily Deaths as population % - 5 day moving average',
            'COVID: 5d avg % pop'
        )
    });

    $('#btn_15_avg').click(function(){
        loadGraph(
            './graph_15_avg.div',
            'COVID-19 Daily Deaths - 15 day moving average',
            'COVID: 15d avg'
        )
    });

    $('#btn_15_avg_pct').click(function(){
        loadGraph(
            './graph_15_avg_pct.div',
            'COVID-19 Daily Deaths as population % - 15 day moving average',
            'COVID: 15d avg (%)'
        )
    });

    btn_0_avg.trigger('click')
});
