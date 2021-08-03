$(document).ready(function(){
  $(".js-logout").click(function () {
    $.ajax({
      url: '/account/logout-modal/',
      type: 'get',
      dataType: 'json',
      success: function (data) {
        $("#base-modal").modal("show");
        $("#base-modal .modal-dialog").html(data.html_modal);
      }
    });
  });
});