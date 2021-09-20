$(document).ready(function () {
    // Deals with the AJAX for loading invite user form.
    $(".js-add-invitation").click(function () {
        $.ajax({
            url: '/users/invitations/invite-user/',
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#base-modal").modal("show");
                $("#base-modal .modal-dialog").addClass("modal-dialog-scrollable");
            },
            success: function (data) {
                $("#base-modal .modal-dialog").html(data.html_modal);
            }
        });
    });

    // Checks the uniqueness of the invitee
    $("#base-modal").on("change", "#id_email", function () {
        var email = $(this).val();
        $.ajax({
            url: '/users/invitations/check-user/',
            data: {
                'email': email
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
    $("#base-modal").on("submit", ".js-invite-user-form", function () {
        $('#modal-overlay').fadeToggle(100);
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    if (data.targets) {
                        $.ajax({
                            url: "/users/invitations/user-targets/" + data.invitation_key + "/",
                            type: 'get',
                            dataType: 'json',
                            beforeSend: function () {
                                $('#modal-overlay').fadeToggle(100);
                                $("#base-modal").modal("hide");
                                $("#base-large-modal").modal("show");
                                $("#base-large-modal .modal-dialog").addClass("modal-dialog-scrollable");
                            },
                            success: function (data) {
                                $("#base-large-modal .modal-dialog").html(data.html_large_modal);
                            }
                        });
                    } else {
                        $('#modal-overlay').fadeToggle(100);
                        $("#base-modal").modal("hide");
                        location.reload();
                    }
                } else {
                    $('#modal-overlay').fadeToggle(100);
                    $("#base-modal .modal-dialog").html(data.html_modal);
                }
            }
        });
        return false;
    });
    
    // Deals with the form submission for adding user targets to invitations with AJAX
    $("#base-large-modal").on("submit", ".js-add-user-targets-form", function (e) {
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
});