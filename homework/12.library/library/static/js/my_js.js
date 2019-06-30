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
    //登录
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
    });
    //添加作者
    $("#add_author_commit").click(function () {
        $.ajax({
            url:"/add_author/",
            type:"post",
            data:{
                author_name:$("#add_author_id").val(),
                author_age:$("#add_age_id").val(),
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success:function (data) {
                if(data.success){
                    location.href = "/index/";
                    alert(data.info)
                }else{
                    $(".add_author_error").text(data.info).css({"color":"red"})
                }
            }
        })
    });
//提交作者编辑信息
$("#author_edit_commit").click(
    function () {
        let user_id = $("#edit_user_ID").text();
        $.ajax({
            url:"/edit_author/"+user_id+"/",
            type:"post",
            data:{
                author_name:$("#edit_author_id").val(),
                author_age:$("#edit_age_id").val(),
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success:function (data) {
                if(data.success){
                    alert(data.info);
                    location.href = "/index/"
                }else{
                    $(".edit_author_error").text(data.info).css({"color":"red"})
                }
            }
        })
    }
);

    
    //添加作者
    $("#add_publish_commit").click(function () {
        $.ajax({
            url:"/add_publish/",
            type:"post",
            data:{
                publish_name:$("#add_publish_name_id").val(),
                publish_city:$("#add_publish_city_id").val(),
                publish_email:$("#add_publish_email_id").val(),
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success:function (data) {
                if(data.success){
                    location.href = "/index/";
                    alert(data.info)
                }else{
                    $(".add_publish_error").text(data.info).css({"color":"red"})
                }
            }
        })
    });
    
    
    //提交出版社编辑信息
$("#publish_edit_commit").click(
    function () {
        let publish_id = $("#edit_publish_ID").text();
        $.ajax({
            url:"/edit_publish/"+publish_id+"/",
            type:"post",
            data:{
                publish_name:$("#edit_publish_name_id").val(),
                publish_city:$("#edit_publish_city_id").val(),
                publish_email:$("#edit_publish_email_id").val(),
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success:function (data) {
                if(data.success){
                    alert(data.info);
                    location.href = "/index/"
                }else{
                    $(".edit_publish_error").text(data.info).css({"color":"red"})
                }
            }
        })
    }
);

});
