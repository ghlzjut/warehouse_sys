/**
 * Created by GHL on 2018/6/8.
 */
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
        url : '/showGoodsOut',
        cellMinWidth : 95,
        page : true,
        height : "full-125",
        limit : 15,
        limits : [10,15,20,25],
        id : "newsListTable",
        cols : [[
            {type: "checkbox", fixed:"left", width:50},
            {field: 'id', title: 'ID', width:60, align:"center"},
            {field: 'CLOTH_CODE', title: '布样编码', align:'cneter' ,sort:'true'},
            {field: 'CUSTOMER', title: '客户名', edit:'true',align:'cneter'},
            {field: 'CLOTH_COUNT', title: '出库数量（米）', edit:'true',align:'cneter'},
            {field: 'AMOUNT', title: '出库价格（元/米）', edit:'true',align:'cneter'},
            {field:'CREATE_TIME',title: '出库日期',align:'cneter',edit:'text'},
            // {field: 'newsLook', title: '浏览权限', align:'center'},
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
    table.on('tool(GoodsList)', function(obj){
        var layEvent = obj.event,
            data = obj.data;
            if(layEvent === 'edit'){ //修改
            layer.confirm('确定修改？',{icon:3, title:'提示信息'},function(index){
                 $.get("/editGoodsOut",{
                     //传入出库数据
                    id : data.id ,
                    CLOTH_CODE:data.CLOTH_CODE,
                    CUSTOMER:data.CUSTOMER,
                    CLOTH_COUNT:data.CLOTH_COUNT,
                    AMOUNT:data.AMOUNT,
                    CREATE_TIME:data.CREATE_TIME
                 },function(data){
                    console.log(data);
                    tableIns.reload();
                    layer.close(index);
                 })
            });
        }
    });

})