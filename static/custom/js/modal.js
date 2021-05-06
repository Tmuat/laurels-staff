$(document).ready(function(){
  $(".js-logout").click(function () {
    $.ajax({
      url: '/account/logout-modal/',
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