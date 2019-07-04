$(function () {
    //头像预览功能
    $("#avatar").change(function () {
        let file_obj = $(this)[0].files[0];
        let reader = new FileReader();
        reader.readAsDataURL(file_obj);
        reader.onload = function () {
            $("#my_avatar_img").attr("src",reader.result)
        }
    });
    $(".my_reg_commit").click(function () {
        let formData = new FormData();
        //存放数据方式一：
        // formData.append("csrfmiddlewaretoken", $("[name='csrfmiddlewaretoken']").val());
        // formData.append("username", $("#id_username").val());
        // formData.append("password", $("#id_password").val());
        // formData.append("re_password", $("#id_re_password").val());
        // formData.append("phone", $("#id_phone").val());
        // formData.append("avatar", $("#avatar")[0].files[0]);
        
        // 存放数据方式二
        let request_data = $("#form").serializeArray();
        // console.log(request_data)，下面是request_data的内容
        //[{…}, {…}, {…}, {…}, {…}]
        // 0: {name: "csrfmiddlewaretoken", value: "Q6cM6rw8847S5taZaulrJChCvezVM0WvOJ1kraj3YY2EO8TpzSzgKHELlLk0hMtM"}
        // 1: {name: "username", value: "vita"}
        // 2: {name: "password", value: "123"}
        // 3: {name: "re_password", value: "123"}
        // 4: {name: "telephone", value: "1212112121"}
        // length: 5
        // __proto__: Array(0)
        //列表循环
        $.each(request_data,function (index,data) {
            formData.append(data.name,data.value)
        });
        //文件对象$("#avatar")[0].files[0]
        formData.append("avatar",$("#avatar")[0].files[0]);
        $.ajax({
            url:"/register/",
            type:"post",
            contentType:false,//上传文件，需要设置这两个false
            processData: false,
            data:formData,
            success:function (data) {
                if (data.user){
                    location.href="/login/"
                }else{
                    //清除报错添加的样式，否则下次报信错，原来的错误样式还在
                    $("span.error").html("");
                    $(".form-group").removeClass("has-error");

                    //data.msg是一个字典，每个key对应的是列表
                    $.each(data.msg,function (key,val_error_list) {
                        if(key==="__all__"){
                            //错误信息框中添加报错信息，并给该框添加has-error类
                            //这里是确认密码处添加报错信息
                            $("#id_re_password").next().html(val_error_list[0]).parent().addClass("has-error")
                        }
                        $("#id_"+key).next().html(val_error_list[0]).parent().addClass("has-error")

                })
                }

            }
        })
    })
});