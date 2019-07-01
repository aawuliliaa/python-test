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

                console.log("========");
                console.log(data);
                if (data.user){
                    //用户创建成功，result.user=="用户名"
                    alert(data.user+" create success!");
                    //创建成功，跳转到login页面
                    location.href="/login/"
                }else{
                    let error_info = data.info;
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

                    //    用户名和密码正确
                    location.href = "/index/"

                }else{
                //    用户不存在
                    $(".my_login_error").text(data.info).css({"color":"red"})
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
    //编辑作者时，展示默认信息
    $(".my_author_edit_show_button").click(function () {
        let author_id = $(this).val();
        let author_age = $(this).parent("td").parent("tr").children(".author_age").text();
        let author_name = $(this).parent("td").parent("tr").find(".author_name").text();
        $("#edit_user_ID").text(author_id);
        $("#edit_author_id").val(author_name);
        $("#edit_age_id").val(author_age)
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
//编辑出版社时，展示默认信息
    $(".my_publish_edit_show_button").click(function () {
        let publish_id = $(this).val();
        let publish_email = $(this).parent("td").parent("tr").children(".publish_email").text();
        let publish_city = $(this).parent("td").parent("tr").children(".publish_city").text();
        let publish_name = $(this).parent("td").parent("tr").find(".publish_name").text();
        $("#edit_publish_ID").text(publish_id);
        $("#edit_publish_name_id").val(publish_name);
        $("#edit_publish_city_id").val(publish_city);
        $("#edit_publish_email_id").val(publish_email);
    });
    $("#book_add_commit").click(function () {
        //由于后端插入数据的时候使用的是列表的形式，所以我们直接在这里把数据放到列表中
        let book_author_id_list = [];
        $('#add_book_authors_id option:selected').each(function () {
            book_author_id_list.push($(this).val());
            //book_author_id_list+=","
        });
        let book_publish_id = $("#add_book_publish_id option:selected").val();
        let book_title = $("#add_book_title_id").val();
        let book_publishDate = $("#add_book_publishDate_id").val();
        let book_price = $("#add_book_price_id").val();
        $.ajax({
            url:"/add_book/",
            type:"post",
            //如果不做traditional:true的设置，参数传递中是会自动把key变为了book_authors_id_list[]，服务端是无法通过book_authors_id_list获取参数的
            traditional:true,
            data:{
                book_authors_id_list:book_author_id_list,
                book_publish_id:book_publish_id,
                book_title:book_title,
                book_publishDate:book_publishDate,
                book_price:book_price,
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success:function (data) {
                    if(data.success){
                        alert(data.info);
                        location.href = "/index/"
                    }else{
                        $(".add_book_error").text(data.info).css({"color":"red"})
                    }
                }
        })
    });

        //提交书籍编辑信息
    $("#book_edit_commit").click(
        function () {
                //由于后端插入数据的时候使用的是列表的形式，所以我们直接在这里把数据放到列表中
            let book_id = $("#edit_book_ID").text();
            let book_author_id_list = [];
            $('#edit_book_authors_id option:selected').each(function () {
                book_author_id_list.push($(this).val());
                //book_author_id_list+=","
            });
            let book_publish_id = $("#edit_book_publish_id option:selected").val();
            let book_title = $("#edit_book_title_id").val();
            let book_publishDate = $("#edit_book_publishDate_id").val();
            let book_price = $("#edit_book_price_id").val();
            $.ajax({
                url:"/edit_book/"+book_id+"/",
                type:"post",
                //如果不做traditional:true的设置，参数传递中是会自动把key变为了book_authors_id_list[]，服务端是无法通过book_authors_id_list获取参数的
                traditional:true,
                data:{
                    book_authors_id_list:book_author_id_list,
                    book_publish_id:book_publish_id,
                    book_title:book_title,
                    book_publishDate:book_publishDate,
                    book_price:book_price,
                    csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                },
                success:function (data) {
                        if(data.success){
                            alert(data.info);
                            location.href = "/index/"
                        }else{
                            $(".edit_book_error").text(data.info).css({"color":"red"})
                        }
                    }
            })
        }
    );
    //编辑书籍，弹出模态框
    $('.my_book_edit_show_button').click(function () {
        let book_id = $(this).val();
        $.ajax({
            url:"/edit_book/"+book_id+"/",
            type:"get",
            success:function (data) {
                // console.log(data.json_books_obj);[{"model": "app.author", "pk": 1, "fields": {"name": "\u5f20\u4e09\u65b0", "age": 12}}]
                //设置模态框中的值

                let publish_list = JSON.parse(data.json_publish_list);
                let author_list = JSON.parse(data.json_author_list);
                let book_obj = data.json_book_obj;

                let publish_str = "";
                let author_str = "";
                for(let publish_item in publish_list){
                    //这块研究了好一会，这个publish_item只是列表的索引
                    // console.log(publish_list[publish_obj].fields.name)
                    if (publish_list.hasOwnProperty(publish_item)){
                        let publish_name = publish_list[publish_item].fields.name;
                        let publish_id = publish_list[publish_item].pk;
                        if(publish_id === book_obj.publish_id){
                            publish_str+=`<option value="${publish_id}" selected>${publish_name}</option>`
                        }else{
                            publish_str+=`<option value="${publish_id}">${publish_name}</option>`
                        }
                    }
                }
                for(let author_item in author_list){
                    //这块研究了好一会，这个publish_item只是列表的索引
                    // console.log(publish_list[publish_obj].fields.name)
                    if (author_list.hasOwnProperty(author_item)){
                        let author_name = author_list[author_item].fields.name;
                        let author_id = author_list[author_item].pk;
                        //如果该书的作者有当前循环的作者id，就设置为selected
                        if (book_obj.author_id_list.indexOf(author_id)!==-1){
                            author_str+=`<option value="${author_id}" selected>${author_name}</option>`
                        }else{
                            author_str+=`<option value="${author_id}">${author_name}</option>`
                        }


                    }
                }
                //设置模态框中的数据
                $("#edit_book_ID").html(book_obj.book_id);
                $("#edit_book_title_id").val(book_obj.book_title);
                $("#edit_book_price_id").val(book_obj.book_price);
                $("#edit_book_publishDate_id").val(book_obj.book_publishDate);
                $("#edit_book_publish_id").html(publish_str);
                $("#edit_book_authors_id").html(author_str);

            }
        })
    });
//添加书籍模态框弹出时，设置出版社和作者
    $("#my_book_add_button").click(function () {
        $.ajax({
            url:"/add_book/",
            type:"get",
            success:function (data) {
                 // console.log(data.json_books_obj);[{"model": "app.author", "pk": 1, "fields": {"name": "\u5f20\u4e09\u65b0", "age": 12}}]
                let publish_list = JSON.parse(data.json_publish_list);
                let author_list = JSON.parse(data.json_author_list);
                let publish_str = "";
                let author_str = "";
                for(let publish_item in publish_list){
                    //这块研究了好一会，这个publish_item只是列表的索引,0,1,2,3
                    // console.log(publish_list[publish_obj].fields.name)
                    if (publish_list.hasOwnProperty(publish_item)){
                        let publish_name = publish_list[publish_item].fields.name;
                        let publish_id = publish_list[publish_item].pk;
                        
                        if(publish_item === 0){
                            publish_str+=`<option value="${publish_id}" selected>${publish_name}</option>`
                        }else{
                            publish_str+=`<option value="${publish_id}">${publish_name}</option>`
                        }
                    }
                }
                for(let author_item in author_list){
                    //这块研究了好一会，这个publish_item只是列表的索引
                    // console.log(publish_list[publish_obj].fields.name)
                    if (author_list.hasOwnProperty(author_item)){
                        let author_name = author_list[author_item].fields.name;
                        let author_id = author_list[author_item].pk;
                        author_str+=`<option value="${author_id}">${author_name}</option>`
                    }
                }
                $("#add_book_publish_id").html(publish_str);
                $("#add_book_authors_id").html(author_str);
            }
        })
    })
});
