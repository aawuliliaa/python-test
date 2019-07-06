$(function () {
    //添加文章，提交文章到数据库中
    $(".add_article_commit").click(function () {
        let article_title = $("#add_article_title").val();
        let article_desc = $("#add_article_desc").val();
        //获取编辑器中的内容
        let article_content = $(document.getElementsByTagName("iframe")[0].contentWindow.document.body).html();
        let article_category = $(".my_article_classes option:selected").val();
        //由于后端插入数据的时候使用的是列表的形式，所以我们直接在这里把数据放到列表中
        let tag_id_list = [];
        $('.my_article_tag option:selected').each(function () {
            tag_id_list.push($(this).val());
        });
        $.ajax({
            url:"/add_article/",
            type:"post",
            //传递列表到后端时，需要设置该项，否则无法通过key获取值，因为会自动在key后面添加[]
            traditional:true,
            data:{
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
                article_title:article_title,
                article_category:article_category,
                article_content:article_content,
                tag_id_list:tag_id_list
            },
            success:function (data) {
                if (data.success){
                    alert("文章添加成功");
                    location.href="/back_manage/"
                }else{
                    $(".add_article_error_info").text(data.info).css("color","red");
                    setTimeout(function () {
                         $(".add_article_error_info").text("")
                    },500)
                }
            }
        })
    });

    $(".box_show").click(function () {
        //点击左侧的内容，nav_tabs中响应的标签添加active
        if($(this).hasClass("pa")){
            let pa_val = $(this).attr("value");
            $(`li.na[value=${pa_val}]`).addClass("active").siblings("li").removeClass("active");
            $(`.${pa_val}`).removeClass("hidden").siblings("div").addClass("hidden")
        }
        if($(this).hasClass("na")){
            let na_val = $(this).attr("value");
            $(this).addClass("active").siblings("li").removeClass("active");
            $(`.${na_val}`).removeClass("hidden").siblings("div").addClass("hidden")
        }
    });
    //需要进行事件委托，只有该方式，新加的元素才能事件才能操作
    $(".list-group").on('click','.del_classes',function(){
       let classes = "";
        if($(this).hasClass("category")){
            classes="category"
        }else if($(this).hasClass("tag")){
            classes="tag"
        }
        let classes_id = $(this).attr("value");
        let del_button_obj = $(this);
        $.ajax({
            url:"/del_classes/",
            type: "post",
            data:{
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
                classes:classes,
                classes_id:classes_id
            },
            success:function (data) {
                if(data.success){
                    del_button_obj.parent("li").remove()
                }

            }
        });
    });

    //删除分类和标签
    // $(".del_classes").click(function () {
    //     let classes = "";
    //     if($(this).hasClass("category")){
    //         classes="category"
    //     }else if($(this).hasClass("tag")){
    //         classes="tag"
    //     }
    //     let classes_id = $(this).attr("value");
    //     let del_button_obj = $(this);
    //     $.ajax({
    //         url:"/del_classes/",
    //         type: "post",
    //         data:{
    //             csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
    //             classes:classes,
    //             classes_id:classes_id
    //         },
    //         success:function (data) {
    //             if(data.success){
    //                 del_button_obj.parent("li").remove()
    //             }
    //
    //         }
    //     });
    // });


    //添加文章分类或标签
         $(".add_classes_btn").click(function () {

            let classes = "";
            let classes_obj="";
            let box_class="";
            if($(this).hasClass("category")){
                classes="category";
            }else if($(this).hasClass("tag")){
                classes="tag";
            }
            let add_button_obj = $(this);
            $.ajax({
                url:"/add_classes/",
                type:"post",
                data:{
                    csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
                    classes:classes,
                    classes_title:add_button_obj.siblings("input").val()
                },
                success:function (data) {
                    //添加新加的元素，立即展示在页面中
                    if(data.success){
                        let new_item = `<li class="list-group-item">
                            ${data.title}
                        <button type="button" class="btn btn-warning del_classes category" value="${data.id}">删除</button>
                        </li>`;
                        $(new_item).insertBefore(add_button_obj.parent("li"))
                         }
                    else{
                        //展示错误信息
                        add_button_obj.siblings("span").text(data.info).css("color","red");
                        setTimeout(function () {
                            add_button_obj.siblings("span").text("")
                        },500)
                    }
                    //输入框置空
                    add_button_obj.siblings("input").val("");

                }
            })
        });


});
 //kindeditor内容，放在上面不行，只能放在外面
 KindEditor.ready(function(K) {
                    window.editor = K.create('#add_article_content',{

                        resizeType:0,
                        uploadJson:"/upload/",
                        extraFileUploadParams:{
                            csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
                        },
                        filePostName:"upload_img"
                    });
            });
