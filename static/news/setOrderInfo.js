/**
 * Created by GHL on 2018/5/22.
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
        url : '/showPieceGoods',
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
            {field: 'CLOTH_PIECE_COUNT', title: '米数', align:'cneter'},
            {field: 'REMARKS', title: '备注', align:'cneter'},
            {field: 'CLOTH_PIECE', title: '相同规格布匹数',align:'cneter'},
            {title: '操作', width:170, templet:'#newsListBar',fixed:"right",align:"center"}
        ]]
    });

    //搜索【此功能需要后台配合，所以暂时没有动态效果演示】
    $(".search_btn").on("click",function(){
        if($(".searchVal").val() != ''){
            table.reload("newsListTable",{
                url : '/showPieceGoods',
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
        var p_value=$(".orderNo").html();
        console.log(p_value);
       if(layEvent === 'add'){ //删除
            layer.confirm('确定添加至码单？',{icon:3, title:'提示信息'},function(index){
                 $.get("/addToOrder",{
                    id : p_value ,//将需要删除的newsId作为参数传入
                    PieceId:data.id
                 },function(data){
                    tableIns.reload();
                    layer.close(index);
                 })
            });
        }
    });

});