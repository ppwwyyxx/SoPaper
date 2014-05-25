var SearchApp = angular.module('SearchApp', ['ngResource', 'ngRoute', 'ngSanitize']);


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

var PAPER_PER_PAGE = 3;

function SearchCtrl($scope, $http, $sce) {
    $scope.paper_title = "So easy";
    $scope.hasbibtex = false;
    $scope.hasreferences = false;
    $scope.zan = 0;
    $scope.cai = 0;

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

            $scope.search_type = data.type;
            if ($scope.search_type == 'title') {
                $scope.paper_pid = data.results[0]._id;
                console.log(data.results[0]._id);
                $scope.paper_title = data.results[0].title;
                $scope.paper_abstract = data.results[0].abstract;
                $scope.paper_author = data.results[0].author;
                if (typeof $scope.paper_author != 'undefined')
                    $scope.hasauthor = true;
                $scope.paper_bibtex = data.results[0].bibtex;
                if (typeof $scope.paper_bibtex != 'undefined')
                    $scope.hasbibtex = true;
                $scope.paper_citednum = data.results[0].citecnt;
                if ($scope.paper_citednum != 0)
                    $scope.hascitedby = true;
                $scope.paper_references = data.results[0].references;
                if (typeof $scope.paper_references != 'undefined')
                    $scope.hasreferences = true;
                $scope.paper_download_count = data.results[0].download_cnt;
                $scope.zan = 0;
                $scope.cai = 0;
                $scope.downloadahref = '/download?pid=' + $scope.paper_pid;
                $scope.haspdf = data.results[0].haspdf;
                $scope.paperpage = data.results[0].page;
                $scope.$digest();
                /* UI Settings */
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
                $('.ui.uprate.button').on('click', function() {
                    $('.ui.message').show();
                    $.ajax({
                        type: 'GET',
                        url: '/mark?pid=' + $scope.paper_pid + '&mark=1',
                        data: {},
                        dataType: 'json'
                    }).success(function(data, status, headers, config) {
                        console.log('OK');
                        console.log(data);
                        $scope.zan = 1;
                        $scope.cai = 2;
                        $scope.$digest();
                    }).error(function(data, status) {
                        console.log('status' + status);
                        has
                        console.log(data);
                    });
                });
                $('.ui.downrate.button').on('click', function() {
                    $('.ui.message').show();
                    $.ajax({
                        type: 'GET',
                        url: '/mark?pid=' + $scope.paper_pid + '&mark=-1',
                        data: {},
                        dataType: 'json'
                    }).success(function(data, status, headers, config) {
                        console.log('OK');
                        console.log(data);
                        $scope.cai = 1;
                        $scope.zan = 2;
                        $scope.$digest();
                    }).error(function(data, status) {
                        console.log('status' + status);
                        console.log(data);
                    });
                });
                Tryingdownload();

            } else if ($scope.search_type == 'content') {
                $scope.papers = data.results;
                if (typeof $scope.papers != 'undefined')
                    $scope.paper_cnt = data.results.length;
                $scope.pagecnt = Math.ceil(($scope.paper_cnt + 0.0) / PAPER_PER_PAGE);
                $scope.currentpage = 1;
                $scope.currentpapers = [];
                if ($scope.paper_cnt < PAPER_PER_PAGE)
                    icnt = $scope.paper_cnt;
                else icnt = PAPER_PER_PAGE;
                for (var i = 0; i < icnt; i++)
                    $scope.currentpapers.push($scope.papers[($scope.currentpage - 1) * PAPER_PER_PAGE + i]);
                $scope.hassummary = true;
                $scope.$digest();
            }

        }).error(function(data, status) {
            console.log('status' + status);
            console.log(data);
        });
    };

    $scope.Download = function() {
        $.ajax({
            type: 'GET',
            url: '/download?pid=' + $scope.paper_pid,
            data: {},
            dataType: 'json'
        }).success(function(data, status, headers, config) {
            console.log('Downloading...');
            console.log(data);
        }).error(function(data, status) {
            console.log('status' + status);
            console.log(data);
        });
    };

    function ReadHTML(page) {
        $.ajax({
            type: 'GET',
            url: '/html?pid=' + $scope.paper_pid + '&page=0',
            data: {},
            dataType: 'json'
        }).success(function(data, status, headers, config) {
            console.log('html comes');
            console.log(data);
            $scope.pdfhtml = $sce.trustAsHtml(data.htmls['0']);
            $scope.$digest();
            console.log($scope.pdfhtml);
            nakedhtml = document.createElement('div');
            nakedhtml.innerHTML = $scope.pdfhtml;
        }).error(function(data, status) {
            console.log('status' + status);
            console.log(data);
        });
    }

    function Tryingdownload() {
        $.ajax({
            type: 'GET',
            url: '/download_available?pid=' + $scope.paper_pid,
            data: {},
            dataType: 'json'
        }).success(function(data, status, headers, config) {
            console.log('Ask for download OK');
            console.log(data);
            if (data.progress == 'done') {
                console.log('download_complete');
                $scope.downloadahref = '/download?pid=' + $scope.paper_pid;
                ReadHTML();
                return;
            } else if (data.progress == 'failed') {
                alert('Due to law, This paper is unable to download');
            } else {
                console.log(data.progress);
                //Tryingdownload();
                setTimeout(Tryingdownload, 2000);

            }
        }).error(function(data, status) {
            console.log('status' + status);
            console.log(data);
        });
    }
}