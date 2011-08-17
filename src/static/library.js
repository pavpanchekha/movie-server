function swipeLeft() {
    if ($("section:visible").prev("section").length) {
        $("section:visible").hide().prev("section").show(); 
    }
}

function swipeRight() {
    if ($("section:visible").next("section").length) {
        $("section:visible").hide().next("section").show(); 
    }
}

$(function () {
    $("section").hide().last().show();
    
    $(document).swipe({
        swipeLeft:  swipeLeft,
        swipeRight: swipeRight,
        threshold: 200,
        allowPageScroll: "vertical",
    });
});
