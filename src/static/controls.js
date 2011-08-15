$(document).ready(function () {
    $("#popup").one("click", function () {
        $("#hegemony").toggleClass("display");
        $("#popup").click(function () {
            // XXX
            $("#popup").parent("form").attr("action", "/hegemony");
        });
        return false;
    });
});
