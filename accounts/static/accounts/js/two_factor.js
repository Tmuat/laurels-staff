$(document).ready(function () {
  // Deals with the AJAX for removing a OTP. Loads the template
  $(".js-remove-otp").click(function () {
    $.ajax({
      url: '/account/two-factor/remove/',
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

  // Deals with OTP form submission for AJAX. Calls the setup URL on success
  $("#base-modal").on("submit", ".js-remove-otp-form", function () {
    $('#modal-overlay').fadeToggle(100);
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $('#modal-overlay').fadeToggle(100);
          $.ajax({
            url: '/account/two-factor/setup/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
              $("#base-modal .modal-dialog").html(data.html_modal);
            }
          });
        } else {
          $("#base-modal .modal-dialog").html(data.html_form);
        }
      }
    });
    return false;
  });

  // Deals with the form submission for adding OTP with AJAX
  $("#base-modal").on("submit", ".js-add-otp-form", function () {
    $('#modal-overlay').fadeToggle(100);
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
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

  // Deals with the loading of the backup tokens form with AJAX
  $(".js-backup-otp").click(function () {
    $.ajax({
      url: '/account/two-factor/backup/tokens/',
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

  // Deals with the loading of backup tokens with AJAX
  $("#base-modal").on("submit", ".js-generate-backup-otp", function () {
    $('#modal-overlay').fadeToggle(100);
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $('#modal-overlay').fadeToggle(100);
          $.ajax({
            url: '/account/two-factor/backup/tokens/',
            type: 'get',
            dataType: 'json',
            success: function (data) {
              $("#base-modal .modal-dialog").html(data.html_modal);
            }
          });
        } else {
          $('#modal-overlay').fadeToggle(100);
          $("#base-modal .modal-dialog").html(data.html_form);
        }
      }
    });
    return false;
  });

});