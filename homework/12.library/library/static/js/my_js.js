$(function () {
    //提交注册的用户信息
    $("#my_register_commit").click(
        function () {
            $.ajax({
            url:"/register/",
            type:"post",

            data:{
                user:$("#register_user_id").val(),
                pwd:$("#register_pwd_id").val(),
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success:function (data) {
                let result = JSON.parse(data);
                if (result.user){
                    //用户创建成功，result.user=="用户名"
                    alert(result.user+" create success!");
                    //创建成功，跳转到login页面
                    location.href="/login/"
                }else{
                    let error_info = result.info;
                    $("#my_register_error").text(error_info).css({"color":"red"})
                }


            }
        })
        }
    );

    $("#my_login_commit").click(function () {
        $.ajax({
            url:"/login/",
            type:"post",
            data:{
                user:$("#login_user_id").val(),
                pwd:$("#login_pwd_id").val(),
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success:function (data) {
                console.log(data);
                if(data.user){
                    if(data.info){
                    //    用户存在，错误信息也存在，就是密码不正确
                        $(".my_login_pwd_error").text(data.info).css({"color":"red"})
                    }else{
                    //    用户名和密码正确
                        location.href = "/index/"
                    }
                }else{
                //    用户不存在
                    $(".my_login_user_error").text(data.info).css({"color":"red"})
                }

            }
        })
    })
});