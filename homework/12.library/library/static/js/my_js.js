$(function () {
    $("#my_register_commit").click(
        $.ajax({
            url:"/register/",
            type:"post",
            data:{
                user:$("#register_user_id").val(),
                pwd:$("#register_pwd_id").val()
            },
            success:function (data) {
                
            }
        })
    )
});