$(document).ready(function () {

    // Deals with filtering
    var submitFilterGetForm = function () {
        $('#modal-overlay').fadeToggle(100);
        var currentUrl = new URL(window.location);
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
                currentUrl.searchParams.set("start-date", data.start_date);
                currentUrl.searchParams.set("end-date", data.end_date);
                currentUrl.searchParams.set("filter", data.filter);
                window.location.replace(currentUrl);
            }
        });
        return false;
    };

    // Deals with sorting
    var setSort = function () {
        $('#modal-overlay').fadeToggle(100);
        var currentUrl = new URL(window.location);
        var element = $(this);
        currentUrl.searchParams.set("sort", element.attr("data-sort"));
        currentUrl.searchParams.set("direction", element.attr("data-direction"));
        window.location.replace(currentUrl);
    };

    // Deals with removing sorting
    var removeSort = function () {
        var currentUrl = new URL(window.location);
        var element = $(this);
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");
        window.location.replace(currentUrl);
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

    $(".js-sort").on("click", setSort);
    $(".js-remove-sort").on("click", removeSort);
});