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

    // Deals with the AJAX for showing add property/valuation form
    $(".js-add-property").click(function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#base-large-modal").modal("show");
            },
            success: function (data) {
                $("#base-large-modal .modal-dialog").html(data.html_modal);
                var api_key = $('#base-large-modal #id_get_address_api_key').text().slice(1, -1);

                $('.get-address-select2').select2({
                    dropdownParent: $("#base-large-modal"),
                    width: '100%',
                    minimumInputLength: 4,
                    placeholder: "Type The Postcode",
                    language: {
                        inputTooShort: function () {
                            return '';
                        }
                    },
                    ajax: {
                        url: function (params) {
                            if (params.term) return 'https://api.getaddress.io/suggest/' + params.term;
                            return '';
                        },
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                'api-key': api_key
                            };
                            return query;
                        },
                        processResults: function (data) {
                            var results = [];

                            if (data.suggestions && data.suggestions.length > 0) {

                                for (var i = 0; i < data.suggestions.length; i++) {
                                    var suggestion = data.suggestions[i];
                                    var result = {
                                        id: suggestion.id,
                                        text: suggestion.address
                                    }
                                    results.push(result);
                                }
                            }

                            return {
                                results: results
                            };
                        }
                    }
                });
            }
        });
    });

    // Deals with the get address request
    $('#base-large-modal').on('change', 'select', function () {
        var option = $(".get-address-select2 option:selected")
        var api_key = $('#base-large-modal #id_get_address_api_key').text().slice(1, -1);
        var id = option.attr("value");
        $.get('https://api.getaddress.io/get/' + id, {
            'api-key': api_key
        }, function (address, status) {
            $("#id_address_line_1").val(address["line_1"]);
            $("#id_address_line_2").val(address["line_2"]);
            $("#id_town").val(address["town_or_city"]);
            $("#id_postcode").val(address["postcode"]);
        });
    });

});