$(document).ready(function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      });

    // Deals with rendering a scrollable model with AJAX
    var loadLargeScrollableBaseModal = function () {
        var instance = $(this);
        $.ajax({
            url: instance.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#base-large-modal .modal-dialog").addClass("modal-dialog-scrollable");
                $("#base-large-modal").modal("show");
                $("#base-large-modal .modal-dialog").html(data.html_modal);
            }
        });
        return false;
    };

    // Binding functions
    // Links

    $(".js-scrollable-modal").on("click", loadLargeScrollableBaseModal);
});