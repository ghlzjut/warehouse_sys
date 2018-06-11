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
            {field: 'CLOTH_PIECE_COUNT', title: '米数',edit:'true', align:'cneter'},
            {field: 'REMARKS', title: '备注', edit:'true',align:'cneter'},
            {title: '操作', width:170, templet:'#newsListBar',fixed:"right",align:"center"}
        ]]
    });

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


    //列表操作
    table.on('tool(newsList)', function(obj){
        var layEvent = obj.event,
            data = obj.data;
        if(layEvent === 'edit'){ //添加布匹数量
             $.get("/addPieceGoodsAction",{
                CLOTH_CODE : data.CLOTH_CODE,
                CLOTH_PIECE : data.CLOTH_PIECE,
                CLOTH_PIECE_COUNT : data.CLOTH_PIECE_COUNT,
                REMARKS : data.REMARKS
             },function(data){
                 if(data=='pieceFailed'){
                     layer.msg("请输入布匹数！")
                 }else if(data=='pieceCountFailed'){
                     layer.msg("请输入米数！")
                 }else if(data=='fail'){
                     layer.msg("未知错误！")
                 }else if (data=='success'){
                     layer.msg("添加成功！")
                 }
                tableIns.reload();
                layer.close(index);
             });
        }
    });

})