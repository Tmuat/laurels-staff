$(document).ready(function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

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
                $("#base-large-modal").modal("show");
                $("#base-large-modal .modal-dialog").html(data.html_modal);
                $('#modal-overlay').fadeToggle(100);
            }
        });
        return false;
    };

    // Add scrollable to modal
    $(".js-large-scrollable-modal").on("click", function() {
        $("#base-large-modal .modal-dialog").addClass("modal-dialog-scrollable");
    });

    // Binding functions
    // Links
    $("#base-modal").on("click", ".js-edit-offer-status", loadBaseModal);

    $("#base-modal").on("click", ".js-load-form", loadBaseModal);
    $("#base-modal").on("click", ".js-hide-base-load-large", hideBaseModalAndLoadLargeModal);
    $(".js-load-form").on("click", loadBaseModal);
    $(".js-load-large-form").on("click", loadFormLargeModal);
    $("#base-static-modal").on("click", ".js-load-static-form", loadFormBaseStaticModal);

    $("#base-modal").on("submit", ".js-submit-form", submitForm);
    $("#base-large-modal").on("submit", ".js-submit-form", submitLargeForm);
    $("#base-static-modal").on("submit", ".js-submit-form", submitStaticForm);
});