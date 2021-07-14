$(document).ready(function () {
    $('#hub-select').change(function() {
        var selector = $(this);
        var currentUrl = new URL(window.location);

        var selectedVal = selector.val();

        if(selectedVal == "reset"){
            currentUrl.searchParams.delete("hub");
        } else {
            currentUrl.searchParams.set("hub", selectedVal);
        }

        window.location.replace(currentUrl);
    })

    $('#employee-select').change(function() {
        var selector = $(this);
        var currentUrl = new URL(window.location);

        var selectedVal = selector.val();

        if(selectedVal == "reset"){
            currentUrl.searchParams.delete("user");
        } else {
            currentUrl.searchParams.set("user", selectedVal);
        }

        window.location.replace(currentUrl);
    })

    // Deals with rendering a form with AJAX to the base modal
    var loadFormBaseModal = function () {
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

    // Deals with the form submission for static modal
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

    // Reload the current page
    $("#base-static-modal").on("click", ".js-reload", function () {
        $('#modal-overlay').fadeToggle(100);
        location.reload();
    });

    // Binding functions
    // Links

    $(".js-load-form").on("click", loadFormBaseModal);

    $("#base-static-modal").on("click", ".js-load-static-form", loadFormBaseStaticModal);

    $("#base-modal").on("submit", ".js-submit-form-success", submitFormAndLoadSuccess);
    $("#base-static-modal").on("submit", ".js-submit-form", submitStaticForm);
});