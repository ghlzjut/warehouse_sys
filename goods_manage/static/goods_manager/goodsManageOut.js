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
            {field: 'CLOTH_CODE', title: '布样编码', align:'cneter' ,sort:'true'},
            {field: 'CLOTH_NAME', title: '布样名称', align:'cneter' ,sort:'true'},
            {field: 'CLOTH_FACTORY', title: '布样厂商', align:'cneter' ,sort:'true'},
            {field: 'CLOTH_REMAIN', title: '库存数量（米）', align:'cneter'},
            {field: 'CUSTOMER', title: '请输入客户名', edit:'true',align:'cneter'},
            {field: 'OUT_COUNT', title: '请输入出库数量（米）', edit:'true',align:'cneter'},
            {field: 'AMOUNT', title: '价格（元/米）', edit:'true',align:'cneter'},
            {field:'CREATE_DATE',title: '出库日期',align:'cneter',edit:'text'},
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
            if(layEvent === 'out'){ //出库
            layer.confirm('确定出库？',{icon:3, title:'提示信息'},function(index){
                 $.get("/outWareHouse",{
                     //传入出库数据
                    id : data.id ,
                    CLOTH_CODE:data.CLOTH_CODE,
                    CUSTOMER:data.CUSTOMER,
                    OUT_COUNT:data.OUT_COUNT,
                    AMOUNT:data.AMOUNT,
                    CREATE_DATE:data.CREATE_DATE
                 },function(data){
                     console.log(data)
                     if(data=='fail'){
                         layer.msg('库存数量不足，请补货入库！！！')
                     }
                     else if(data=='ValueError'){
                         layer.msg('请输入数字哦！')
                     }
                     else if(data=='notNull'){
                         layer.msg('出库数不能为空！')
                     }
                    tableIns.reload();
                    layer.close(index);
                 })
            });
        }
    });

})