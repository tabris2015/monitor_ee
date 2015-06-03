/*$(function () {

    $('#ultimo_gauge').highcharts({

        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },

        title: {
            text: 'Consumo'
        },

        pane: {
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                    ]
                },
                borderWidth: 1,
                outerRadius: '107%'
            }, {
                // default background
            }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
            }]
        },

        // the value axis
        yAxis: {
            min: 0,
            max: 200,

            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',

            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
            },
            title: {
                text: 'km/h'
            },
            plotBands: [{
                from: 0,
                to: 120,
                color: '#55BF3B' // green
            }, {
                from: 120,
                to: 160,
                color: '#DDDF0D' // yellow
            }, {
                from: 160,
                to: 200,
                color: '#DF5353' // red
            }]
        },

        series: [{
            name: 'Speed',
            data: [80],
            tooltip: {
                valueSuffix: ' km/h'
            }
        }]

    },
        // Add some life

        function (chart) {
            if (!chart.renderer.forExport) {
                setInterval(function () {
                    var point = chart.series[0].points[0],
                        newVal,
                        inc = Math.round((Math.random() - 0.5) * 20);

                    newVal = point.y + inc;
                    if (newVal < 0 || newVal > 200) {
                        newVal = point.y - inc;
                    }

                    //point.update(newVal);

                }, 3000);
            }
        }
        );
});
*/
$(function () {
   $(document).ready(function(){
        /*
            la variable chart_options define las opciones
            para el grafico de highcharts
        */
        var chart_options = {
        
            chart: {
                type: 'gauge',
                renderTo: 'ultimo_gauge',
                plotBackgroundColor: null,
                plotBackgroundImage: null,
                plotBorderWidth: 0,
                plotShadow: false
            },

            title: {
                text: 'Consumo'
            },

            pane: {
                startAngle: -150,
                endAngle: 150,
                background: [{
                    backgroundColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0, '#FFF'],
                            [1, '#333']
                        ]
                    },
                    borderWidth: 0,
                    outerRadius: '109%'
                }, {
                    backgroundColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0, '#333'],
                            [1, '#FFF']
                        ]
                    },
                    borderWidth: 1,
                    outerRadius: '107%'
                }, {
                    // default background
                }, {
                    backgroundColor: '#DDD',
                    borderWidth: 0,
                    outerRadius: '105%',
                    innerRadius: '103%'
                }]
            },

            // the value axis
            yAxis: {
                min: 0,
                max: 200,

                minorTickInterval: 'auto',
                minorTickWidth: 1,
                minorTickLength: 10,
                minorTickPosition: 'inside',
                minorTickColor: '#666',

                tickPixelInterval: 30,
                tickWidth: 2,
                tickPosition: 'inside',
                tickLength: 10,
                tickColor: '#666',
                labels: {
                    step: 2,
                    rotation: 'auto'
                },
                title: {
                    text: 'km/h'
                },
                plotBands: [{
                    from: 0,
                    to: 120,
                    color: '#55BF3B' // green
                }, {
                    from: 120,
                    to: 160,
                    color: '#DDDF0D' // yellow
                }, {
                    from: 160,
                    to: 200,
                    color: '#DF5353' // red
                }]
            },

            series: [{
                name: 'Speed',
                data: [80],
                toolt: {
                    valueSuffix: ' km/h'
                }
            }]
        };
        // variable que almacena la fecha

        //var fecha = "2014-12-25";
        var medidor_slug = $("#med_name").text();
        //variable que almacena el url de la vista que nos retornara los datos
        var data_url;

        //$("#boton").click(function(){
                //adquiere la fecha del formulario en la plantilla
        var fecha = $("input#dia").val();
        var f_arr = fecha.split("-");
        anho = parseInt(f_arr[0]);
        mes = parseInt(f_arr[1]-1);
        dia_ = parseInt(f_arr[2]);
        var inicio = Date.UTC(anho,mes,dia_);

        data_url = '/rango/ult_dia';
        $("#jquery_test").text(data_url); //cadena de prueba
         //url concatenada con la fecha elegida
                //funcion que dibuja el chart obteniendo json del url definido anteriormente
        $.getJSON(data_url,
            function(data) {
            //chart_options.xAxis.categories = data['chart_data']['dates'];
            //chart_options.series[0].name = 'Avg Glucose (mg/dL)';
                chart_options.series[0].points[0].update(data['data']);    //define los datos
                //chart_options.series[0].data.push(data);
                //chart_options.subtitle.text = fecha; // subtitulo
                //chart_options.plotOptions.series.pointStart=inicio;
                //chart_options.plotOptions.series.pointInterval= 3600 * 1000; // one hour
                //aqui es donde crea el chart
                var chart = new Highcharts.Chart(chart_options);
            });
        //});   

        
        

    });
});
