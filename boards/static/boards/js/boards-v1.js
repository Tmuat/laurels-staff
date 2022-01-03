$(document).ready(function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    // Deals with the form submission before loading board modal
    var submitLargeFormAndLoadBoards = function () {
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
                    $("#base-static-modal .modal-dialog").html(data.html_board);
                    $("#modal-overlay").fadeToggle(100);
                } else {
                    $("#base-large-modal .modal-dialog").html(data.html_modal);
                    $("#modal-overlay").fadeToggle(100);
                }
            }
        });
        return false;
    };

    var hideBaseAndLoadLargeModal = function () {
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

    $("#base-large-modal").on("submit", ".js-submit-form-boards", submitLargeFormAndLoadBoards);
    $("#base-modal").on("click", ".js-hide-base-load-large-modal", hideBaseAndLoadLargeModal);

});