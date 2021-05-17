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
                    $("#page-title").html(data.html_region_page_title);
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

    // Deals with the AJAX for editing a region.
    $(".js-edit-region").click(function () {
        var button = $(this);
        $.ajax({
            url: button.attr("data-url"),
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

    // Checks the uniqueness of the region name whilst editing
    $("#base-modal").on("change", "#id_region_name", function () {
        var regionName = $(this).val();
        var currentRegionName = $('#region_slug').text().slice(1, -1);
        $.ajax({
            url: '/region-hub/check/region/' + currentRegionName + '/',
            data: {
                'region_name': regionName
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    $("#base-modal").find("#mdi-icon").removeClass("mdi-check-circle-outline").addClass("mdi-close-circle-outline");
                    $("#base-modal").find("#unique_check").addClass("text-danger border-danger");
                    $("#base-modal").find("#add-button").attr("disabled", true);
                } else {
                    $("#base-modal").find("#mdi-icon").removeClass("mdi-close-circle-outline").addClass("mdi-check-circle-outline");
                    $("#base-modal").find("#unique_check").removeClass("text-danger border-danger").addClass("border-success text-success");
                    $("#base-modal").find("#add-button").removeAttr("disabled");
                };
            }
        });
    });

    // Checks if the region has hubs still associated with it
    $("#base-modal").on("change", "#id_is_active", function () {
        var currentRegionName = $('#region_slug').text().slice(1, -1);
        if($("#id_is_active").prop('checked') != true){
            $.ajax({
                url: '/region-hub/check/region/hubs/' + currentRegionName + '/',
                dataType: 'json',
                success: function (data) {
                    if (data.associated_hubs) {
                        $("#base-modal").find("#second-mdi-icon").removeClass("mdi-help-circle").addClass("mdi-close-circle-outline");
                        $("#base-modal").find("#hub_check").addClass("text-danger border-danger");
                        $("#base-modal").find("#add-button").attr("disabled", true);
                    } else {
                        $("#base-modal").find("#second-mdi-icon").removeClass("mdi-help-circle").addClass("mdi-check-circle-outline");
                        $("#base-modal").find("#hub_check").removeClass("text-danger border-danger").addClass("border-success text-success");
                        $("#base-modal").find("#add-button").removeAttr("disabled");
                    };
                }
            });
        };
    });

    // Deals with the form submission for editing region with AJAX
    $("#base-modal").on("submit", ".js-edit-region-form", function () {
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
    });

    // Deals with the AJAX for adding a hub. Loads the template.
    $(".js-add-hub").click(function () {
        $.ajax({
            url: '/region-hub/add/hub/',
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

    // Checks the uniqueness of the hub name
    $("#base-modal").on("change", "#id_hub_name", function () {
        var hubName = $(this).val();
        $.ajax({
            url: '/region-hub/check/hub/',
            data: {
                'hub_name': hubName
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

    // Deals with the form submission for adding hub with AJAX
    $("#base-modal").on("submit", ".js-add-hub-form", function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    var hub = data.hub_slug
                    $("#panel-div").html(data.html_region_panels);
                    $("#page-title").html(data.html_region_page_title);
                    $("#base-modal").modal("hide");
                    $.ajax({
                        url: '/region-hub/add/' + hub + '/hub-targets/',
                        type: 'get',
                        dataType: 'json',
                        beforeSend: function () {
                            $("#base-large-modal .modal-dialog").addClass("modal-dialog-scrollable");
                            $("#base-large-modal").modal("show");
                        },
                        success: function (data) {
                            $("#base-large-modal .modal-dialog").html(data.html_large_modal);
                        }
                    });
                    $('#modal-overlay').fadeToggle(100);
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    });

    // Deals with the form submission for adding hub targets with AJAX
    $("#base-large-modal").on("submit", ".js-add-hub-targets-form", function (e) {
        e.preventDefault();

        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: "json",
            success: function (data) {
                if (data.form_is_valid) {
                    $("#modal-overlay").fadeToggle(100);
                    $("#base-large-modal").modal("hide");
                    location.reload();
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-large-modal .modal-dialog").html(data.html_large_modal);
                }
            }
        });
    });

    $(".js-add-specific-hub-targets").click(function () {
        var button = $(this);
        $.ajax({
            url: button.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#base-large-modal .modal-dialog").addClass("modal-dialog-scrollable");
                $("#base-large-modal").modal("show");
            },
            success: function (data) {
                $("#base-large-modal .modal-dialog").html(data.html_large_modal);
            }
        });
    });

    // Deals with the AJAX for editing a hub.
    $(".js-edit-hub").click(function () {
        var button = $(this);
        $.ajax({
            url: button.attr("data-url"),
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

    // Checks the uniqueness of the hub name
    $("#base-modal").on("change", "#id_change_hub_name", function () {
        var hubName = $(this).val();
        var currentHubName = $('#hub_slug').text().slice(1, -1);
        $.ajax({
            url: '/region-hub/check/hub/' + currentHubName + '/',
            data: {
                'hub_name': hubName
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    $("#base-modal").find("#mdi-icon").removeClass("mdi-check-circle-outline").addClass("mdi-close-circle-outline");
                    $("#base-modal").find("#unique_check").addClass("text-danger border-danger");
                    $("#base-modal").find("#add-button").attr("disabled", true);
                } else {
                    $("#base-modal").find("#mdi-icon").removeClass("mdi-close-circle-outline").addClass("mdi-check-circle-outline");
                    $("#base-modal").find("#unique_check").removeClass("text-danger border-danger").addClass("border-success text-success");
                    $("#base-modal").find("#add-button").removeAttr("disabled");
                };
            }
        });
    });

    // Deals with the form submission for editing hub with AJAX
    $("#base-modal").on("submit", ".js-edit-hub-form", function () {
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
    });

    // Deals with the AJAX for editing hub targets.
    $(".js-edit-hub-targets").click(function () {
        var button = $(this);
        $.ajax({
            url: button.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#base-large-modal").modal("show");
            },
            success: function (data) {
                $("#base-large-modal .modal-dialog").html(data.html_large_modal);
            }
        });
    });

});