var SearchApp = angular.module('SearchApp', ['ngResource', 'ngRoute']);

/*
$(document).ready(function() {

    query: function(data) {
        $.ajax({
            type: 'POST',
            url: '/query',
            data: {

            },
            dataType: 'json'
        }).success(function(res, status, headers, config) {
            if (res.success) {
                console.log(res.data);
            } else if (res.error) {
                console.log(res.error);
                // mai meng
            }
        }).error(function(data, status) {
            console.log('status' + status);
            console.log(data);
        });
    }
});
*/


function SearchCtrl($scope, $http) {
    $scope.Search = function() {
        $.ajax({
            type: 'GET',
            url: '/query?q=' + $scope.keyword,
            data: {
                'q': $scope.keyword
            },
            dataType: 'json'
        }).success(function(data, status, headers, config) {
            console.log('OK');
            console.log(data);
        }).error(function(data, status) {
            console.log('status' + status);
            console.log(data);
        });
    }
}