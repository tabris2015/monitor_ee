$(function () {
   $(document).ready(function(){
        $.getJSON('/rango/ult_semana/',function(data){
			   var chart = new Highcharts.Chart({
					chart: {
						type: 'column',
						renderTo: 'ult_semana',
						marginRight: 70,
						marginBottom: 25
					},
					title: {
						text: 'Resumen Semanal',
						x: -20 //center
					},
					subtitle: {
						text: 'Consumo por areas',
						x: -20
					},
					xAxis: {
						type: 'category',
						labels: {
							rotation : -45,
						}
					},
					yAxis: {
						title: {
							text: 'Consumo en KWh'
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
