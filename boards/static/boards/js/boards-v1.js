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
                    $("#base-modal").modal("show");
                    $("#base-modal .modal-dialog").html(data.html_board);
                    $("#modal-overlay").fadeToggle(100);
                } else {
                    $("#base-large-modal .modal-dialog").html(data.html_modal);
                    $("#modal-overlay").fadeToggle(100);
                }
            }
        });
        return false;
    };

    $("#base-large-modal").on("submit", ".js-submit-form-boards", submitLargeFormAndLoadBoards);

});