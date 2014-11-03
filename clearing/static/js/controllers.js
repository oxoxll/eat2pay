
var clearingApp = angular.module('clearingApp', []);

clearingApp.controller('clearingCtrl', ['$scope','$http', function ($scope, $http){
    var host = '/clearing/';
    var member = window.location.pathname.slice(1).split('/')[1];

//    获取配置信息
    function getMenbers() {
//        设置checkbox默认不选中
        $scope.member_list = [{id: 1, name: 'asd'}, {id: 2, name: 'qwe'}, {id: 3, name: 'zxv'}, {id: 4, name: 'bgt'}, {id: 5, name: 'neo'} ];
        return;
        $http({
            method: 'GET',
            url: host + member +  '/get_member_list/'
        }).success(function(response, status, headers, config){
            //console.log('set profile success!');
            $scope.member_list = response.content.member_list;
        }).error(function(response){
            $scope.remind=response.r;
        });
    }

//    保存配置信息
    $scope.confirm_order = function () {
        $http({
            method: 'POST',
            url: host + member + '/profile/',
            data:$scope.member_list
        }).success(function(response, status, headers, config){
            console.log('set profile success!');
            alert('set profile success!');
        }).error(function(response){
            $scope.remind=response.r;
        });
    };

//    页面加载时先获取配置信息
    getMenbers();

}]);
