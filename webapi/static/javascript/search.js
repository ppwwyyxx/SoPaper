var SearchApp = angular.module('SearchApp', ['ngResource', 'ngRoute']);

SearchApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});
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
    $scope.paper_title = "So easy";
    $scope.hasbibtex = false;
    $scope.hasreferences = false;
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
            if (typeof $scope.paper_author != 'undefined')
                $scope.hasauthor = true;
            $scope.paper_bibtex = data.results[0].bibtex;
            if (typeof $scope.paper_bibtex != 'undefined')
                $scope.hasbibtex = true;
            $scope.paper_citedby = data.results[0].citedby;
            if (typeof $scope.paper_citedby != 'undefined')
                $scope.hascitedby = true;
            if ($scope.paper_citedby) {
                $scope.paper_citednum = $scope.paper_citedby.length;
            }
            $scope.paper_references = data.results[0].references;
            if (typeof $scope.paper_references != 'undefined')
                $scope.hasreferences = true;
            $scope.paper_download_count = data.results[0].download_cnt;

            $scope.$digest();
            $(".ui.labeled.icon.sidebar")
                .sidebar("show");
            $(".ui.extremly.wide.sidebar")
                .sidebar("hide");

            $('.ui.bib.modal').modal('setting', 'closable', false)
                .modal('attach events', '.bib.button', 'show');

            $('.ui.ref.modal').modal('setting', 'closable', false)
                .modal('attach events', '.ref.button', 'show');

            $('.ui.com.modal').modal('setting', 'closable', false)
                .modal('attach events', '.com.button', 'show');

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