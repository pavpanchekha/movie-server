function fix_widths() {
    var width = $("body").width();
    var N = Math.floor(width / 240);
    var itemwidth = Math.floor(width / N) - 4; // 2 -> padding

    var lasth1 = 0;
    $("div.item, h1").each(function (idx) {
        if (this.tagName == "H1" || this.tagName == "h1") {
            lasth1 = idx + 1;
            return;
        }

        if ((idx - lasth1) % N == 0) {
            $(this).css("clear", "left");
        } else {
            $(this).css("clear", "none");
        }
        $(this).width(itemwidth);
    });
}


$(window).load(fix_widths);
$(window).resize(fix_widths);
