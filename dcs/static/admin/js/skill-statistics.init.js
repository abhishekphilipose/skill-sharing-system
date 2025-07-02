document.addEventListener('DOMContentLoaded', function() {
    var options = {
        series: [{
            name: 'Active Users',
            type: 'column',
            data: skillStats.map(stat => stat.total_users)
        }, {
            name: 'Total Requests',
            type: 'area',
            data: skillStats.map(stat => stat.total_requests)
        }, {
            name: 'Completed',
            type: 'line',
            data: skillStats.map(stat => stat.completed_requests)
        }],
        chart: {
            height: 350,
            type: 'line',
            stacked: false,
            toolbar: {
                show: true,
                tools: {
                    download: true,
                    selection: true,
                    zoom: true,
                    zoomin: true,
                    zoomout: true,
                    pan: true,
                }
            },
            animations: {
                enabled: true,
                easing: 'easeinout',
                speed: 800,
                animateGradually: {
                    enabled: true,
                    delay: 150
                },
                dynamicAnimation: {
                    enabled: true,
                    speed: 350
                }
            },
            dropShadow: {
                enabled: true,
                opacity: 0.3,
                blur: 5,
                left: -7,
                top: 22
            }
        },
        stroke: {
            width: [0, 2, 5],
            curve: 'smooth'
        },
        plotOptions: {
            bar: {
                columnWidth: '50%',
                borderRadius: 5
            }
        },
        fill: {
            opacity: [0.85, 0.25, 1],
            gradient: {
                inverseColors: false,
                shade: 'light',
                type: "vertical",
                opacityFrom: 0.85,
                opacityTo: 0.55,
                stops: [0, 100, 100, 100]
            }
        },
        labels: skillStats.map(stat => stat.skills),
        markers: {
            size: 0
        },
        xaxis: {
            type: 'category',
            title: {
                text: 'Skills',
                style: {
                    fontSize: '14px',
                    fontWeight: 600
                }
            }
        },
        yaxis: {
            title: {
                text: 'Count',
                style: {
                    fontSize: '14px',
                    fontWeight: 600
                }
            },
            min: 0
        },
        tooltip: {
            shared: true,
            intersect: false,
            y: {
                formatter: function (y) {
                    if (typeof y !== "undefined") {
                        return y.toFixed(0);
                    }
                    return y;
                }
            }
        },
        legend: {
            labels: {
                useSeriesColors: true
            },
            markers: {
                customHTML: [
                    function() {
                        return '<span><i class="fas fa-circle"></i></span>'
                    }
                ]
            }
        },
        colors: ['#008FFB', '#00E396', '#FEB019'],
        title: {
            text: 'Skill Analytics Overview',
            align: 'left',
            style: {
                fontSize: '16px',
                fontWeight: 600,
                fontFamily: 'inherit'
            }
        }
    };

    var chart = new ApexCharts(document.querySelector("#skill-statistics"), options);
    chart.render();
});
