$(document).ready(function () {
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

    // Deals with hiding a modal
    var hideModal = function () {
        $("#base-modal").modal("hide");
    };

    $("#base-modal").on("click", ".js-hide-modal", hideModal);
    $("#base-modal").on("click", ".js-load-form", loadBaseModal);
    $(".js-load-form").on("click", loadBaseModal);
    $(".js-load-large-form").on("click", loadFormLargeModal);
    $("#base-modal").on("click", ".js-load-large-form", loadFormLargeModal);

    $("#base-modal").on("submit", ".js-submit-form", submitForm);
    $("#base-large-modal").on("submit", ".js-submit-form", submitLargeForm);
});