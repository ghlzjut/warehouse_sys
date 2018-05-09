/**
 * Created by GHL on 2018/5/4.
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
        elem: '#GoodsList',
        url : '/showGoodsList',
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
            {field: 'CLOTH_FACTORY', title: '布样厂商', align:'cneter'},
            {field: 'CLOTH_REMAIN', title: '库存数量（米）', align:'cneter'},
            {field: 'OUT_COUNT', title: '请输入出库数量（米）', edit:'true',align:'cneter',value:0},
            {field: 'IN_COUNT', title: '请输入入库数量（米）', edit:'true',align:'cneter'},
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
                url : '/showGoodsList',
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

    //添加文章
    // function addNews(edit){
    //     var index = layui.layer.open({
    //         title : "添加文章",
    //         type : 2,
    //         content : "/addcloth",
    //         success : function(layero, index){
    //             var body = layui.layer.getChildFrame('body', index);
    //             if(edit){
    //                 body.find(".ID").val(edit.id);
    //                 body.find(".newsCode").val(edit.CLOTH_CODE);
    //                 body.find(".newsName").val(edit.CLOTH_NAME);
    //                 body.find(".newsFactory").val(edit.CLOTH_FACTORY);
    //                 body.find(".thumbImg").attr("src",edit.newsImg);
    //                 body.find("#news_content").val(edit.CONTENT);
    //                 body.find(".CLOTH_STATUS select").val(edit.CLOTH_STATUS);
    //                 body.find(".openness input[name='openness'][title='"+edit.newsLook+"']").prop("checked","checked");
    //                 body.find(".newsTop input[name='newsTop']").prop("checked",edit.newsTop);
    //                 form.render();
    //             }
    //             setTimeout(function(){
    //                 layui.layer.tips('点击此处返回文章列表', '.layui-layer-setwin .layui-layer-close', {
    //                     tips: 3
    //                 });
    //             },500)
    //         }
    //     })
    //     layui.layer.full(index);
    //     //改变窗口大小时，重置弹窗的宽高，防止超出可视区域（如F12调出debug的操作）
    //     $(window).on("resize",function(){
    //         layui.layer.full(index);
    //     })
    // }
    // $(".addNews_btn").click(function(){
    //     addNews();
    // })
    //
    // //批量删除
    // $(".delAll_btn").click(function(){
    //     var checkStatus = table.checkStatus('newsListTable'),
    //         data = checkStatus.data,
    //         newsId = [];
    //     if(data.length > 0) {
    //         for (var i in data) {
    //             newsId.push(data[i].id);
    //         }
    //         console.log(newsId)
    //         layer.confirm('确定删除选中的文章？', {icon: 3, title: '提示信息'}, function (index) {
    //              $.get("/delCloth",{
    //                  id : newsId  //将需要删除的newsId作为参数传入
    //              },function(data){
    //             tableIns.reload();
    //             layer.close(index);
    //              })
    //         })
    //     }else{
    //         layer.msg("请选择需要删除的文章");
    //     }
    // })

    //列表操作
    table.on('tool(GoodsList)', function(obj){
        var layEvent = obj.event,
            data = obj.data;

        if(layEvent === 'in'){ //入库
             layer.confirm('确定入库？',{icon:3, title:'提示信息'},function(index){
                 $.get("/inWareHouse",{
                     //传入出库数据
                    id : data.id ,
                    CLOTH_CODE:data.CLOTH_CODE,
                    IN_COUNT:data.IN_COUNT
                 },function(data){
                      if(data=='ValueError'){
                         layer.msg('请输入数字哦！')
                     }
                    tableIns.reload();
                    layer.close(index);
                 })
            });
        } else if(layEvent === 'out'){ //出库
            layer.confirm('确定出库？',{icon:3, title:'提示信息'},function(index){
                 $.get("/outWareHouse",{
                     //传入出库数据
                    id : data.id ,
                    CLOTH_CODE:data.CLOTH_CODE,
                    OUT_COUNT:data.OUT_COUNT
                 },function(data){
                     if(data=='fail'){
                         layer.msg('库存数量不足，请补货入库！！！')
                     }
                     else if(data='ValueError'){
                         layer.msg('请输入数字哦！')
                     }
                    tableIns.reload();
                    layer.close(index);
                 })
            });
        }
    });

})