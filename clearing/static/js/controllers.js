
var clearingApp = angular.module('clearingApp', []);

clearingApp.controller('clearingCtrl', [
    '$scope','$http',
    function ($scope, $http){
    var host = '/clearing/';
    var member = window.location.pathname.slice(1).split('/')[1];

    $scope.clearingplay = function () {
        console.log(window.location);
        window.location.href= host + member + '/play/';
    };








//    获取配置信息
    function getProfile() {
//        设置checkbox默认不选中
        $scope.chk = false;
        $scope.check = function(val){
            !val ? alert('选中') : alert('未选中');
        };
//    前往优酷视频上传，先请求服务器返回clearing的token
    $scope.toclearingUpload = function () {
        $http.get(host + member + '/getToken/').success(function (response) {
//            如果未取得token，表明未验证，先进行验证
            if (response.content['error']) {
                console.log('not auth yet , request auth.');
                window.location.href = host + member +'/authRequset/';
            }
//            如顺利获取token，携带token访问clearing上传页面（页面代码由优酷提供）
            else {
                $scope.access_token = response.content.access_token;
                console.log($scope.access_token);
                window.location.href = host + member + '/upload/?access_token=' + $scope.access_token;
            }
        }).error(function (response) {
            $scope.remind=response.r;
        });
    };
//    保存配置信息
    $scope.set = function () {
        $http({
            method: 'POST',
            url: host + member + '/profile/',
            data:$scope.profile
        }).success(function(response, status, headers, config){
            console.log('set profile success!');
        }).error(function(response){
            $scope.remind=response.r;
        });
    };
//    删除数据库中优酷验证token的4个字段
    $scope.removeclearingAuth = function () {
        $http.get(host + member + '/remove/').success(function(response, status, headers, config){
            $scope.clearingbind = false;
            $scope.flash = 'sucessfully unbind clearing';
        }).error(function(response){
            $scope.remind=response.r;
        });
    };



//    页面加载时先获取配置信息
    getProfile();

}]);
