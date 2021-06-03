$(document).ready(function () {
    // Deals with the re-ordering of property chain
    $("#save-property-order").click(function () {
        var order = [];
        $("div[id^='property_chain']").each(function () {
            var instance = $(this);
            order.push(instance.attr("data-pk"));
        });
        $('#order').val(order);

        var form = $("#property-chain-reorder");
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.valid) {
                    $("#saved").removeClass("d-none")
                    $("#unsaved").addClass("d-none")
                    $("#error").addClass("d-none")
                } else {
                    $("#saved").addClass("d-none")
                    $("#unsaved").addClass("d-none")
                    $("#error").removeClass("d-none")
                }
            }
        });
        return false;
    });

    // Checks for change in the property chain div
    $("#simple-dragula").on("mousedown", ".dragula-handle", function () {
        $("#saved").addClass("d-none")
        $("#error").addClass("d-none")
        $("#unsaved").removeClass("d-none")
    });

    // Deals with ajax for returning modal with property chain detail
    $("#simple-dragula").on("click", ".js-property-chain-expand", function () {
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