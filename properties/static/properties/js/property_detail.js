$(document).ready(function () {
    // Deals with the AJAX for adding a region. Loads the template
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
});