/**
 * Created by GHL on 2018/5/24.
 */
/**
 * Created by GHL on 2018/4/17.
 */
layui.use(['form','layer','laydate','table','laytpl'],function(){
    var form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery,
        laydate = layui.laydate,
        laytpl = layui.laytpl,
        table = layui.table;

    //新闻列表
    var tableIns = table.render({
        elem: '#newsList',
        url : '/showWhiteCloth',
        cellMinWidth : 95,
        page : true,
        height : "full-125",
        limit : 15,
        limits : [10,15,20,25],
        id : "newsListTable",
        cols : [[
            {type: "checkbox", fixed:"left", width:50},
            {field: 'id', title: 'ID', width:60, align:"center"},
            {field: 'CLOTH_CODE', title: '布样编码', align:'cneter'},
            {field: 'CLOTH_NAME', title: '布样名称', align:'cneter'},
            {field: 'CLOTH_REMAIN', title: '库存', align:'cneter'},
            {field: 'CLOTH_DEAL_REMAIN', title: '出场加工数', align:'cneter'},
            // {field: 'newsLook', title: '浏览权限', align:'center'},
            {title: '操作', width:170, templet:'#newsListBar',fixed:"right",align:"center"}
        ]]
    });

    //是否置顶
    form.on('switch(newsTop)', function(data){
        var index = layer.msg('修改中，请稍候',{icon: 16,time:false,shade:0.8});
        setTimeout(function(){
            layer.close(index);
            if(data.elem.checked){
                layer.msg("置顶成功！");
            }else{
                layer.msg("取消置顶成功！");
            }
        },500);
    })

    //搜索【此功能需要后台配合，所以暂时没有动态效果演示】
    $(".search_btn").on("click",function(){
        if($(".searchVal").val() != ''){
            table.reload("newsListTable",{
                url : '/showWhiteCloth',
                page: {
                    curr: 1 //重新从第 1 页开始
                },
                where: {
                    key: $(".searchVal").val()  //搜索的关键字
                }
            })
        }else{
            layer.msg("请输入搜索的内容");
        }
    });

    //添加布样
    function addNews(edit){
        var index = layui.layer.open({
            title : "添加布样",
            type : 2,
            content : "/addWhiteCloth",
            success : function(layero, index){
                var body = layui.layer.getChildFrame('body', index);
                if(edit){
                    body.find(".ID").val(edit.id);
                    body.find(".newsCode").val(edit.CLOTH_CODE);
                    body.find(".newsName").val(edit.CLOTH_NAME);
                    body.find(".CLOTH_REMAIN").val(edit.CLOTH_REMAIN);
                    body.find(".CLOTH_DEAL_REMAIN").val(edit.CLOTH_DEAL_REMAIN);
                    form.render();
                }
                setTimeout(function(){
                    layui.layer.tips('点击此处返回布样管理', '.layui-layer-setwin .layui-layer-close', {
                        tips: 3
                    });
                },500)
            }
        })
        layui.layer.full(index);
        //改变窗口大小时，重置弹窗的宽高，防止超出可视区域（如F12调出debug的操作）
        $(window).on("resize",function(){
            layui.layer.full(index);
        })
    }
    $(".addNews_btn").click(function(){
        addNews();
    })

    //批量删除
    $(".delAll_btn").click(function(){
        var checkStatus = table.checkStatus('newsListTable'),
            data = checkStatus.data,
            newsId = [];
        if(data.length > 0) {
            for (var i in data) {
                newsId.push(data[i].id);
            }
            console.log(newsId)
            layer.confirm('确定删除选中的布样？', {icon: 3, title: '提示信息'}, function (index) {
                 $.get("/delWhiteCloth",{
                     id : newsId  //将需要删除的newsId作为参数传入
                 },function(data){
                tableIns.reload();
                layer.close(index);
                 })
            })
        }else{
            layer.msg("请选择需要删除的布样");
        }
    })

    //列表操作
    table.on('tool(newsList)', function(obj){
        var layEvent = obj.event,
            data = obj.data;

        if(layEvent === 'edit'){ //编辑
            addNews(data);
        } else if(layEvent === 'del'){ //删除
            layer.confirm('确定删除此布样？',{icon:3, title:'提示信息'},function(index){
                 $.get("/delWhiteCloth",{
                    id : data.id  //将需要删除的newsId作为参数传入
                 },function(data){
                    tableIns.reload();
                    layer.close(index);
                 })
            });
        } else if(layEvent === 'look'){ //预览
            layer.alert("此功能暂未开放")
        }
    });

})