
$(document).ready(function () {
    // {#alert(location.pathname) /asset/env/#}
        // {#设置每页*条数据,在用户当前会话有效#}
// {#    吧"/asset/env/变为 assetenv,因为/放到cookie中就乱码了，到后端无法根据key来获取值"#}
        let location_pathname = location.pathname.split("/").join("");

        // {#        隐藏footable默认生成的分页#}
        $(".pagination ul").css("display","none");
        if($.cookie(`${location_pathname}data_nums_per_page`)){

            data_nums_per_page = $.cookie(`${location_pathname}data_nums_per_page`);
            // {#alert(data_nums_per_page)#}
            $(`.data_nums_per_page_change option[value=${data_nums_per_page}]`).attr('selected',true);
            $("#footable_id").attr("data-page-size",data_nums_per_page)
        }
        let search_content = $("#search");
        if($.cookie(`${location_pathname}search`)){
            search_content_val = $.cookie(`${location_pathname}search`);

            // {#search_content.val(decodeURIComponent(search_content));#}
            search_content.val(search_content_val);
        }
        // {#渲染成footable#}
        $('.footable').footable();

    });
$(function () {

    let location_pathname = location.pathname.split("/").join("");
    // {#alert(location_pathname)#}
    // {#console.log("/asset/".replace("/",""))#}
    $(".pagination ul").css("display","none");
    // {#每页数据量修改后，就刷新页面，并设置selected为#}
    $(".data_nums_per_page_change").change(function () {
         data_nums_per_page = $(".data_nums_per_page_change option:selected").val();
         $.cookie(`${location_pathname}data_nums_per_page`, data_nums_per_page, { path: '/' });
         location.href=location.pathname;

         // {#$("#footable_id").attr("data-page-size",data_nums_per_page)#}

    });
    let search_content = $("#search");
    search_content.keyup(function(){

        if(event.keyCode == 13){
        //这里写你要执行的事件;
        //     {#$.cookie(`${location_pathname}search`, encodeURIComponent(search_content.val()), { path: '/' });#}
             $.cookie(`${location_pathname}search`, search_content.val(), { path: '/' });
            location.href=location.pathname;
        }
    });
});