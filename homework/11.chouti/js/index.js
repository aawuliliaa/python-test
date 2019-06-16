
$(function() {
    //点击评论处的关闭按钮，隐藏评论区
    $('.my-comment-close').click(function (event) {
        event.stopPropagation();
        $(this).parent('div').parent('div').css('display','none');
    });
    //点击评论按钮，展开评论区
    $('.span2').click(function () {

        $(this).parent('p').parent('div').parent('a').siblings('.panel').css('display','block');
    })
});