$(function () {
    $("#select_system").change(function(){
        //选择系统框变化了，环境框的内容是该系统下的所有环境
        let system_selected_id = $("#select_system option:selected").val();
        $.ajax({
            url:"/task_manage/get_env_by_system_id/",
            type:"get",
            data:{"system_id":system_selected_id},
            success:function (result) {
                console.log(result)
                $("#select_environment option").remove();
                // $("#select_environment").remove(old_child);
                //不加value=""，通过val()获取option的值是text()中的值
                $("#select_environment").append(`<option value="">---------------</option>`);
                $("#select_host option").remove();
                // $("#select_environment").remove(old_child);
                $("#select_host").append(`<option value="">---------------</option>`);
                if(result.env_list.length > 0) {
                     $.each(result.env_list,function(index,value){

                         $("#select_environment").append(`<option value="${value.id}">${value.name}----${value.abs_name}</option>`);
                     })
                }
                if(result.host_list.length > 0) {
                     $.each(result.host_list,function(index,value){

                         $("#select_host").append(`<option value="${value.id}">${value.ip}</option>`);
                     })
                }
            }
        });
    });



    $("#select_environment").change(function(){
        //选择系统框变化了，环境框的内容是该系统下的所有环境
        let system_selected_id = $("#select_system option:selected").val();
        let environment_selected_id = $("#select_environment option:selected").val();
        $.ajax({
            url:"/task_manage/get_host_by_sys_or_env_id/",
            type:"get",
            data:{"system_id":system_selected_id,
                  "environment_id": environment_selected_id},
            success:function (result) {
                $("#select_host option").remove();
                // $("#select_environment").remove(old_child);
                $("#select_host").append(`<option value="">---------------</option>`);
                if(result.length > 0) {
                     $.each(result,function(index,value){

                         $("#select_host").append(`<option value="${value.id}">${value.ip}</option>`);
                     })
                }
            }
        });
    })



});