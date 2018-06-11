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
        url : '/showOrderList',
        cellMinWidth : 95,
        page : true,
        height : "full-125",
        limit : 15,
        limits : [10,15,20,25],
        id : "newsListTable",
        cols : [[
            {type: "checkbox", fixed:"left", width:50},
            {field: 'id', title: '码单号', width:90, align:"center"},
            {field: 'CUSTOMER', title: '客户名称', align:'cneter'},
            {field: 'CLOTH_PIECE', title: '布匹数', align:'cneter'},
            {field: 'CLOTH_COUNT', title: '布匹总米数', align:'cneter'},
            {field: 'AMOUNT', title: '订单金额',  align:'center'},
            // {field: 'newsLook', title: '浏览权限', align:'center'},
            {field: 'ORDER_TIME', title: '下单时间', align:'center', minWidth:110},
            {title: '操作', width:170, templet:'#newsListBar',fixed:"right",align:"center"}
        ]]
    });


    //搜索【此功能需要后台配合，所以暂时没有动态效果演示】
    $(".search_btn").on("click",function(){
        if($(".searchVal").val() != ''){
            table.reload("newsListTable",{
                url : '/showOrderList',
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
            title : "添加码单",
            type : 2,
            content : "/addOrder",
            success : function(layero, index){
                var body = layui.layer.getChildFrame('body', index);
                if(edit){
                    body.find(".ID").val(edit.id);
                    body.find(".CUSTOMER").val(edit.CUSTOMER);
                    body.find(".CLOTH_PIECE").val(edit.CLOTH_PIECE);
                    body.find(".CLOTH_COUNT").val(edit.CLOTH_COUNT);
                    body.find(".AMOUNT").val(edit.AMOUNT);
                    body.find(".ORDER_TIME").val(edit.ORDER_TIME);
                    form.render();
                }
                setTimeout(function(){
                    layui.layer.tips('点击此处返回码单列表', '.layui-layer-setwin .layui-layer-close', {
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

    //码单下单
    function setOrder(edit){
        var index = layui.layer.open({
            title : "码单信息",
            type : 2,
            content : "/setOrderInfo",
            success : function(layero, index){
                var body = layui.layer.getChildFrame('body', index);
                if(edit){
                    body.find(".orderNo").append(edit.id)
                    form.render();
                }
                setTimeout(function(){
                    layui.layer.tips('点击此处返回码单列表', '.layui-layer-setwin .layui-layer-close', {
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
            layer.confirm('确定删除选中的码单？', {icon: 3, title: '提示信息'}, function (index) {
                 $.get("/delOrder",{
                     id : newsId  //将需要删除的newsId作为参数传入
                 },function(data){
                tableIns.reload();
                layer.close(index);
                 })
            })
        }else{
            layer.msg("请选择需要删除的码单");
        }
    })

    //列表操作
    table.on('tool(newsList)', function(obj){
        var layEvent = obj.event,
            data = obj.data;
        if(layEvent === 'edit'){ //编辑
            addNews(data);
        } else if(layEvent === 'del'){ //删除
            layer.confirm('确定删除此文章？',{icon:3, title:'提示信息'},function(index){
                 $.get("/delOrder",{
                    id : data.id  //将需要删除的newsId作为参数传入
                 },function(data){
                    tableIns.reload();
                    layer.close(index);
                 })
            });
        } else if(layEvent === 'add'){ //下单
            setOrder(data);
        }
    });

})