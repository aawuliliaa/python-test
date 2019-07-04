$(function () {
    let handlerPopup = function (captchaObj) {

        // 成功的回调
        captchaObj.onSuccess(function () {
            let validate = captchaObj.getValidate();
            $.ajax({
                url: "/pc-geetest/ajax_validate", // 进行二次验证
                type: "post",
                dataType: "json",
                data: {
                    username: $('#login_user_id').val(),
                    password: $('#login_pwd_id').val(),
                    csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                    geetest_challenge: validate.geetest_challenge,
                    geetest_validate: validate.geetest_validate,
                    geetest_seccode: validate.geetest_seccode
                },
                success: function (data) {
                    if (data && (data.status === "success")) {

                        // location.href="/index/"
                        if (data.user){
                            location.href="/index/"
                        }else{
                            $(".my_login_error").text("用户名或密码不存在").css("color","red")
                        }

                    } else {
                        $(document.body).html('<h1>登录失败</h1>');
                    }
                }
            });
        });
        $("#popup-submit").click(function () {

            captchaObj.show();

        });
        // 将验证码加到id为captcha的元素里
        captchaObj.appendTo("#popup-captcha");
        // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
    };

    // 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
    $.ajax({
        url: "/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
        type: "get",
        dataType: "json",
        success: function (data) {
            // 使用initGeetest接口
            // 参数1：配置参数
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
            }, handlerPopup);
        }
    });

     // 给每个input框绑定获取焦点之后清除之前错误提示的事件
    $("input.form-control").on("focus", function () {
        $(".my_login_error").text("");
    });
});
