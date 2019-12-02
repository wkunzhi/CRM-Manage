(function (jq) {
    jq('.multi-menu .title').click(function () {
        // 对自己进行收缩
        $(this).next().toggleClass('hide');
    });
})(jQuery);