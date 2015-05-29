$(function () {
   $(document).ready(function(){
        $.getJSON('/rango/javamap/',function(data){
			   var chart = new Highcharts.Chart({
					chart: {
						type: 'line',
						renderTo: 'javachart',
						marginRight: 70,
						marginBottom: 25
					},
					title: {
						text: 'test',
						x: -20 //center
					},
					subtitle: {
						text: 'test chart django',
						x: -20
					},
					yAxis: {
						title: {
							text: 'valor'
						},
						plotLines: [{
							value: 0,
							width: 1,
							color: '#808080'
						}]
					},
					tooltip: {
						valueSuffix: 'KWh'
					},
					legend: {
						layout: 'vertical',
						align: 'right',
						verticalAlign: 'top',
						x: -10,
						y: 100,
						borderWidth: 0
					},
					series:data, 
				});											
        });
    });
});
