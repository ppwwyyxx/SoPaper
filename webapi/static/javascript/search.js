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
    $scope.paper_title = "abc";
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

            $scope.paper_pid = data.results[0]._id;
            $scope.paper_title = data.results[0].title;
            $scope.paper_abstract = data.results[0].abstract;
            $scope.paper_author = data.results[0].author;
            $scope.paper_bibtex = data.results[0].bibtex;
            $scope.paper_citedby = data.results[0].citedby;
            if ($scope.paper_citedby) {
                $scope.paper_citednum = $scope.paper_citedby.length;
            }
            $scope.paper_references = data.results[0].references;
            $scope.paper_abstract = data.results[0].abstract;
            $scope.paper_download_count = data.results[0].download_cnt;

            //$scope.paper_title = data.results[0].title;
            $scope.$digest();
            $(".ui.labeled.icon.sidebar")
                .sidebar("show");
            $(".ui.extremly.wide.sidebar")
                .sidebar("hide");
        }).error(function(data, status) {
            console.log('status' + status);
            console.log(data);
        });
    }
    $scope.Download = function() {
        $.ajax({
            type: 'GET',
            url: '/download?pid=' + $scope.paper_pid,
            data: {},
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