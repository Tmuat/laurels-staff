$(document).ready(function () {
    // Deals with the AJAX for showing property history notes
    $("#tbody-history").on("click", ".js-show-notes", function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#base-modal").modal("show");
            },
            success: function (data) {
                $("#base-modal .modal-dialog").html(data.html_modal);
            }
        });
    });

    // Deals with the AJAX for property history pagination
    $("#history").on("click", ".js-history-pagination", function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#tbody-history").html(data.html_table);
                $("#history-pagination").html(data.pagination);
            }
        });
        return false;
    });

    // Deals with the AJAX for showing the history of offers
    $("#tbody-offers").on("click", ".js-show-offers", function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#base-modal").modal("show");
            },
            success: function (data) {
                $("#base-modal .modal-dialog").html(data.html_modal);
            }
        });
    });

    // Deals with the AJAX for offers pagination
    $("#offers").on("click", ".js-offers-pagination", function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#tbody-offers").html(data.html_table);
                $("#offers-pagination").html(data.pagination);
            }
        });
        return false;
    });
});