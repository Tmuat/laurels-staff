$(document).ready(function () {

    // Deals with the form submission only
    var submitGetForm = function () {
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

    // Deals with filtering
    var submitFilterGetForm = function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        var selectedOption = form.find(':selected').val()
        $.ajax({
            url: form.attr("action"),
            data: {
                filter: selectedOption 
                },
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                // location.reload();
                $('#modal-overlay').fadeToggle(100);
                console.log(data.start_date)
                console.log(data.end_date)
            }
        });
        return false;
    };

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

    // Binding functions
    // Links

    $(".js-load-form").on("click", loadBaseModal);
    $(".js-filter-get-form").on("submit", submitFilterGetForm);
    $("#base-modal").on("submit", ".js-submit-get-form", submitGetForm);
});