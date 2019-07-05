$(function () {
    //提交评论处使用
    let pid = "";
    let reply_user = "";
   // 获取评论树
   $.ajax({
    url:"/get_comment_tree/",
    type:"get",
    data:{
        article_id:$("#article_id").text()
    },
    success:function (data) {
        $.each(data,function (index,comment_obj) {
            let comment_obj_pk = comment_obj.pk;
            let comment_obj_content = comment_obj.content;
            let comment_obj_parent_comment_id = comment_obj.parent_comment_id;
            let comment_obj_user__username = comment_obj.user__username;
            let s = `<div class="comment_item list-group-item" id=${comment_obj_pk}><a class="user_name">@${comment_obj_user__username}<span>&nbsp;&nbsp;</span></a><span>${comment_obj_content}</span><a class="pull-right reply_btn" id="">回复</a></div>`;
            if(!comment_obj_parent_comment_id){
                $("#comment_tree").append(s)
            }else{
                $("[id=" + comment_obj_parent_comment_id + "]").append(s);
            }

        })
    }
});
    //点击回复按钮，聚焦到回复评论的内容框
    //事件委托，新加的元素为其添加事件是不成功的，需要使用事件委托的方式
    $("#comment_tree").on('click','.reply_btn',function(){
       pid = $(this).parent("div").attr("id");
       reply_user = $(this).parent("div").children(".user_name").text();
       let my_comment_content = reply_user+"\n";
       $("#my_comment_content").focus().val(my_comment_content);
     });
   // $(".reply_btn").click(function () {
   //     console.log("2222222222");
   //     pid = $(this).parent("div").attr("id");
   //     let my_comment_content =$(this).parent("div").find(".user_name").text()+"\n";
   //     $("#my_comment_content").focus().val(my_comment_content);
   //
   // })
   // 提交评论内容
    $("#my_comment_commit").click(function () {
        let article_id = $("#article_id").text();
        let comment_content = $("#my_comment_content").val();

        $.ajax({
            url:"/commit_comment/",
            type: "post",
            data: {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                article_id:article_id,
                comment_content:comment_content,
                parent_comment_id:pid,
                reply_user:reply_user
            },
            success:function (data) {
                let comment_obj_pk = data.pk;
                let comment_obj_content = data.content;
                let comment_obj_parent_comment_id = data.parent_comment_id;
                let comment_obj_user__username = data.user__username;
                let s = `<div class="comment_item list-group-item" id=${comment_obj_pk}><a class="user_name">@${comment_obj_user__username}<span>&nbsp;&nbsp;</span></a><span>${comment_obj_content}</span><a class="pull-right reply_btn" id="">回复</a></div>`;

                if(data.success){
                    if(pid){
                        $("[id=" + comment_obj_parent_comment_id + "]").append(s);
                    }else{
                        $("#comment_tree").append(s)
                    }
                    //成功之后的清理工作，是不影响后面的操作
                    pid="";
                    reply_user="";
                    $("#my_comment_content").val("")
                }
            }
        })
    });
    $(".my_article_up_down").click(function () {
        let article_id = $("#article_id").text();
        let this_obj = $(this);
        let up_down = $(this).hasClass("my_article_down")?"down":"up";
        $.ajax({
            url:"/up_down/",
            type:"post",
            data:{
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                article_id:article_id,
                up_down:up_down
            },
            success:function (data) {
                let up_down_info = "";
                if(data.success){
                    up_down_info = this_obj.hasClass("my_article_up")?"点赞成功！":"反对成功！";
                    this_obj.text(parseInt(this_obj.text())+1);
                }else{
                    up_down_info = "已经点评过了！"
                }

                $(".up_down_info").text(up_down_info).css("color","red");
                setTimeout(function () {
                    $(".up_down_info").text("")
                },500)
            }
        });

    });
});