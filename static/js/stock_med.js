$(function () {

    var medidor_slug = $("#med_name").text();
    //variable que almacena el url de la vista que nos retornara los datos
    var data_url;
    data_url = '/rango/completo_json/?medidor_slug='+medidor_slug;
    $.getJSON(data_url, function (data) {

        // create the chart
        $('#chart_medidor').highcharts('StockChart', {
            chart: {
                alignTicks: false
            },

            rangeSelector: {
                selected: 1
            },

            title: {
                text: 'Histórico de Consumo'
            },

            subtitle: {
                text: "Sector: "+ medidor_slug,
                x: -20
            },

            yAxis: [{ // Primary yAxis
                labels: {
                    format: '{value}Kwh',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: 'Promedio',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                min: 0,
                max:50

            }, { // Secondary yAxis
                title: {
                    text: 'Acumulado',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    format: '{value} Kwh',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                max: 8000
                //opposite: true
            }],

            series: [{
                type: 'column',
                name: 'Potencia',
                data: data,
                yAxis: 1,
                dataGrouping: {
                    //forced: true,
                    units: [
                        [
                            'week',
                            [1]
                        ],
                        
                        [
                            'month', // unit name
                            [1] // allowed multiples
                        ], 
                        [
                            'hour',
                            [1]
                        ]
                    ]
                }
            },
            {
                type: 'line',
                name: 'Promedio',
                data: data,
                dataGrouping: {
                    //forced: true,
                    units: [
                        
                        [
                            'week',
                            [1]
                        ],
                        
                        [
                            'month', // unit name
                            [1] // allowed multiples
                        ], 
                        [
                            'hour',
                            [1]
                        ]
                    ]
                }
            }],

        });
    });
});