//jquery方式调用标签和方法
$(function() {

    //点击评论处的关闭按钮，隐藏评论区
    // $('.my-comment-close').click(function (event) {
    //     event.stopPropagation();
    //     $(this).parent('div').parent('div').css('display','none');
    // });
    //事件委托方式
    $(document).on('click','.my-comment-close',function(){
         event.stopPropagation();
         $(this).parent('div').parent('div').css('display','none');
     });


    //点击评论按钮，展开评论区
    // $('.span2').click(function () {
    //
    //     $(this).parent('p').parent('div').parent('a').siblings('.panel').css('display','block');
    // });
    //事件委托方式
     $(document).on('click','.span2',function(){
         $(this).parent('p').parent('div').parent('a').siblings('.panel').css('display','block');
     });
    //增加点赞数需求
    // $('.span1').click(function () {
    //     let span1_id = $(this).attr('id');
    //     let list_item = load_list_item();
    //     //默认评论数是0
    //     let recommend_count=Number($(this).children('span').text());
    //     if(list_item["recommend"]!=null){
    //         //评论数加1
    //         recommend_count +=1;
    //         list_item["recommend"][span1_id]=recommend_count;
    //     }else{
    //         recommend_count+=1;
    //         list_item={
    //             "recommend":{}
    //         };
    //         list_item["recommend"][span1_id]=recommend_count+1;
    //     }
    //     $(this).children('span').text(recommend_count);
    //     //把评论数保存起来，刷新页面或重新登陆时使用
    //     saveToLocalStorage(list_item);
    // });
    //事件委托方式
    $(document).on('click','.span1',function(){
         let span1_id = $(this).attr('id');
        let list_item = load_list_item();
        //默认评论数是0
        let recommend_count=Number($(this).children('span').text());
        if(list_item["recommend"]!=null){
            //评论数加1
            recommend_count +=1;
            list_item["recommend"][span1_id]=recommend_count;
        }else{
            recommend_count+=1;
            list_item={
                "recommend":{}
            };
            list_item["recommend"][span1_id]=recommend_count+1;
        }
        $(this).children('span').text(recommend_count);
        //把评论数保存起来，刷新页面或重新登陆时使用
        saveToLocalStorage(list_item);
     });
//提交评论需求
//     $('.commit-my-comment').click(function () {
//         //评论区域增加一条评论
//         let textarea_info = $(this).parent('.form-inline').find('textarea').val();
//         $(this).parent('.form-inline').find('textarea').val("");
//         $(this).parent('.form-inline').parent('.panel-body').find('ul').append(`<li class="list-group-item">${textarea_info}</li>`);
//         //最热评论数加1
//         let hot_comment = Number($(this).parent().parent().parent().find('.panel-heading').find('span:eq(0)').text());
//         hot_comment+=1;
//         $(this).parent('.form-inline').parent('.panel-body').parent('.panel').find('.panel-heading').find('span:eq(0)').text(hot_comment);
//         let comment_number = Number($(this).parent('.form-inline').parent('.panel-body').parent('.panel').parent('.list-group').find('.span2 span ').text());
//         comment_number+=1;
//         $(this).parent('.form-inline').parent('.panel-body').parent('.panel').parent('.list-group').find('.span2 span ').text(comment_number)
//
//     });
    //事件委托方式
    $(document).on('click','.commit-my-comment',function(){
         //评论区域增加一条评论
        let textarea_info = $(this).parent('.form-inline').find('textarea').val();
        $(this).parent('.form-inline').find('textarea').val("");
        $(this).parent('.form-inline').parent('.panel-body').find('ul').append(`<li class="list-group-item">${textarea_info}</li>`);
        //最热评论数加1
        let hot_comment = Number($(this).parent().parent().parent().find('.panel-heading').find('span:eq(0)').text());
        hot_comment+=1;
        $(this).parent('.form-inline').parent('.panel-body').parent('.panel').find('.panel-heading').find('span:eq(0)').text(hot_comment);
        let comment_number = Number($(this).parent('.form-inline').parent('.panel-body').parent('.panel').parent('.list-group').find('.span2 span ').text());
        comment_number+=1;
        $(this).parent('.form-inline').parent('.panel-body').parent('.panel').parent('.list-group').find('.span2 span ').text(comment_number)

     });
     //发布
//     $('button.my-publish').click(function () {
//         let publish_title = $(this).parent('.modal-footer').parent('.modal-content').find('#exampleInputEmail1').val();
//         let publish_info = $(this).parent('.modal-footer').parent('.modal-content').find('#exampleInputPassword1').val();
//         let recommend_id = guid();
//         let prepend_info=`
//         <div class="list-group">
//                 <a href="#" class="list-group-item my-comment-a">
//                     <div class="pull-left">
//                         <h5>
//                             ${publish_title} &nbsp;&nbsp
//                             <small>
//                                 -www.yystv,cn &nbsp;42区
//                             </small>
//                         </h5>
//                         <small>${publish_info}</small>
//                         <p class="my-comment-bottom-info">
//                             <span title="推荐" class="span1" id="recommend-${recommend_id}"><span>0</span></span>
//                             <span title="评论" class="span2"><span>0</span></span>
//                             <span title="加入私藏" class="span3"><span><small>私藏</small></span></span>
//                             <span class="span4"><img src="./images/small-img.jpg" alt=""></span>
//                             <span class="span5"><small>alice</small></span>
//                             <span class="span6"><small>8分钟前</small></span>
//                             <span class="span7"><small>发布</small></span>
//                         </p>
//                     </div>
//                     <div class="pull-right" >
//                         <img src="./images/1.jpg" alt="" class="my-comment-img">
//                     </div>
//                 </a>
// <!--                评论区，默认隐藏-->
//                 <div class="panel panel-default my-comment">
//                       <div class="panel-heading">
//                           最热评论 (<span>0</span>)
//                           <button type="button" class="close my-comment-close" aria-label="Close"><span aria-hidden="true">&times;</span></button>
//                       </div>
//                       <div class="panel-body">
//                           <ul class="list-group">
//                           </ul>
//                           <div class="form-inline">
//                               <label for="my-text-id"></label>
//                               <textarea name="" id="my-text-id" rows="2" cols="80" class="form-control"></textarea>
//                               <button type="button" class="btn btn-info commit-my-comment">评论</button>
//                           </div>
//
//                       </div>
//                 </div>
//             </div>
//         `;
//         //添加到分页前面
//         $('.my-pagination').prepend(prepend_info);
//
//     });
    $(document).on('click','button.my-publish',function(){
         let publish_title = $(this).parent('.modal-footer').parent('.modal-content').find('#exampleInputEmail1').val();
        let publish_info = $(this).parent('.modal-footer').parent('.modal-content').find('#exampleInputPassword1').val();
        let recommend_id = guid();
        let prepend_info=`
        <div class="list-group">
                <a href="#" class="list-group-item my-comment-a">
                    <div class="pull-left">
                        <h5>
                            ${publish_title} &nbsp;&nbsp
                            <small>
                                -www.yystv,cn &nbsp;42区
                            </small>
                        </h5>
                        <small>${publish_info}</small>
                        <p class="my-comment-bottom-info">
                            <span title="推荐" class="span1" id="recommend-${recommend_id}"><span>0</span></span>
                            <span title="评论" class="span2"><span>0</span></span>
                            <span title="加入私藏" class="span3"><span><small>私藏</small></span></span>
                            <span class="span4"><img src="./images/small-img.jpg" alt=""></span>
                            <span class="span5"><small>alice</small></span>
                            <span class="span6"><small>8分钟前</small></span>
                            <span class="span7"><small>发布</small></span>
                        </p>
                    </div>
                    <div class="pull-right" >
                        <img src="./images/1.jpg" alt="" class="my-comment-img">
                    </div>
                </a>
<!--                评论区，默认隐藏-->
                <div class="panel panel-default my-comment">
                      <div class="panel-heading">
                          最热评论 (<span>0</span>)
                          <button type="button" class="close my-comment-close" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                      </div>
                      <div class="panel-body">
                          <ul class="list-group">
                          </ul>
                          <div class="form-inline">
                              <label for="my-text-id"></label>
                              <textarea name="" id="my-text-id" rows="2" cols="80" class="form-control"></textarea>
                              <button type="button" class="btn btn-info commit-my-comment">评论</button>
                          </div>

                      </div>
                </div>
            </div>
        `;
        //添加到分页前面
        $('.my-pagination').prepend(prepend_info);
     });
     // //刷新页面调用的方法
     // $(window).ready(function () {
     //
     //    });
});

//保存数据到localStorage中，这些主要用于存储数据，
//保存到浏览器中，用于刷新浏览器或重新加载浏览器，展示数据使用
function saveToLocalStorage(data) {
    localStorage.setItem("list_item", JSON.stringify(data));
}
//加载localStorage中的数据
function load_list_item() {
    let list_item = localStorage.getItem('list_item');
    if(list_item != null){
        return JSON.parse(list_item);
    }else{
        return {};
    }
}
//生成uuid,用于设置新加的li的id,保证id的唯一
function guid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        let r = Math.random()*16|0, v = c === 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}