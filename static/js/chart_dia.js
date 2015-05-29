$(function () {
   $(document).ready(function(){
        /*
            la variable chart_options define las opciones
            para el grafico de highcharts
        */
        var chart_options = {
        
        	chart: {
        		type: 'line',
        		renderTo: 'resumen_dia',
        		marginRight: 70,
        		marginBottom: 25
        	},
            plotOptions: {
            series: {
                //pointStart: Date.UTC(2010, 0, 1),
                pointInterval: 3600 * 1000 // one hour
            }
            },
        	title: {
        		text: 'consumo',
        		x: -20 //center
        	},
        	subtitle: {
        		text: "fecha",
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
            xAxis: {
                type: 'datetime',
                allowDecimals: false//type: 'datetime'
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
        	series: [{}],
    	};
        // variable que almacena la fecha

    	//var fecha = "2014-12-25";
        var medidor_slug = $("#med_name").text();
    	//variable que almacena el url de la vista que nos retornara los datos
        var data_url;

    	$("#btn_buscar").click(function(){
                //adquiere la fecha del formulario en la plantilla
    	var fecha = $("input#dia").val();
        var f_arr = fecha.split("-");
        anho = parseInt(f_arr[0]);
        mes = parseInt(f_arr[1]-1);
        dia_ = parseInt(f_arr[2]);
        var inicio = Date.UTC(anho,mes,dia_);

        data_url = '/rango/chart_dia_json/?dia='+fecha+"&medidor_slug="+medidor_slug;
    	$("#jquery_test").text(data_url); //cadena de prueba
    	 //url concatenada con la fecha elegida
    	        //funcion que dibuja el chart obteniendo json del url definido anteriormente
        $.getJSON(data_url,
            function(data) {
            //chart_options.xAxis.categories = data['chart_data']['dates'];
            //chart_options.series[0].name = 'Avg Glucose (mg/dL)';
                chart_options.series= data;    //define los datos
                chart_options.subtitle.text = fecha; // subtitulo
                chart_options.plotOptions.series.pointStart=inicio;
                //chart_options.plotOptions.series.pointInterval= 3600 * 1000; // one hour
                //aqui es donde crea el chart
                var chart = new Highcharts.Chart(chart_options);
            });
    	});   

        
        

    });
});
