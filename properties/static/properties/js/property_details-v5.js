$(document).ready(function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      });
    
    function initialSelectTwo() {
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

    function dataTaken() {
        $("#base-large-modal").find("#add-button").addClass("d-none");
        $("#base-large-modal").find("#alert-info-div").removeClass("d-none");
        $("#base-large-modal").find("#alert-div").removeClass("d-none");
        $("#base-large-modal").find("#property-form").removeClass("js-add-property").addClass("js-add-propertyprocess");

        $("#base-large-modal").find("#id_address_line_1").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_address_line_2").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_town").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_postcode").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_property_type").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_property_style").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_number_of_bedrooms").attr("disabled", true).removeAttr("required");
        $("#base-large-modal").find("#id_tenure").attr("disabled", true).removeAttr("required");
    };

    function dataNotTaken() {
        $("#base-large-modal").find("#add-button").removeAttr("disabled");
        $("#base-large-modal").find("#alert-info-div").addClass("d-none");
        $("#base-large-modal").find("#alert-div").addClass("d-none");
        $("#base-large-modal").find("#add-button").removeClass("d-none");
        $("#base-large-modal").find("#property-form").addClass("js-add-property").removeClass("js-add-propertyprocess");

        $("#base-large-modal").find("#id_address_line_1").removeAttr("disabled");
        $("#base-large-modal").find("#id_address_line_2").removeAttr("disabled");
        $("#base-large-modal").find("#id_town").removeAttr("disabled");
        $("#base-large-modal").find("#id_postcode").removeAttr("disabled");
        $("#base-large-modal").find("#id_property_type").removeAttr("disabled");
        $("#base-large-modal").find("#id_property_style").removeAttr("disabled");
        $("#base-large-modal").find("#id_number_of_bedrooms").removeAttr("disabled");
        $("#base-large-modal").find("#id_tenure").removeAttr("disabled");
    };

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

    // Deals with the AJAX for property botes pagination
    $("#notes").on("click", ".js-notes-pagination", function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#tbody-notes").html(data.html_table);
                $("#notes-pagination").html(data.pagination);
            }
        });
        return false;
    });

    // Deals with the AJAX for showing add property/valuation form
    $(".js-add-property").click(function () {
        var instance = $(this);
        $('#modal-overlay').fadeToggle(100);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#base-large-modal").modal("show");
            },
            success: function (data) {
                $('#modal-overlay').fadeToggle(100);
                $("#base-large-modal .modal-dialog").html(data.html_modal);

                initialSelectTwo()
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
            $.ajax({
                url: '/properties/validate/address/',
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

    // Checks the uniqueness of the address, utilised when address' are typed in
    var address_line_1 = false
    var postcode = false
    $("#base-large-modal").on("change", "#id_address_line_1", function () {
        address_line_1 = true
        checkUniqueness()
    });
    $("#base-large-modal").on("change", "#id_postcode", function () {
        postcode = true
        checkUniqueness()
    });
    function checkUniqueness() {
        if (address_line_1 && postcode) {
            $.ajax({
                url: '/properties/validate/address/',
                data: {
                    'address_line_1': $("#id_address_line_1").val(),
                    'address_line_2': $("#id_address_line_2").val(),
                    'postcode': $("#id_postcode").val(),
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
        }
    }

    // Deals with the form submission for adding property & property process with AJAX
    // If success, calls the ajax for adding a valuation
    $("#base-large-modal").on("submit", ".js-add-property", function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#base-large-modal").modal("hide");
                    $('#modal-overlay').fadeToggle(100);
                    
                    $.ajax({
                        url: '/properties/add/valuation/' + data.propertyprocess_id + '/',
                        type: 'get',
                        dataType: 'json',
                        beforeSend: function () {
                            $("#base-modal").modal("show");
                        },
                        success: function (data) {
                            $("#base-modal .modal-dialog").html(data.html_modal);
                        }
                    });
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-large-modal .modal-dialog").html(data.html_modal);
                    $("#base-large-modal").find("#add-button").removeAttr("disabled");
                    initialSelectTwo()
                }
            }
        });
        return false;
    });

    // Deals with the form submission for adding property process when property in already in the system
    // If success, calls the ajax for adding a valuation
    $("#base-large-modal").on("submit", ".js-add-propertyprocess", function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        var button = $("#valuation-button")
        $.ajax({
            url: button.attr("data-url"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#base-large-modal").modal("hide");
                    $('#modal-overlay').fadeToggle(100);

                    $.ajax({
                        url: '/properties/add/valuation/' + data.propertyprocess_id + '/',
                        type: 'get',
                        dataType: 'json',
                        beforeSend: function () {
                            $("#base-modal").modal("show");
                        },
                        success: function (data) {
                            $("#base-modal .modal-dialog").html(data.html_modal);
                        }
                    });
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-large-modal .modal-dialog").html(data.html_modal);
                    $("#base-large-modal").find("#add-button").removeAttr("disabled");
                    initialSelectTwo()
                }
            }
        });
        return false;
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
                    $("#base-large-modal").modal("hide");
                    location.reload();
                    $('#modal-overlay').fadeToggle(100);
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-large-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    };

    // Deals with the form submission before loading success modal
    var submitLargeFormAndLoadSuccess = function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#base-large-modal").modal("hide");
                    $("#base-static-modal").modal("show");
                    $("#base-static-modal .modal-dialog").html(data.html_success);
                    $('#modal-overlay').fadeToggle(100);
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-large-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    };

    // Deals with the form submission before loading success modal
    var submitFormAndLoadSuccess = function () {
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
                    $("#base-static-modal").modal("show");
                    $("#base-static-modal .modal-dialog").html(data.html_success);
                    $('#modal-overlay').fadeToggle(100);
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    };

    // Deals with the form submission for adding history notes
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

    // Deals with the form submission for adding offerer
    $("#base-modal").on("submit", ".js-add-offerer-form", function () {
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
                    $.ajax({
                        url: data.url,
                        type: 'get',
                        dataType: 'json',
                        success: function (data) {
                            $("#base-static-modal").modal("show");
                            $('#modal-overlay').fadeToggle(100);
                            $("#base-static-modal .modal-dialog").html(data.html_modal);
                        }
                    });
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    });

    // Deals with the form submission for adding offerer mortgage
    $("#base-static-modal").on("submit", ".js-add-offerer-mortgage-form", function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $.ajax({
                        url: data.url,
                        type: 'get',
                        dataType: 'json',
                        success: function (data) {
                            $("#base-static-modal .modal-dialog").html(data.html_modal);
                            $('#modal-overlay').fadeToggle(100);
                        }
                    });
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-static-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    });

    // Deals with the form submission for adding offerer cash
    $("#base-static-modal").on("submit", ".js-add-offerer-cash-form", function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $.ajax({
                        url: data.url,
                        type: 'get',
                        dataType: 'json',
                        success: function (data) {
                            $("#base-static-modal .modal-dialog").html(data.html_modal);
                            $('#modal-overlay').fadeToggle(100);
                        }
                    });
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-static-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    });

    // Deals with the form submission for adding offerer for lettings
    $("#base-modal").on("submit", ".js-add-offerer-lettings-form", function () {
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
                    $.ajax({
                        url: data.url,
                        type: 'get',
                        dataType: 'json',
                        success: function (data) {
                            $("#base-static-modal").modal("show");
                            $("#base-static-modal .modal-dialog").html(data.html_modal);
                            $('#modal-overlay').fadeToggle(100);
                        }
                    });
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    });

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

    // Add scrollable to modal
    $(".js-large-scrollable-modal").on("click", function() {
        $("#base-large-modal .modal-dialog").addClass("modal-dialog-scrollable");
    });

    // Binding functions
    // Links
    $("#quick-actions").on("click", ".js-add-valuation", loadBaseModal);
    $("#quick-actions").on("click", ".js-add-instruction", loadBaseModal);
    $("#quick-actions").on("click", ".js-add-reduction", loadBaseModal);
    $("#quick-actions").on("click", ".js-add-offerer", loadBaseModal);

    $(".js-add-offerer").on("click", loadBaseModal);
    $("#base-modal").on("click", ".js-edit-offer-status", loadBaseModal);

    $("#base-modal").on("click", ".js-load-form", loadBaseModal);
    $(".js-load-form").on("click", loadBaseModal);
    $(".js-load-large-form").on("click", loadFormLargeModal);
    $("#base-static-modal").on("click", ".js-load-static-form", loadFormBaseStaticModal);

    $("#base-modal").on("submit", ".js-submit-form-success", submitFormAndLoadSuccess);
    $("#base-large-modal").on("submit", ".js-submit-form-success", submitLargeFormAndLoadSuccess);
    $("#base-static-modal").on("submit", ".js-submit-form-success", submitFormAndLoadSuccess);

    $("#base-modal").on("submit", ".js-submit-form", submitForm);
    $("#base-large-modal").on("submit", ".js-submit-form", submitLargeForm);
    $("#base-static-modal").on("submit", ".js-submit-form", submitStaticForm);
});