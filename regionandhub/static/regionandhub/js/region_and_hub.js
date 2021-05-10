$(document).ready(function () {
    // Deals with the AJAX for adding a region. Loads the template
    $(".js-add-region").click(function () {
        $.ajax({
            url: '/region-hub/add/region/',
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

    // Checks the uniqueness of the region name
    $("#base-modal").on("change", "#id_name", function () {
        var regionName = $(this).val();
        $.ajax({
            url: '/region-hub/check/region/',
            data: {
                'region_name': regionName
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

    // Deals with the form submission for adding region with AJAX
    $("#base-modal").on("submit", ".js-add-region-form", function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#panel-div").html(data.html_region_panels);
                    console.log("Should have changed");
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-modal").modal("hide");
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    });

});