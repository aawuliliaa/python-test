$(function () {
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
    })
});
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
