$(document).ready(function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
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

    // Deals with hiding the base modal
    var hideBaseModal = function () {
        $("#base-modal").modal("hide");
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
    // Deals with rendering a form with AJAX to the large modal thats scrollable
    var loadFormLargeScrollableModal = function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#base-large-modal").modal("show");
                $("#base-large-modal .modal-dialog").addClass("modal-dialog-scrollable");
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

    $('#query-search').on("click", function() {
        var currentUrl = new URL(window.location);

        var selectedVal = $("#managed-query").val();

        currentUrl.searchParams.delete("page");
        currentUrl.searchParams.set("query", selectedVal);

        window.location.replace(currentUrl);
    })

    // Binding functions
    // Links

    $(".js-load-form").on("click", loadBaseModal);
    $(".js-load-large-form").on("click", loadFormLargeModal);
    $(".js-load-large-scrollable-form").on("click", loadFormLargeScrollableModal);

    $("#base-modal").on("click", ".js-load-large-form", loadFormLargeModal);
    $("#base-modal").on("click", ".js-load-large-scrollable-form", loadFormLargeScrollableModal);
    $("#base-modal").on("click", ".js-hide-form", hideBaseModal);
    $("#base-modal").on("submit", ".js-submit-form", submitForm);
    $("#base-large-modal").on("submit", ".js-submit-form", submitLargeForm);
    $("#base-static-modal").on("submit", ".js-submit-form", submitStaticForm);
});