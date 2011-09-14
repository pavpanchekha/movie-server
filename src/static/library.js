function swipeLeft() {
    $("#all").animate({left: "-100%"}, "fast");
}

function swipeRight() {
    $("#all").animate({left: "0"}, "fast");
}

$(function () {
    //$("section").hide().last().show();
    
    $(document).swipe({
        swipeLeft:  swipeLeft,
        swipeRight: swipeRight,
        threshold: 200,
        allowPageScroll: "vertical",
    });
});
