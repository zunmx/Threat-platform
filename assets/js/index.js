var app = angular.module('CTEWP', []);
app.controller('base', function ($scope, $http) {

    $scope.value = {
        'visitorNum': 0,
        "newIpNum": 0,
        "portNum": 0
    }
    $scope.redraw = function () {
        $('#lineChart').sparkline($scope.visitor.visitorNum6, {
            type: 'line',
            height: '70',
            width: '100%',
            lineWidth: '2',
            lineColor: 'rgba(255, 255, 255, .5)',
            fillColor: 'rgba(255, 255, 255, .15)'
        });
        $('#lineChart2').sparkline($scope.visitor.newIpNum6, {
            type: 'line',
            height: '70',
            width: '100%',
            lineWidth: '2',
            lineColor: 'rgba(255, 255, 255, .5)',
            fillColor: 'rgba(255, 255, 255, .15)'
        });
        $('#lineChart3').sparkline($scope.visitor.portNum6, {
            type: 'line',
            height: '70',
            width: '100%',
            lineWidth: '2',
            lineColor: 'rgba(255, 255, 255, .5)',
            fillColor: 'rgba(255, 255, 255, .15)'
        });
        $('#ipatttime').sparkline($scope.visitor.ipatttime, {
            type: 'line',
            height: '150',
            width: '100%',
            lineWidth: '2',
            lineColor: 'rgba(255, 255, 255, .5)',
            fillColor: 'rgba(255, 255, 255, .15)'
        });

        $scope.calcVisitorNum();
    }
    $scope.init = function () {
        $scope.visitor = {
            "visitorNum6": [],  //近期访问总数
            "newIpNum6": [], // 近期访问者，不同ip
            "portNum6": [],// 近期独立端口数
            "ipTop": {}, // ip前10
            "portTop": {}, //端口前10
            "bef100": {}, // 前100攻击数据
            "ip10": {},//ip攻击前十
            "port10": {},//威胁端口前十
            "warn": {},
            "ipatttime": [], // ip攻击时段
            "ipatttimedt": []
        }
        $http({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            },
            method: 'POST',
            data: { method: "getv6" },
            url: "api.php"
        }).success(function (response, status, headers, config) {
            if (response["code"] == 0) {
                response = response["msg"];
                $scope.visitor.visitorNum6 = [];
                $.each(response, function (i, item) {
                    $scope.visitor.visitorNum6.push(parseInt(item.sec));
                })
            } else {
                swal({
                    title: '错误',
                    text: '请求接口过于频繁',
                    icon: "error",
                    timer: 1000,
                    buttons: false,
                });
            }
        });
        $http({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            },
            method: 'POST',
            data: { method: "getn6" },
            url: "api.php"
        }).success(function (response, status, headers, config) {
            if (response["code"] == 0) {
                response = response["msg"];
                $scope.visitor.newIpNum6 = [];
                $.each(response, function (i, item) {
                    $scope.visitor.newIpNum6.push(parseInt(item.sec));
                })
            } else {
                swal({
                    title: '错误',
                    text: '请求接口过于频繁',
                    icon: "error",
                    timer: 1000,
                    buttons: false,
                });
            }
        });
        $http({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            },
            method: 'POST',
            data: { method: "getp6" },
            url: "api.php"
        }).success(function (response, status, headers, config) {
            if (response["code"] == 0) {
                response = response["msg"];
                $scope.visitor.portNum6 = [];
                $.each(response, function (i, item) {
                    $scope.visitor.portNum6.push(parseInt(item.sec));
                })
            } else {
                swal({
                    title: '错误',
                    text: '请求接口过于频繁',
                    icon: "error",
                    timer: 1000,
                    buttons: false,
                });
            }
        });

        $http({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            },
            method: 'POST',
            data: { method: "getbef10" },
            url: "api.php"
        }).success(function (response, status, headers, config) {
            if (response["code"] == 0) {
                response = response["msg"];
                $scope.visitor.bef100 = response;
            } else {
                swal({
                    title: '错误',
                    text: '请求接口过于频繁',
                    icon: "error",
                    timer: 1000,
                    buttons: false,
                });
            }
        });
        $http({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            },
            method: 'POST',
            data: { method: "gettopip10" },
            url: "api.php"
        }).success(function (response, status, headers, config) {
            if (response["code"] == 0) {
                response = response["msg"];
                $scope.visitor.ip10 = response;
            } else {
                swal({
                    title: '错误',
                    text: '请求接口过于频繁',
                    icon: "error",
                    timer: 1000,
                    buttons: false,
                });
            }
        });
        $http({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            },
            method: 'POST',
            data: { method: "gettopport10" },
            url: "api.php"
        }).success(function (response, status, headers, config) {
            if (response["code"] == 0) {
                response = response["msg"];
                $scope.visitor.port10 = response;
            } else {
                swal({
                    title: '错误',
                    text: '请求接口过于频繁',
                    icon: "error",
                    timer: 1000,
                    buttons: false,
                });
            }
        });
        $http({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            },
            method: 'POST',
            data: { method: "gettotal" },
            url: "api.php"
        }).success(function (response, status, headers, config) {
            if (response["code"] == 0) {
                response = response["msg"][0]["sec"];
                $scope.total = response;
            } else {
                swal({
                    title: '错误',
                    text: '请求接口过于频繁',
                    icon: "error",
                    timer: 1000,
                    buttons: false,
                });
            }
        });

        $http({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            },
            method: 'POST',
            data: { method: "getwarn" },
            url: "api.php"
        }).success(function (response, status, headers, config) {
            if (response["code"] == 0) {
                response = response["msg"];
                $scope.visitor.warn = response;
            } else {
                swal({
                    title: '错误',
                    text: '请求接口过于频繁',
                    icon: "error",
                    timer: 1000,
                    buttons: false,
                });
            }
        });
        $http({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            },
            method: 'POST',
            data: { method: "ipatttime" },
            url: "api.php"
        }).success(function (response, status, headers, config) {
            if (response["code"] == 0) {
                response = response["msg"];
                $scope.visitor.ipatttime = [];
                $scope.visitor.ipatttimedt = []
                $.each(response, function (i, item) {
                    $scope.visitor.ipatttime.push(parseInt(item.sec));
                })
                $.each(response, function (i, item) {
                    $scope.visitor.ipatttimedt.push((item.dt));
                })

                var ctx = document.getElementById('statisticsChart').getContext('2d');
                var statisticsChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: $scope.visitor.ipatttimedt,
                        datasets: [{
                            label: "攻击次数",
                            borderColor: '#177dff',
                            pointBackgroundColor: 'rgba(23, 125, 255, 0.6)',
                            pointRadius: 0,
                            backgroundColor: 'rgba(23, 125, 255, 0.4)',
                            legendColor: '#177dff',
                            fill: true,
                            borderWidth: 2,
                            data: $scope.visitor.ipatttime
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        legend: {
                            display: true
                        },
                        tooltips: {
                            bodySpacing: 2,
                            mode: "nearest",
                            intersect: 0,
                            position: "nearest",
                            xPadding: 10,
                            yPadding: 10,
                            caretPadding: 10
                        },
                        layout: {
                            padding: { left: 5, right: 5, top: 15, bottom: 15 }
                        },
                        scales: {
                            yAxes: [{
                                ticks: {
                                    fontStyle: "500",
                                    beginAtZero: false,
                                    maxTicksLimit: 5,
                                    padding: 10
                                },
                                gridLines: {
                                    drawTicks: false,
                                    display: false
                                }
                            }],
                            xAxes: [{
                                gridLines: {
                                    zeroLineColor: "transparent"
                                },
                                ticks: {
                                    padding: 10,
                                    fontStyle: "500"
                                }
                            }]
                        },
                        legendCallback: function (chart) {
                            var text = [];
                            text.push('<ul class="' + chart.id + '-legend html-legend">');
                            for (var i = 0; i < chart.data.datasets.length; i++) {
                                text.push('<li><span style="background-color:' + chart.data.datasets[i].legendColor + '"></span>');
                                if (chart.data.datasets[i].label) {
                                    text.push(chart.data.datasets[i].label);
                                }
                                text.push('</li>');
                            }
                            text.push('</ul>');
                            return text.join('');
                        }
                    }
                });




            } else {
                swal({
                    title: '错误',
                    text: '请求接口过于频繁',
                    icon: "error",
                    timer: 1000,
                    buttons: false,
                });
            }
        });

        setInterval(function () {
            $scope.redraw();
        }, 1000);
        setInterval(function () {
            $scope.init();
        }, 60000);
        swal({
            title: '消息',
            text: '重新加载数据文件',
            icon: "success",
            timer: 1000,
            buttons: false,
        });
    }
    $scope.calcVisitorNum = function () {
        $scope.value.visitorNum = Number.parseFloat(((($scope.visitor.visitorNum6[0] - $scope.visitor.visitorNum6[1]) / $scope.visitor.visitorNum6[1]) * 100).toFixed(2));
        $scope.value.newIpNum = Number.parseFloat(((($scope.visitor.newIpNum6[0] - $scope.visitor.newIpNum6[1]) / $scope.visitor.newIpNum6[1]) * 100).toFixed(2));
        $scope.value.portNum = Number.parseFloat(((($scope.visitor.portNum6[0] - $scope.visitor.portNum6[1]) / $scope.visitor.portNum6[1]) * 100).toFixed(2));
        // $("#d0").html($scope.value.visitorNum + "%");
        // $("#d1").html($scope.value.newIpNum + "%");
        // $("#d2").html($scope.value.portNum + "%");
    }

});