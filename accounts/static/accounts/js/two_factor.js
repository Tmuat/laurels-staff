$(document).ready(function(){
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
        }
        else {
          $("#base-modal .modal-dialog").html(data.html_form);
        }
      }
    });
    return false;
  });

});