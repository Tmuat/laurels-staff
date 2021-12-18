$(document).ready(function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    $('#query-search').on("click", function() {
        var currentUrl = new URL(window.location);

        var selectedVal = $("#tout-query").val();

        currentUrl.searchParams.delete("page");
        currentUrl.searchParams.set("query", selectedVal);

        window.location.replace(currentUrl);
    })

    function dataTaken() {
        $("#base-large-modal").find("#add-button").addClass("d-none");
        $("#base-large-modal").find("#alert-info-div").removeClass("d-none");
        $("#base-large-modal").find("#alert-div").removeClass("d-none");

        $("#base-large-modal").find("#id_address_line_1").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_address_line_2").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_town").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_county").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_postcode").attr("disabled", true).removeAttr("required");
    };

    function dataNotTaken() {
        $("#base-large-modal").find("#add-button").removeAttr("disabled");
        $("#base-large-modal").find("#alert-info-div").addClass("d-none");
        $("#base-large-modal").find("#alert-div").addClass("d-none");
        $("#base-large-modal").find("#add-button").removeClass("d-none");

        $("#base-large-modal").find("#id_address_line_1").removeAttr("disabled");
        $("#base-large-modal").find("#id_address_line_2").removeAttr("disabled");
        $("#base-large-modal").find("#id_town").removeAttr("disabled");
        $("#base-large-modal").find("#id_county").removeAttr("disabled");
        $("#base-large-modal").find("#id_postcode").removeAttr("disabled");
    };

    function initialAddressSelectTwo() {
        var api_key = $('#base-large-modal #id_get_address_api_key').text().slice(1, -1);
        $('.get-address-select2').select2({
            dropdownParent: $("#base-large-modal"),
            width: '100%',
            minimumInputLength: 4,
            placeholder: "Postcode or Address Line 1",
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
    };

    // Deals with the get address request
    $('#base-large-modal').on('change', 'select', function () {
        var option = $(".get-address-select2 option:selected")
        var api_key = $('#base-large-modal #id_get_address_api_key').text().slice(1, -1);
        var id = option.attr("value");
        $.get('https://api.getaddress.io/get/' + id, {
            'api-key': api_key
        }, function (address) {
            $("#id_address_line_1").val(address["line_1"]);
            $("#id_address_line_2").val(address["line_2"]);
            $("#id_town").val(address["town_or_city"]);
            $("#id_county").val(address["county"]);
            $("#id_postcode").val(address["postcode"]);
            $.ajax({
                url: '/touting/tout-list/validate/property/',
                data: {
                    'address_line_1': address["line_1"],
                    'address_line_2': address["line_2"],
                    'postcode': address["postcode"],
                },
                dataType: 'json',
                success: function (data) {
                    if (data.is_taken) {
                        $("#alert-div").html(data.html_alert);
                        dataTaken()
                    } else {
                        dataNotTaken()
                    };
                }
            });
        });
    });

    function initialLargeStaticAddressSelectTwo() {
        var api_key = $('#base-large-static-modal #id_get_address_api_key').text().slice(1, -1);
        $('.get-address-select2-large-static').select2({
            dropdownParent: $("#base-large-static-modal"),
            width: '100%',
            minimumInputLength: 4,
            placeholder: "Postcode or Address Line 1",
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
    };

    // Deals with the get address request - large static
    $('#base-large-static-modal').on('change', '.get-address-select2-large-static', function () {
        var option = $(".get-address-select2-large-static option:selected")
        var api_key = $('#base-large-static-modal #id_get_address_api_key').text().slice(1, -1);
        var id = option.attr("value");
        $.get('https://api.getaddress.io/get/' + id, {
            'api-key': api_key
            }, function (address) {
                $("#id_ll_address_line_1").val(address["line_1"]);
                $("#id_ll_address_line_2").val(address["line_2"]);
                $("#id_ll_town").val(address["town_or_city"]);
                $("#id_ll_county").val(address["county"]);
                $("#id_ll_postcode").val(address["postcode"]);
            }
        );
    });

    function initialAreaSelectTwo() {
        $('#id_area').select2({
            dropdownParent: $("#base-large-modal"),
            width: '100%',
            minimumInputLength: 2,
            placeholder: "Search Area Code",
            language: {
                inputTooShort: function () {
                    return '';
                }
            },
        });
    };

    function initialPropertySelectTwo() {
        $('#id_landlord_property').select2({
            dropdownParent: $("#base-large-static-modal"),
            width: '100%',
            minimumInputLength: 3,
            placeholder: "Search By Postcode",
            language: {
                inputTooShort: function () {
                    return '';
                }
            },
        });
    };

    // Checks the uniqueness of the area code
    $("#base-modal").on("change", "#id_area_code", function () {
        var areaCode = $(this).val();
        $.ajax({
            url: '/touting/check/area/',
            data: {
                'area_code': areaCode
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    $("#base-modal").find("#mdi-icon").removeClass("mdi-help-circle mdi-check-circle-outline").addClass("mdi-close-circle-outline");
                    $("#base-modal").find("#unique_check").addClass("text-danger border-danger");
                    $("#base-modal").find("#add-button").attr("disabled", true);
                } else {
                    $("#base-modal").find("#mdi-icon").removeClass("mdi-help-circle mdi-close-circle-outline").addClass("mdi-check-circle-outline");
                    $("#base-modal").find("#unique_check").removeClass("text-danger border-danger").addClass("border-success text-success");
                    $("#base-modal").find("#add-button").removeAttr("disabled");
                };
            }
        });
    });

    // Deals with the form submission only
    var submitForm = function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#base-modal").modal("hide");
                    location.reload();
                    $('#modal-overlay').fadeToggle(100);
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    };

    // Deals with the form submission only
    var submitLargeForm = function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    if (data.form_chain ) {
                        $("#base-large-modal").modal("hide");
                        $.ajax({
                            url: data.next,
                            type: 'get',
                            dataType: 'json',
                            success: function (data) {
                                $("#base-large-static-modal").modal("show");
                                $("#base-large-static-modal .modal-dialog").html(data.html_modal);
                                if (data.selectTwo) {
                                    initialLargeStaticAddressSelectTwo()
                                };
                                $('#modal-overlay').fadeToggle(100);
                            }
                        });
                    } else {
                        $("#base-large-modal").modal("hide");
                        location.reload();
                        $('#modal-overlay').fadeToggle(100);
                    }
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-large-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    };

    // Deals with the form submission only
    var submitLargeStaticForm = function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    if (data.form_chain ) {
                        $("#base-large-static-modal").modal("hide");
                        $.ajax({
                            url: data.next,
                            type: 'get',
                            dataType: 'json',
                            success: function (data) {
                                $("#base-large-static-modal").modal("show");
                                $("#base-large-static-modal .modal-dialog").html(data.html_modal);
                                if (data.selectTwo) {
                                    initialLargeStaticAddressSelectTwo()
                                };
                                $('#modal-overlay').fadeToggle(100);
                            }
                        });
                    } else {
                        $("#base-large-static-modal").modal("hide");
                        location.reload();
                        $('#modal-overlay').fadeToggle(100);
                    }
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-large-static-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    };

    // Deals with the form submission only
    var submitStaticForm = function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#base-static-modal").modal("hide");
                    $('#modal-overlay').fadeToggle(100);
                    location.reload();
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-static-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    };

    $("#base-static-modal").on("click", ".js-reload", function () {
        $('#modal-overlay').fadeToggle(100);
        location.reload();
    });

    // Deals with rendering the base modal
    var loadBaseModal = function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#base-modal").modal("show");
                $("#base-modal .modal-dialog").html(data.html_modal);
            }
        });
        return false;
    };

    // Deals with rendering a form with AJAX to the large modal
    var loadFormLargeModal = function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#base-large-modal").modal("show");
                $("#base-large-modal .modal-dialog").html(data.html_modal);
            }
        });
        return false;
    };

    // Deals with rendering a form with AJAX to the base static modal
    var loadFormBaseStaticModal = function () {
        $('#modal-overlay').fadeToggle(100);
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $('#modal-overlay').fadeToggle(100);
                $("#base-static-modal").modal("show");
                $("#base-static-modal .modal-dialog").html(data.html_modal);
            }
        });
    };

    // Deals with hiding a static modal
    var hideBaseLargeStaticModal = function () {
        $("#base-large-static-modal").modal("hide");
    };

    // Deals with hiding the base modal and loading a large modal
    var hideBaseModalAndLoadLargeModal = function () {
        $('#modal-overlay').fadeToggle(100);
        $("#base-modal").modal("hide");
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (data.modal == "large") {
                    $("#base-large-modal").modal("show");
                    $("#base-large-modal .modal-dialog").html(data.html_modal);
                    if (data.selectTwo) {
                        initialAddressSelectTwo();
                        initialAreaSelectTwo();
                    };
                } else if (data.modal == "large-static") {
                    $("#base-large-static-modal").modal("show");
                    $("#base-large-static-modal .modal-dialog").html(data.html_modal);
                    if (data.selectTwo) {
                        initialLargeStaticAddressSelectTwo();
                        initialPropertySelectTwo();
                    };
                }
                $('#modal-overlay').fadeToggle(100);
            }
        });
        return false;
    };

    // Add scrollable to modal
    $(".js-large-scrollable-modal").on("click", function() {
        $("#base-large-modal .modal-dialog").addClass("modal-dialog-scrollable");
    });

    // Binding functions hideBaseStaticModal
    // Links
    $("#base-modal").on("click", ".js-edit-offer-status", loadBaseModal);

    $("#base-modal").on("click", ".js-load-form", loadBaseModal);
    $("#base-modal").on("click", ".js-hide-base-load-large", hideBaseModalAndLoadLargeModal);
    $("#base-large-static-modal").on("click", ".js-hide-large-static-modal", hideBaseLargeStaticModal);

    $(".js-load-form").on("click", loadBaseModal);
    $(".js-load-large-form").on("click", loadFormLargeModal);
    $("#base-static-modal").on("click", ".js-load-static-form", loadFormBaseStaticModal);

    $("#base-modal").on("submit", ".js-submit-form", submitForm);
    $("#base-large-modal").on("submit", ".js-submit-form", submitLargeForm);
    $("#base-large-static-modal").on("submit", ".js-submit-form", submitLargeStaticForm);
    $("#base-static-modal").on("submit", ".js-submit-form", submitStaticForm);
});