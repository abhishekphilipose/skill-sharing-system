document.addEventListener('DOMContentLoaded', function() {
    var options = {
        series: [{
            name: 'Total Users',
            data: skillStats.map(stat => stat.total_users)
        }, {
            name: 'Total Requests',
            data: skillStats.map(stat => stat.total_requests)
        }, {
            name: 'Completed Requests',
            data: skillStats.map(stat => stat.completed_requests)
        }],
        chart: {
            type: 'bar',
            height: 350,
            stacked: false,
        },
        plotOptions: {
            bar: {
                horizontal: false,
                borderRadius: 10
            },
        },
        xaxis: {
            categories: skillStats.map(stat => stat.skills),
        },
        colors: ['#108dff', '#287F71', '#E77636'],
        title: {
            text: 'Skills Usage Statistics'
        }
    };

    var chart = new ApexCharts(document.querySelector("#skill-statistics"), options);
    chart.render();
});
