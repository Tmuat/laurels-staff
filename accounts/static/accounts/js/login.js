$(document).ready(function () {
    $("#show-otp").click(function () {
        $("#show-otp").addClass("d-none")
        $("#otp-inputs").removeClass("d-none")
        $("#submit").removeClass("d-none")
        return false;
    });
});