//Global variables Start.

//Default page number for grid.
var pageNumber = 1;
//pages numbers for grid.
var noOfPagesVisible = 5;

var yearResults = '';

var global_sortBy = '';
var global_sortDir = '';

var ref_Pagenumber = 1;
var ref_sortBy = '';
var ref_sortDir = '';

var currentElectionType = 'General';
var isFiltered = false;
var isReferendum = false;

var global_maxPages = 0;

var isViewMap = false;

var tabType = '';

var global_county = null;
var global_office = null;
var global_party = null;
var global_filtercandidateLname = null;
var global_filterElectionType = null;

var global_ref_county = null;
var global_ref_Electiontype = null;

var isLogin = false;
var global_CandidateSearch_ElectionTypes = [];
var isMainFilter = false;
var globale_Filtered_ElectionType = null;

//Global variables End.

var urls = {
    GET_ELECTION_YEARS: "/ENRHistorical/GetElectionYears",
    GET_ELECTION_DATA: "/ENRHistorical/GetElectionData",
    GET_REFERENDUMS_DATA: "/ENRHistorical/GetReferendums",
    GET_ELECTION_TYPES: "/ENRHistorical/GetElectionTypes",
    GET_ELECTION_URL_BY_YEAR: "/ENRHistorical/GetElectionURLByYear",
    GET_ELECTION_TYPES_BY_YEAR: "/ENRHistorical/GetElectionTypesByYear",
    GET_ELECTION_YEARS_BY_REFTYPE: "/ENRHistorical/GetElectionYearsByRefType",
    GET_ELECTION_TYPE_FOR_DISPLAY_MESSAGE: "/ENRHistorical/GetElectionTypeForDisplayCandidateMessage",
    GET_ELECTION_LAST_UPDATE_DATE: "/ENRHistorical/GetElectionLastUpdateDate",
    GET_OFFICES: "/ENRHistorical/GetOffices",
    GET_PARTIES: "/ENRHistorical/GetParties",
    EXPORT_ELECTIONS_TO_CSV: "/ENRHistorical/ExportElectionsToCSV",
    EXPORT_CANDIDATES_TO_CSV: "/ENRHistorical/ExportCandidatesToCSV",
    EXPORT_REFERENDUMS_TO_CSV: "/ENRHistorical/ExportReferendumsToCSV"
};

var historicalResults = (function () {

    methods = {
        //Search by voter information to login 
        submit: function () {

        },

        openPopup: function (id) {
            $('#' + id).removeClass("modal fade bd-example-modal-lg");
            $('#' + id).addClass("modal fade bd-example-modal-lg show in");
            $('body').addClass("modal-open");
            $('#' + id).show();
            $("body").append("<div class='modal-backdrop fade show'></div>");
            historicalResults.service.hideOrShowDivs(id);
        },

        hideOrShowDivs: function (id) {
            if (id == 'filter-tab1') {
                if ($("#candidateLname").val() && $("#candidateLname").val().trim().length > 0
                    && $('#drpElectionYears option:selected').text() == 'Select Year') {
                    $("#divElectionType").show();
                    $("#divCandidateLastName").hide();
                }
                else {
                    $("#divElectionType").hide();
                    $("#divCandidateLastName").show();
                }
            }
        },

        closePopup: function () {
            $(".modal").removeClass("in");
            $(".modal-backdrop").remove();
            $('body').removeClass('modal-open');
            $('body').css('padding-right', '');
            $(".modal").hide();
        },

        appendTbodyData: function (data, year, electionType) {
            var htmlData = '';
            if (data.length > 0) {
                if ($('#candidateLname').val() !== "" && $('#drpElectionYears option:selected').text() === 'Select Year') {
                    displayCandidateGrid(data, htmlData);
                } else {
                    displayElectionGrid(data, htmlData);
                }
            } else if ($('#candidateLname').val() !== "" && $('#drpElectionYears option:selected').text() === 'Select Year') {
                $('#lblNoresult').show().html('The Candidate ' + $('#candidateLname').val().trim() + ' did not participate in any elections.');
                $('#gridDiv').hide();
                showCandidateGrid();
                $('#divInnerCandidateGrid').hide();
            } else if (!isFiltered) {
                if (electionType === 'Special') {
                    displayElectionGrid(data, htmlData);
                    $('#lblNoElectionData').html('No data found.').show();
                } else if (!isReferendum) {
                    historicalResults.service.getElectionTypeForMessage(year, electionType)
                        .done(function (data) {
                            if (data && data.length > 0) {
                                $('#lblNoElectionData').show().html('Candidate ' + $('#candidateLname').val() + ' did not participate in the ' + data[0].ElectionType + '.');
                            }
                        });
                }
                $('#gridDiv').hide();
                showElectionReferendumGrid();
            } else {
                isFiltered = false;
                $('#lblNofilterdata').show();
                if ($('#county option:selected').text() === '-- ALL COUNTIES --' &&
                    global_filtercandidateLname.length > 0) {
                    $('#lblNofilterdata').html('No results returned.');
                } else if ($('#county option:selected').text().search('-- ALL COUNTIES --') != -1) {
                    $('#lblNofilterdata').html('No results returned.');
                } else {
                    if ($("#county option:selected").map(function() { return this.text }).get().join(',').search(',') == -1) {
                        $('#lblNofilterdata').html('No results returned from ' + $("#county option:selected").map(function() { return this.text }).get().join(',') + ' County.');
                    } else {
                        $('#lblNofilterdata').html('No results returned from ' + $("#county option:selected").map(function() { return this.text }).get().join(',') + ' Counties.');
                    }
                }
                historicalResults.service.closePopup();
            }
        },

        getElectionTypeForMessage: function(year, electionType) {
            return $.ajax({
                url: urls.GET_ELECTION_TYPE_FOR_DISPLAY_MESSAGE,
                type: "POST",
                data: {
                    'year': year,
                    'electionType': electionType
                }
            });
        },

        setPageNumber: function (pagCount, totalPageCount) {
            var noOfPage = Math.ceil(totalPageCount);
            var pages = '';
            var pageCount = pagCount;
            global_maxPages = totalPageCount;

            //New Pagination Change
            var _pageVisibleCount = (noOfPage > pageCount) ? pageCount : noOfPage;

            for (var i = 1; i <= _pageVisibleCount; i++) {
                pages += generatePageLink(i);
            }

            if (noOfPage > pageCount) {
                pages += '<li class="page-item liEndDot"><span class="page-link">...</span></li>';
                pages += generatePageLink(noOfPage);
            }
            if ($('#candidateLname').val() != "" && $('#drpElectionYears option:selected').text() == 'Select Year') {//Candidate grid
                $('#candidatePagination li.page-item.num').remove();
                $('#candidatePagination .liStartDot').remove();
                $('#candidatePagination .liEndDot').remove();
                $('#candidatePagination').find('.liPrevious').after(pages);
            } else if (isReferendum) {
                $('#referendumPagination li.page-item.num').remove();
                $('#referendumPagination .liStartDot').remove();
                $('#referendumPagination .liEndDot').remove();
                $('#referendumPagination').find('.liPrevious').first().after(pages);
            } else {//primary
                $('#primaryPagination li.page-item.num').remove();
                $('#primaryPagination .liStartDot').remove();
                $('#primaryPagination .liEndDot').remove();
                $('#primaryPagination').find('.liPrevious').after(pages);
            }
        },

        getElectionLastUpdateDate: function (year) {
            var eleType = global_filterElectionType == null ? currentElectionType : global_filterElectionType;
            return $.ajax({
                url: urls.GET_ELECTION_LAST_UPDATE_DATE,
                type: "POST",
                data: {
                    'year': year,
                    'electionType': eleType
                },
                success: function (data) {
                    if (data.length > 0) {
                        var lastUpdatedDate = new Date(data[0].UpdatedDate);
                        $("#spanUpdatedDate").html("Last Updated " + lastUpdatedDate.toLocaleString('en-us', { month: 'long', day: 'numeric', year: 'numeric', hour: 'numeric', hour12: true, minute: 'numeric' }));
                    }
                }
            });
        },

        getElectionData: function (year, candidateLName, pageNumber, sortBy, sortDir, setPageNumber) {
            var eleType = global_filterElectionType == null ? currentElectionType : global_filterElectionType;
            return $.ajax({
                url: urls.GET_ELECTION_DATA,
                type: "POST",
                data: {
                    'year': year,
                    'candidateName': candidateLName,
                    'pageNumber': pageNumber,
                    'sortBy': sortBy,
                    'sortDir': sortDir,
                    'electionType': eleType,
                    'county': global_county,
                    'office': global_office,
                    'party': global_party,
                    'filterCandidateName': global_filtercandidateLname,
                    'filterElectionType': (global_filterElectionType == null ? false : true)
                },
                success: function (data) {
                    historicalResults.service.appendTbodyData(data, year, eleType);
                    if (setPageNumber) {
                        if (data.length > 0) {
                            historicalResults.service.setPageNumber(noOfPagesVisible, data[0].pagesCount);
                            $("#candidatePagination .liPrevious").next().find('a.page-link-num').addClass('active');
                            $("#primaryPagination .liPrevious").next().find('a.page-link-num').addClass('active');
                        }
                    }
                }
            });
        },

        getElectionYearsByURL: function (refType) {
            $.ajax({
                url: urls.GET_ELECTION_YEARS_BY_REFTYPE,
                type: "POST",
                data: { 'refType': refType },
                success: function (data) {
                    //Historical Results start.                   
                    var yearCountPerColumn = 4;
                    var initialValue = 1;
                    var innerDivHtml = '';
                    $.each(data, function (i, v) {
                        if (initialValue < yearCountPerColumn) {
                                innerDivHtml = innerDivHtml
                                    + '<a href="#" class="text-slid-grid padding-top10 padding-bottom10 hand-crs" onclick="onElectionYearClick(' + v.ElectionYear + ');">'
                                    + v.ElectionYear
                                    + '</a>';
                                initialValue++;
                        } else if (initialValue == yearCountPerColumn) {
                            innerDivHtml = innerDivHtml
                                + '<a href="#" class="text-slid-grid padding-top10 padding-bottom10 hand-crs" onclick="onElectionYearClick(' + v.ElectionYear + ');">'
                                + v.ElectionYear
                                + '</a>';
                            initialValue = 1;
                        }
                    });

                    if (initialValue <= yearCountPerColumn) {
                        $divElectionMapYears.append('<div class="main-heading-primary">ELECTION RESULT MAPS</div>');
                        $divElectionMapYears.append('<div class="col-md-12 col-sm-12 row">');
                        $divElectionMapYears.append(innerDivHtml);
                        $divElectionMapYears.append('</div>');
                        $divElectionMapYears.append('<div class="mr-tp-200">Election Result Maps are available for 2016 and onward.</div>');

                    }
                },
            });
        },

        getElectionURLByYear: function (year, refType) {
            $.ajax({
                url: urls.GET_ELECTION_URL_BY_YEAR,
                type: "POST",
                data: { 'year': year, 'electionType': currentElectionType, 'refType': refType },
                success: function (data) {
                    if (data.ReferencePath) {
                        $('#mapDiv_input').get(0).contentWindow.location.replace(data.ReferencePath + "?isShow=N");
                        $("#maptableButtonDiv").show();
                    }
                    else {
                        $("#maptableButtonDiv").hide();
                        $("#mapDiv").hide();
                        $("#gridDiv").show();
                    }
                },
            });
        },

        getElectionTypeByYear: function (year) {
            $.ajax({
                url: urls.GET_ELECTION_TYPES_BY_YEAR,
                type: "POST",
                data: {
                    'year': year
                }
            }).done(function(data) {
                var primary, general, special, referendum;
                for (var i = 0; i < data.length; i++) {
                    if (data[i].ElectionType === "GENERAL") {
                        $("#tabGeneral").show();
                        general = true;
                    } else if (data[i].ElectionType === "PRIMARY") {
                        $("#tabPrimary").show();
                        primary = true;
                    } else if (data[i].ElectionType === "SPECIAL") {
                        $("#tabSpecial").show();
                        special = true;
                    } else if (data[i].ElectionType === "REFERENDUMS") {
                        $("#tabReferendum").show();
                        referendum = true;
                    }
                }

                // Select the first available tab
                currentElectionType = null;
                if (general) {
                    $('#tabGeneral').trigger('click');
                } else if (primary) {
                    $('#tabPrimary').trigger('click');
                } else if (special) {
                    $('#tabSpecial').trigger('click');
                } else if (referendum) {
                    isReferendum = true;
                    $('#tabReferendum').trigger('click');
                }
            });
        }
    }

    return {
        service: methods
    };
})();

function onElectionYearClick(year) {
    if (year == 0) {
        window.open("http://clerk.house.gov/member_info/electioninfo/index.aspx");
    } else {
        var loginData = $('#isLoginValue').val();
        if (loginData != undefined) {
            isLogin = true;
            isViewMap = true;
            showResults(year);

            if (isViewMap) {
                $("#gridDiv").hide();
                $("#mapDiv").show();

                $('#showGrid').removeClass("btn-primary-sm");
                $('#showMap').addClass("btn-primary-sm");

            }
            else {
                $("#gridDiv").show();
                $("#mapDiv").hide();

            }
            $('#divHistoricalElectionResults').show();
            $('#divHistoricalVoterMaps').hide();
            $('#div6').hide();
            $('#div1').hide();
            $('#divPrint').hide();
            $('#divPrintError').hide();
            $('#div2').hide();
            $('#div3').hide();
            $('#div4').hide();
            $('#div5').hide();
            $('#divCountyContact').hide();
            $('#divsideMenuAbsenteeForm').hide();
            $('#divsideMenuMilitaryForm').hide();
            $('#divsideMenuDocumentsFroms').hide();
        }
        else {
            window.location.href = "/ENRHistorical/ElectionResults" + "?year=" + year + "&isViewMap=true";
        }
    }
}

//GetElectionTypeData
function GetElectionTypes() {
    $.ajax({
        url: urls.GET_ELECTION_TYPES,
        type: "POST",
        data: { 'year': getSelectedYear() }
    }).done(function(data) {
        $('#electionType').html('');
        var htmlData = htmlData + '<option value="0">--SELECT--</option>';
        for (var i = 0; i < data.length; i++) {
            htmlData = htmlData + '<option >' + data[i].ElectionType.toUpperCase() + '</option>';
        }
        $('#electionType').html(htmlData);
    });
}

//Filter data clear
function filterClear() {
    $('#county').val("");
    $('#office').val("Select");
    $('#party').val("Select");
    $('#filtercandidateLname').val("");
    $("#ddlElectionType").val("--SELECT--");

    global_county = null;
    global_office = null;
    global_party = null;
    global_filtercandidateLname = null;
    global_filterElectionType = null;
    pageNumber = 1;
}

function getSelectedYear() {
    var parsed = parseInt($('#drpElectionYears option:selected').text());
    if (isNaN(parsed))
        return null;
    else
        return parsed;
}

//Clear Referendum filter data
function clearReferendumFilter() {
    $('#referendumCounty').val("");
    $('#electionType').val(0);
    global_ref_county = null;
    global_ref_Electiontype = null;
    getReferendums(true);
}

//General & Primary Tab Click 
function onTabSelected(selectedTab) {
    
    if (currentElectionType === selectedTab) {
        // Already on selected tab, no update required.
        return;
    }

    currentElectionType = selectedTab;

    if (currentElectionType === "Referendums") {
        onReferendumsTabClick();
    } else {
        onElectionTabClick();
    }
}

function onElectionTabClick() {
    clearAllFilters();
    setDefaultSort();

    pageNumber = 1;
    getElectionData();
}

/**
 * Load Referendums for the selected year and displays the table after data is loaded.
 */
function onReferendumsTabClick() {
    GetElectionTypes();

    // Hide general/primary election table
    $electionTable.hide();

    // Display Referendums table once data is loaded
    var a1 = getReferendums(true);

    $referendumTable.css('visibility', 'hidden');
    $.when(a1).done(function () { $referendumTable.css('visibility', 'visible').hide().fadeIn(); });
}

/**
 * Make an ajax call to get Referendums data.
 * @returns The jqXHR promise object 
 */
function getReferendums(setPageNumber) {
    isReferendum = true;
    return $.ajax({
        url: urls.GET_REFERENDUMS_DATA,
        type: "POST",
        data: { 'year': getSelectedYear(), 'pageNumber': pageNumber, 'sortBy': global_sortBy, 'sortDir': global_sortDir, 'county': global_ref_county, 'electionType': global_ref_Electiontype },
        success: function (data) {
            displayReferendums(data);
            if (data.length > 0) {
                if (setPageNumber) {
                    historicalResults.service.setPageNumber(noOfPagesVisible, data[0].pagesCount);
                    $("#referendumPagination .liPrevious").next().find('a.page-link-num').addClass('active');
                }
            }
        }
    });
}

//Display referendums data
function displayReferendums(data) {
    showElectionReferendumGrid();

    var htmlPage = '';
    $('#lblNoElectionData').hide();
    if (data.length > 0) {
        for (var i = 0; i < data.length; i++) {
            htmlPage = htmlPage + '<tr>';
            htmlPage = htmlPage + '<td> ' + data[i].ReferendumType + '</td>';
            if (data[i].County == null || data[i].County == '') {
                if (data[i].IsPDF == 1 && $("#referendumCounty option:selected").text().search('-- ALL COUNTIES --') == -1) {
                    $('#threfCounty').show();
                    htmlPage = htmlPage + '<td> ' + '' + '</td>';
                } else {
                    $('#threfCounty').hide();
                }
            } else {
                $('#threfCounty').show();
                htmlPage = htmlPage + '<td> ' + data[i].County + '</td>';
            }
            htmlPage = htmlPage + '<td> ' + data[i].District + '</td>';
            htmlPage = htmlPage + '<td> ' + data[i].ElectionType + '</td>';

            if (data[i].IsPDF) {
                htmlPage = htmlPage + '<td><a href=\\PublicContent' + data[i].Link + ' target="_blank">' + data[i].Question + '</a></td>';
            } else {
                htmlPage = htmlPage + '<td> ' + data[i].Question + '</td>';
            }

            if (data[i].PositiveResult == null && data[i].NegativeResult == null) {
                htmlPage = htmlPage + '<td> </td>';
                htmlPage = htmlPage + '<td> </td>';
            } else {
                htmlPage = htmlPage + '<td> ' + data[i].PositiveResult + '</td>';
                htmlPage = htmlPage + '<td> ' + data[i].NegativeResult + '</td>';
            }
            htmlPage = htmlPage + '</tr>';
            $('#referendumstbodyData').html(htmlPage);
        }
        $('#divReferendumData').show();
        $('#lblRefNofilterdata').hide();
    }
}


// Display Candidate data
function displayCandidateGrid(data, htmlData) {
    showCandidateGrid();
    $('#lblNofilterdata').hide();
    $('#divInnerCandidateGrid').show();
    $('#lblNoresult').hide();

    var nTypes = [];
    for (var i = 0; i < data.length; i++) {
        htmlData = htmlData + '<tr>';
        if (data[i].County == null || data[i].County == '') {
            $('#thcCounty').hide();
        }
        else {
            $('#thcCounty').show();
            htmlData = htmlData + '<td> ' + data[i].County + '</td>';
        }

        htmlData = htmlData + '<td> ' + data[i].CandidateName + '</td>';
        htmlData = htmlData + '<td> ' + data[i].Office + '</td>';
        htmlData = htmlData + '<td>' + data[i].ElectionType + '</td>';
        htmlData = htmlData + '<td> ' + data[i].Party + '</td>';
        htmlData = htmlData + '<td> ' + data[i].District + '</td>';
        htmlData = htmlData + '<td> ' + data[i].Votes + '</td>';
        htmlData = htmlData + '</tr>';

        $('#candidatetbodyData').html(htmlData);

        if (nTypes.indexOf(data[i].PrimaryGeneral) == -1) {
            nTypes.push(data[i].PrimaryGeneral);
        }
    }

    if (isMainFilter) {
        global_CandidateSearch_ElectionTypes = nTypes;
        BindElectionType();
    }

}

function BindElectionType() {
    var data = global_CandidateSearch_ElectionTypes;
    var htmlElectionType = '<option>--SELECT--</option>';
    for (var i = 0; i < data.length; i++) {
        htmlElectionType = htmlElectionType + '<option value=' + data[i] + '>' + data[i] + '</option>';
    }
    $("#ddlElectionType").html(htmlElectionType);
}

// Display Election data
function displayElectionGrid(data, htmlData) {
    showElectionReferendumGrid();

    historicalResults.service.closePopup();
    $('#spanElectionType').html('INDIANA ' + data[0].ElectionType);
    globale_Filtered_ElectionType = data[0].ElectionType;
    if (data[0].VoterTurnOutLink == null || data[0].VoterTurnOutLink == '') {
        $('#aVoterTurnOut').hide();
    } else {
        $('#aVoterTurnOut').show();
        $('#aVoterTurnOut').prop('href', "\\PublicContent" + data[0].VoterTurnOutLink);
        //$('#spanUpdatedDate').prop('href', "\\PublicContent" + data[0].VoterTurnOutLink);
    }

    if (data[0].MoreInfoPath == null || data[0].MoreInfoPath == '') {
        $('#aFinalresults').hide();
        $('#spnFinalresults').hide();
    } else {
        var ResultURL = "http://docs.google.com/gview?url=" + window.location.origin + "/PublicContent" + data[0].MoreInfoPath + "&embedded=true";
        $('#aFinalresults').show();
        $('#spnFinalresults').show();
        $('#aFinalresults').prop('href', ResultURL.replace(/ /g, ''));
    }

    $('#gridDiv').hide();
    if (currentElectionType === 'Special') {
        for (var i = 0; i < data.length; i++) {
            $('#lblNoElectionData').hide();
            $('#gridDiv').show();
            $('#lblNofilterdata').hide();
            htmlData = htmlData + '<tr>';
            htmlData = htmlData + '<td><a href=' + "\\PublicContent" + data[i].SpecialElection + ' target="_blank">View PDF</a></td>';
            htmlData = htmlData + '<td></td>';
            htmlData = htmlData + '<td></td>';
            htmlData = htmlData + '<td></td>';
            htmlData = htmlData + '<td></td>';
            htmlData = htmlData + '</tr>';
            $('#tbodyData').html(htmlData);
        }
    } else {
        if (data[0].AdditionalDocumentList != null && data[0].AdditionalDocumentList !== "") {
            $('#spnAdditionalDocs').show();
            var htmlContent = '';
            for (var i = 0; i < data[0].AdditionalDocumentList.length; i++) {
                var document = data[0].AdditionalDocumentList[i];
                htmlContent += "<a href='\\PublicContent" + document.AdditionalDocument + "' class=\"link-xs\" target=\"_blank\">" + document.AdditionalDocumentLabel + "</a> &nbsp;&nbsp;&nbsp;";
            }
            $('#spnAdditionalDocs').html(htmlContent);
        } else {
            $('#spnAdditionalDocs').hide();
        }

        for (var i = 0; i < data.length; i++) {
            $('#lblNoElectionData').hide();
            $('#gridDiv').show();
            $('#lblNofilterdata').hide();
            htmlData = htmlData + '<tr>';
            if (data[i].County == null || data[i].County == '') {
                $('#thCounty').hide();
            } else {
                $('#thCounty').show();
                htmlData = htmlData + '<td> ' + data[i].County + '</td>';
            }

            htmlData = htmlData + '<td> ' + data[i].Office + '</td>';
            htmlData = htmlData + '<td> ' + data[i].CandidateName + '</td>';
            htmlData = htmlData + '<td> ' + data[i].Party + '</td>';
            htmlData = htmlData + '<td> ' + data[i].District + '</td>';
            htmlData = htmlData + '<td> ' + data[i].Votes + '</td>';
            htmlData = htmlData + '</tr>';
            $('#tbodyData').html(htmlData);
        }
    }
}

function hideElectionTabs() {
    $("#tabGeneral").hide();
    $("#tabPrimary").hide();
    $("#tabSpecial").hide();
    $("#tabReferendum").hide();
}

function clearAllFilters() {
    $('#county').val("");
    $('#office').empty();
    $('#party').empty();
    $('#filtercandidateLname').val("");
    $('#referendumCounty').val("");
    $('#electionType').val(0);
    $("#ddlElectionType").val(0);

    global_county = null;
    global_office = null;
    global_party = null;
    global_filtercandidateLname = null;
    global_filterElectionType = null;
    global_ref_county = null;
    global_ref_Electiontype = null;
}

function setDefaultSort() {
    global_sortBy = '';
    global_sortDir = '';
}

function getElectionTabs() {
    isMainFilter = true;
    hideElectionTabs();
    clearAllFilters();
    setDefaultSort();
    pageNumber = 1;

    var electionYear = getSelectedYear();
    if (electionYear != null) {
        historicalResults.service.getElectionTypeByYear(electionYear);
    } else {
        getElectionData();
    }
}

function getElectionData() {
    $electionTable.css('visibility', 'hidden');

    if (($drpElectionYears.val() === '' || $drpElectionYears.val() === '-1') && $candidateLname.val() === '') {//Validating
        $error_ApplyFilter.show().text("Error: Select one or more filter(s).");
        $error_CandidateLname.hide();
    } else if ($candidateLname.val() && $candidateLname.val().length > 0 && $candidateLname.val().length < 2) {
        $error_CandidateLname.show().text("Error: Candidate Last Name should be minimum of 2 characters.");
        $error_ApplyFilter.hide();
    } else {
        $error_ApplyFilter.hide();
        $error_CandidateLname.hide();

        isReferendum = false;
        // Display Election Results table once all data is loaded
        var electionYear = $('#drpElectionYears option:selected').text();
        var candidateLastName = $('#candidateLname').val();
        var a1 = historicalResults.service.getElectionData(electionYear, candidateLastName, pageNumber, global_sortBy, global_sortDir, true);
        var a2 = historicalResults.service.getElectionLastUpdateDate(electionYear);
        $.when(a1, a2).done(function () { $electionTable.css('visibility', 'visible').hide().fadeIn(); });
        if (!(candidateLastName !== '' && electionYear === 'Select Year')) {
            historicalResults.service.getElectionURLByYear(electionYear, "URL");
        }
    }
}

function setSortOrder(ele) {
    var allSortFields = $('em.sortingColumn');

    var $iEle = $(ele).find('em');
    var _sortOrder = '';

    var currentSortElement = $iEle.prop('id');

    if ($iEle.hasClass('fa-caret-up')) {
        _sortOrder = 'DESC';
        $iEle.removeClass('fa-caret-up');
        $iEle.addClass('fa-caret-down');
    } else if ($iEle.hasClass('fa-caret-down')) {
        _sortOrder = 'ASC';
        $iEle.removeClass('fa-caret-down');
        $iEle.addClass('fa-caret-up');
    } else {
        _sortOrder = 'ASC';
        $iEle.addClass('fa-caret-up');
    }

    $.each(allSortFields, function(i, v) {
        if (currentSortElement != v.id) {
            $('#' + v.id).removeClass('fa-caret-down');
            $('#' + v.id).removeClass('fa-caret-up');
        }
    });

    global_sortBy = $iEle.data('sortby');
    global_sortDir = _sortOrder;

    ref_sortBy = $iEle.data('sortby');;
    ref_sortDir = _sortOrder;

    if (isReferendum) {
        getReferendums();
    } else {
        historicalResults.service.getElectionData($('#drpElectionYears option:selected').text(),
            $('#candidateLname').val(), pageNumber, global_sortBy, global_sortDir, false);
    }
}

//Get Offices
function ddlCounty() {
    var selectedText = "-- ALL COUNTIES --"; //$('#county option:selected').text();
    $.ajax({
        url: urls.GET_OFFICES,
        type: "POST",
        data: {
            'year': $('#drpElectionYears option:selected').text(),
            'countyName': selectedText
        }
    }).done(function(data) {
        var htmlOffice = '';
        for (var i = 0; i < data.length; i++) {
            htmlOffice = htmlOffice + '<option value=' + data[i].Office + '>' + data[i].Office + '</option>';
        }
        $('#office').html(htmlOffice);
    });
}

//Get Parties
function ddlOffice() {
    var selectedText = "-- ALL COUNTIES --"; //$('#county option:selected').text()
    $.ajax({
        url: urls.GET_PARTIES,
        type: "POST",
        data: {
            'year': $('#drpElectionYears option:selected').text(),
            'countyName': selectedText,
            'office': $('#office option:selected').text()
        }
    }).done(function(data) {
        var htmlParty = '';
        for (var i = 0; i < data.length; i++) {
            htmlParty = htmlParty + '<option value=' + data[i].PartyLetter + '>' + data[i].Party + '</option>';
        }
        $('#party').html(htmlParty);
    });
}

// Get Default Values for Office and Party
function LoadDefaultDropdownData() {
    if ($('#office option:selected').text() === 'Select Office' || $('#office option:selected').text() === '')
        ddlCounty();
    if ($('#party option:selected').text() === 'Select Party' || $('#party option:selected').text() === '')
        ddlOffice();
}

//Get Filtered Data
function getFilteredData() {
    isMainFilter = false;
    global_county = $("#county option:selected").map(function() { return this.text; }).get().join(',');
    global_office = $('#office option:selected').text();
    global_party = $('#party').val();
    global_filtercandidateLname = $('#filtercandidateLname').val();
    if ($candidateLname.val() &&
        $candidateLname.val().length > 0 &&
        $('#drpElectionYears option:selected').text() === 'Select Year' &&
        $('#ddlElectionType option:selected').text() !== '--SELECT--') {
        global_filterElectionType = $('#ddlElectionType option:selected').text();
    } else {
        global_filterElectionType = null;
    }

    pageNumber = 1;
    reloadElectionData(true);
    
    isFiltered = true;
    historicalResults.service.closePopup();
}

/**
 * Reload election data when changing filters or the page number
 */
function reloadElectionData(setPageNumbers = false) {
    historicalResults.service.getElectionData($('#drpElectionYears option:selected').text(), $('#candidateLname').val(), pageNumber, global_sortBy, global_sortDir, setPageNumbers);
}

function getReferendumFilteredData() {
    var selectedCounty = $('#referendumCounty option:selected').text() === '-- ALL COUNTIES --'
        ? ""
        : $("#referendumCounty option:selected").map(function () { return this.text; }).get().join(',');

    var selectedElectiontype = $('#electionType').val() == '0' ? "" : $('#electionType').val();

    global_ref_county = selectedCounty;
    global_ref_Electiontype = selectedElectiontype;

    $.ajax({
        url: '/ENRHistorical/GetReferendums/',
        type: "POST",
        data: {
            'year': $('#drpElectionYears option:selected').text(),
            'pageNumber': ref_Pagenumber,
            'sortBy': ref_sortBy,
            'sortDir': ref_sortDir,
            'county': selectedCounty,
            'electionType': selectedElectiontype
        },
        success: function (data) {
            if (data.length > 0) {
                historicalResults.service.closePopup();
                displayReferendums(data);
                if (data.length > 0) {
                    historicalResults.service.setPageNumber(noOfPagesVisible, data[0].pagesCount);
                    $('#referendumPagination .liPrevious').next().find('a.page-link.page-link-num').addClass('active');
                }
            } else {
                $('#lblRefNofilterdata').show();

                if ($('#referendumCounty option:selected').text() != '-- ALL COUNTIES --') {
                    if ($('#referendumCounty option:selected').text().search('-- ALL COUNTIES --') == -1) {
                        if ($("#referendumCounty option:selected").map(function () { return this.text }).get().join(',').search(',') == -1) {
                            $('#lblRefNofilterdata').html('No results returned from ' + $("#referendumCounty option:selected").map(function () { return this.text }).get().join(',') + ' County.');
                        } else {
                            $('#lblRefNofilterdata').html('No results returned from ' + $("#referendumCounty option:selected").map(function () { return this.text }).get().join(',') + ' Counties.');
                        }
                    } else {
                        $('#lblRefNofilterdata').html('No results returned.');
                    }
                } else {
                    $('#lblRefNofilterdata').html($('#electionType option:selected').text() + ' did not have data.');
                }
                $('#divReferendumData').hide();
                historicalResults.service.closePopup();
            }
        }
    });
}

function displayevent() {
    $("#primaryPagination li").has('a.page-link.page-link-num').each(function () {
        if ($(this).css('display') === 'none') {
            $(this).removeClass('selected');
        } else {
            $(this).addClass('selected');
        }
    });

    $("#candidatePagination li").has('a.page-link.page-link-num').each(function () {
        if ($(this).css('display') === 'none') {
            $(this).removeClass('selected');
        } else {
            $(this).addClass('selected');
        }
    });
}

//Gets the url parameters by name.
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

//Shows the results for selected year.
function showResults(sender) {
    var year;
    if (isLogin) {
        year = sender;
    } else {
        year = getParameterByName("year", window.location.href);
    }

    if (year != null) {
        $('#drpElectionYears').val(year);
        $('#drpElectionYears').trigger('change');
        getElectionTabs();
    }
}

function EnableHistoricalThemeParameters() {
    //Load based on theme
    var darkThemeEnable = sessionStorage.getItem('darkThemeEnable');
    if (darkThemeEnable == 1) {
        $('#imgReferendumGridFilter').attr('src', '/Content/Images/u3250white.png');
        $('#imgElectionDataGridFilter').attr('src', '/Content/Images/u3250white.png');
        $('#imgcandidateResultFilter').attr('src', '/Content/Images/u3250white.png');
        $('#imgcandidateResultcsv').attr('src', '/Content/Images/csv_export_u3152white.png');
        $('#imgReferendumGridCsv').attr('src', '/Content/Images/csv_export_u3152white.png');
        $('#imgElectionDataGridCsv').attr('src', '/Content/Images/csv_export_u3152white.png');
    }
    else {
        $('#imgReferendumGridFilter').attr('src', '/Content/Images/u3250.png');
        $('#imgElectionDataGridFilter').attr('src', '/Content/Images/u3250.png');
        $('#imgcandidateResultFilter').attr('src', '/Content/Images/u3250.png');
        $('#imgcandidateResultcsv').attr('src', '/Content/Images/csv_export_u3152.png');
        $('#imgReferendumGridCsv').attr('src', '/Content/Images/csv_export_u3152.png');
        $('#imgElectionDataGridCsv').attr('src', '/Content/Images/csv_export_u3152.png');
    }
}

$(document).ready(function() {
    EnableHistoricalThemeParameters();
    hideAllGrids();

    //Dark theme fix.
    $('#error_CandidateLname').hide();
    $('#error_ApplyFilter').hide();

    //DOM elements
    $drpElectionYears = $('#drpElectionYears');
    $btnApplyFilter = $('#btnApplyFilter');
    $candidateLname = $('#candidateLname');
    $error_ApplyFilter = $('#error_ApplyFilter');
    $error_CandidateLname = $('#error_CandidateLname');
    $aClear = $('#aClear');
    $divPriorElectionsLink = $('#divPriorElectionsLink');

    $drpElectionYears.html('');
    $divElectionMapYears = $("#divElectionMapYears");
    $divElectionMapYears.html('');

    $electionTable = $('#electionTable');
    $referendumTable = $('#referendumTable');

    //Election year change.
    $drpElectionYears.on('change', function () {
        if ($drpElectionYears.val() === '0') {
            $candidateLname.val('');
            $candidateLname.attr('disabled', 'disabled');
            $btnApplyFilter.attr('disabled', 'disabled');
            $divPriorElectionsLink.show();
            hideAllGrids();
            hideElectionTabs();
        } else {
            $error_ApplyFilter.hide();
            $divPriorElectionsLink.hide();
            $candidateLname.removeAttr('disabled');
            $btnApplyFilter.removeAttr('disabled');
        }
    });

    //Load Election years.
    $.ajax({
        type: "GET",
        contentType: 'application/json; charset=utf-8',
        url: urls.GET_ELECTION_YEARS
    }).done(function(data) {
        $drpElectionYears.append('<option value="-1">Select Year</option>');
        $.each(data, function(i, v) { $drpElectionYears.append('<option>' + v.ElectionYear + '</option>'); });
        $drpElectionYears.append('<option value="0">Prior to 2002</option>');

        showResults(); //Shows the results if year is selected from home page.
    });

    //DOM Events

    //UI events Start.

    if (isViewMap) {
        $("#gridDiv").hide();
        $("#mapDiv").show();

        $('#showGrid').removeClass("btn-primary-sm");
        $('#showMap').addClass("btn-primary-sm");
    } else {
        $("#gridDiv").show();
        $("#mapDiv").hide();
    }

    $("#showGrid").on('click', function () {
        $("#gridDiv").show();
        $("#mapDiv").hide();
    });

    $("#showMap").on('click', function () {
        $("#gridDiv").hide();
        $("#mapDiv").show();
    });

    $(".fbutton").on('click', function (e) {
        $(this).addClass("btn-primary-sm").siblings().removeClass("btn-primary-sm");
    });
    //UI events End.

    function hasStartDot(id) {
        var _result = false;
        $(id).each(function (i, v) {
            if ($(v).hasClass("liStartDot")) {
                _result = true;
            }
        });

        return _result;
    }

    function hasEndDot(id) {
        var _result = false;
        $(id).each(function (i, v) {
            if ($(v).hasClass("liEndDot")) {
                _result = true;
            }
        });

        return _result;
    }

    // Primary grid pagination events 
    $("#primaryPagination .liNext").on('click', function (e) {
        onNextClick(e, "#primaryPagination", reloadElectionData);
    });

    $("#primaryPagination .liPrevious").on('click', function (e) {
        onPreviousClick(e, "#primaryPagination", reloadElectionData);
    });

    $("#primaryPagination").on('click', 'li a.page-link.page-link-num', function (e) {
        onPageNumberClick(e, "#primaryPagination", reloadElectionData);
    });

    // Candidate grid pagination events 
    $("#candidatePagination .liNext").on('click', function (e) {
        onNextClick(e, "#candidatePagination", reloadElectionData);
    });

    $("#candidatePagination .liPrevious").on('click', function (e) {
        onPreviousClick(e, "#candidatePagination", reloadElectionData);
    });

    $("#candidatePagination").on('click', 'li a.page-link.page-link-num', function (e) {
        onPageNumberClick(e, "#candidatePagination", reloadElectionData);
    });

    // Referendum grid pagination events 
    $("#referendumPagination .liNext").on('click', function (e) {
        onNextClick(e, "#referendumPagination", () => getReferendums(false));
    });

    $("#referendumPagination .liPrevious").on('click', function (e) {
        onPreviousClick(e, "#referendumPagination", () => getReferendums(false));
    });

    $("#referendumPagination").on('click', 'li a.page-link.page-link-num', function (e) {
        onPageNumberClick(e, "#referendumPagination", () => getReferendums(false));
    });



    function onNextClick(e, paginationId, reloadAction) {
        e.preventDefault();

        var nextNumber = pageNumber + 1;
        if (nextNumber > global_maxPages) {
            return;
        }

        if (pageNumber < global_maxPages) {
            var hasNextPageNumber = ($(paginationId).find('a.page-link.page-link-num.pagnum-' + nextNumber).length > 0) ? true : false;
            if (hasNextPageNumber) {
                $(paginationId).find('a.page-link.page-link-num.active').removeClass('active').parent()
                    .next().find('a.page-link.page-link-num').addClass('active');
            } else {
                $(paginationId).find('a.page-link.page-link-num.active').removeClass('active').parent()
                    .after(generatePageLink(pageNumber + 1));
                $(paginationId).find('a.page-link.page-link-num.pagnum-' + (pageNumber + 1))
                    .addClass('active');

                if (!hasStartDot(paginationId + ' li')) {
                    $(paginationId).find('a.page-link.page-link-num').eq(0).parent().remove();
                    $(paginationId).find('.liPrevious').after(generatePageLink(1) + '<li class="page-item liStartDot"><span class="page-link">...</span></li>');
                } else {
                    $(paginationId).find('.liStartDot').next().remove();
                }
            }
            pageNumber++;
            reloadAction();
        }

        if (nextNumber === global_maxPages) {
            $(paginationId).find('.liEndDot').remove();
            $(paginationId).find('.liStartDot').next().remove();
            $(paginationId).find('a.page-link.page-link-num.active').removeClass('active');
            $(paginationId).find('a.page-link.page-link-num.pagnum-' + global_maxPages).addClass('active');
        }
    }

    function onPreviousClick(e, paginationId, reloadAction) {
        e.preventDefault();

        var previousNumber = pageNumber - 1;
        if (previousNumber < 1) {
            return;
        }

        if (pageNumber > 1) {
            var hasPreviousPageNumber = $(paginationId).find('a.page-link.page-link-num.pagnum-' + previousNumber).length > 0;
            if (hasPreviousPageNumber) {
                $(paginationId).find('a.page-link.page-link-num.active').removeClass('active').parent().prev().find('a.page-link.page-link-num').addClass('active');
            } else {
                $(paginationId).find('a.page-link.page-link-num.active').removeClass('active').parent().before(generatePageLink(previousNumber));
                $(paginationId).find('a.page-link.page-link-num.pagnum-' + previousNumber).addClass('active');

                if (!hasEndDot(paginationId + ' li')) {
                    $(paginationId).find('a.page-link.page-link-num:last').eq(0).parent().remove();
                    $(paginationId).find('.liNext').before('<li class="page-item liEndDot"><span class="page-link">...</span></li>'
                        + generatePageLink(global_maxPages));
                } else {
                    $(paginationId).find('.liEndDot').prev().remove();
                }
            }
            pageNumber--;
            reloadAction();
        }

        if (previousNumber === 1) {
            $(paginationId).find('.liStartDot').remove();
            $(paginationId).find('.liEndDot').prev().remove();
            $(paginationId).find('a.page-link.page-link-num.active').removeClass('active');
            $(paginationId).find('a.page-link.page-link-num.pagnum-' + 1).addClass('active');
        }
    }

    function onPageNumberClick(e, paginationId, reloadAction) {
        e.preventDefault();

        clearPaginationActive(paginationId);
        $(e.target).addClass('active');
        pageNumber = $(e.target).data("pagnum");
        reloadAction();

        if (pageNumber == 1) {
            if (hasStartDot(paginationId + ' li')) {
                $(paginationId).find('.liStartDot').remove();
                $(paginationId).find('.liEndDot').remove();
                historicalResults.service.setPageNumber(noOfPagesVisible, global_maxPages);
                $(paginationId).find('.liPrevious').next().find('a.page-link.page-link-num').addClass('active');
            }
        }
        if (pageNumber == global_maxPages) {
            if (hasEndDot(paginationId + ' li')) {
                $(paginationId).find('.liStartDot').remove();
                $(paginationId).find('.liEndDot').remove();

                var pages = generatePageLink(1);
                pages += '<li class="page-item liStartDot"><span class="page-link">...</span></li>';
                var _pagesFrom = (global_maxPages - noOfPagesVisible) + 1;
                for (var i = _pagesFrom; i <= global_maxPages; i++) {
                    pages += generatePageLink(i);
                }
                $(paginationId).find('li.page-item.num').remove();
                $(paginationId).find('.liPrevious').after(pages);
                $(paginationId).find('.liNext').prev().find('a.page-link.page-link-num').addClass('active');
            }
        }
    }

    function clearPaginationActive(navigationId) {
        var activePages = $(navigationId + ' li a.page-link.page-link-num.active');

        $.each(activePages, function () {
            activePages.removeClass('active');
        });

    }
});
//DOM Events End.

function generatePageLink(pageIndex) {
    return '<li class="page-item num"><a class="page-link page-link-num pagnum-' + pageIndex + '" data-pagnum="' + pageIndex + '" href="#" aria-label="Page ' + pageIndex + '">' + pageIndex + '</a></li>';
}

function hideAllGrids() {
    $('#divCandidateGrid').hide();
    $('#divElectionGrid').hide();
}

function showCandidateGrid() {
    $('#divCandidateGrid').show();
    $('#divElectionGrid').hide();
}

function showElectionReferendumGrid() {
    $('#divElectionGrid').show();
    $('#divCandidateGrid').hide();
}

//Clear click.
function onClearClick(e) {
    e.preventDefault();
    $drpElectionYears.val('-1');
    $candidateLname.val('');
    $candidateLname.parent().removeClass('has-value').removeClass('is-focused');
    $candidateLname.removeAttr('disabled');
    $btnApplyFilter.removeAttr('disabled');
    $divPriorElectionsLink.hide();
    $error_ApplyFilter.hide();
    $error_CandidateLname.hide();
    pageNumber = 1;
    clearAllFilters();
    hideElectionTabs();
    hideAllGrids();
    setDefaultSort();
    $("#gridDiv").show();
    $("#mapDiv").hide();
    $('#showGrid').addClass("btn-primary-sm");
    $('#showMap').removeClass("btn-primary-sm");
}

//Export CSV click.
function exportElectionsToCsv(e) {
    e.preventDefault();

    var params = getQueryString({
        year: getSelectedYear(),
        electionType: currentElectionType,
        candidateName: $('#candidateLname').val(),
        county: global_county,
        office: global_office,
        party: global_party,
        sortBy: global_sortBy,
        sortDir: global_sortDir,
        filterCandidateName: global_filtercandidateLname,
        filterElectionType: (global_filterElectionType == null ? false : true)
    });
    window.location.href = urls.EXPORT_ELECTIONS_TO_CSV + "?" + params.toString();
}

function exportCandidatesToCsv(e) {
    e.preventDefault();

    var params = getQueryString({
        year: getSelectedYear(),
        electionType: currentElectionType,
        candidateName: $('#candidateLname').val(),
        county: global_county,
        office: global_office,
        party: global_party,
        sortBy: global_sortBy,
        sortDir: global_sortDir,
        filterCandidateName: global_filtercandidateLname,
        filterElectionType: (global_filterElectionType == null ? false : true)
    });
    window.location.href = urls.EXPORT_CANDIDATES_TO_CSV + "?" + params.toString();
}

//Export Referendum CSV click.
function exportReferendumsToCsv(e) {
    e.preventDefault();

    var selectedCounty = $('#referendumCounty option:selected').text() === '-- ALL COUNTIES --'
        ? ""
        : $("#referendumCounty option:selected").map(function () { return this.text; }).get().join(',');

    var params = getQueryString({
        year: getSelectedYear(),
        sortBy: global_sortBy,
        sortDir: global_sortDir,
        county: selectedCounty
    });
    window.location.href = urls.EXPORT_REFERENDUMS_TO_CSV + "?" + params.toString();
}

function getQueryString(oParameters) {
    for (key in oParameters) {
        if (oParameters[key] == null) {
            delete oParameters[key];
        }
    }
    return $.param(oParameters);
}
