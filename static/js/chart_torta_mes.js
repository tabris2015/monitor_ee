$(function () {
            $(document).ready(function () {
                var chart_options = {
                    chart: {
                        renderTo: "resumen_mes",
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false
                    },
                    title: {
                        text: 'Resumen de consumo por áreas'
                    },
                    tooltip: {
                        pointFormat: '{series.name}: <b>{point.y:.1f} KWh</b> - {point.percentage:.1f}%'
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: false
                            },
                            showInLegend: true
                        }
                    },
                    series: [{
                        type: 'pie',
                        name: 'Consumo de Potencia',
                        data: [
                            ['Firefox',   45.0],
                            ['IE',       26.8],
                            {
                                name: 'Chrome',
                                y: 12.8,
                                sliced: true,
                                selected: true
                            },
                            ['Safari',    8.5],
                            ['Opera',     6.2],
                            ['Others',   0.7]
                        ]
                    }]
                };
                var data_url;
                // Build the chart

                $("#btn_buscar").click(function(){      //cuando presionamos boton
                    fecha = $("input#mes").val()
                    data_url = '/rango/torta_mes_json/?mes=' + fecha;
                    $("#jquery_test1").text(data_url);
                    $.getJSON(data_url, function(data){
                        chart_options.series[0] = data;
                        var chart = new Highcharts.Chart(chart_options);
                    });
                });

            });

        });
