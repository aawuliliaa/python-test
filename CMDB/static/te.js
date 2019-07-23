$(document).ready(function () {
        // {#设置每页*条数据,在用户当前会话有效#}
        if($.cookie('env_data_nums_per_page')){
            data_nums_per_page = $.cookie('env_data_nums_per_page');
            $(`.data_nums_per_page_change option[value=${data_nums_per_page}]`).attr('selected',true)
        }
        if($.cookie('env_search')){
            role_search = $.cookie('env_search');
            // {#$("#search").val(decodeURIComponent(role_search));#}
            $("#search").val(role_search);
        }

        // {#这里是点击某行表格，展开下面的内容#}
        $('table.footable').footable({
		"paging": {
			"size": 20
		}
	    });
        // {#$('.footable2').footable();#}
    // FooTable.get("#fooltable_id")
    });
    $(function () {

        // {#每页数据量修改后，就刷新页面，并设置selected为#}
        $(".data_nums_per_page_change").change(function () {
             data_nums_per_page = $(".data_nums_per_page_change option:selected").val();
             FooTable.get('#footable_id').pageSize(data_nums_per_page);
             $.cookie('env_data_nums_per_page', data_nums_per_page, { path: '/' });
             location.href='/asset/env/';

        });
        $("#search_button").click(function () {
            // {#$.cookie('role_search', encodeURIComponent($("#search").val()), { path: '/' });#}
             $.cookie('env_search', $("#search").val(), { path: '/' });
            location.href='/asset/env/';
        })

    })
