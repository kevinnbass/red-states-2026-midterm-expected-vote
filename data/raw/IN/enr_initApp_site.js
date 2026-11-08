(function () {

    "use strict";

    angular.module("enrMapModule", []);

    angular.module("enrServicesModule", []);

    angular.module("EnrApp", [
        "d3ServiceModule", "progressBarLibServiceModule", "topoJsonServiceModule", "slick",
        "enrServicesModule", "enrMapModule", "jsonDataFetcherModule",
        "enrCircularProgressBarModule", "enrCircularProgressButtonModule", "enrTickerModule",
        "enrOfficeSelectionModule", "enrPartyBadgeModule", "enrNavBarModule", "enrDetailsPaneModule"])

        .factory("$exceptionHandler", ["errorHandler", function (errorHandler) {
            return function (exception, cause) {
                var errorMsg = exception;
                if (cause !== undefined)
                    errorMsg += "\n\n\nAdditional Info on Cause:\n" + cause;

                // Let my errorHandler address the unhandled exception.
                //errorHandler.handleError(errorMsg);
                console.log(errorMsg);
            }
        }]);
}());
