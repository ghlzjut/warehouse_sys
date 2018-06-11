/**
 * Created by GHL on 2018/5/22.
 */
/**
 * Created by GHL on 2018/4/17.
 */
//获取url中的参数
function GetRequest() {
   var url = location.search; //获取url中"?"符后的字串
   var theRequest = new Object();
   if (url.indexOf("?") != -1) {
      var str = url.substr(1);
      strs = str.split("&");
      for(var i = 0; i < strs.length; i ++) {
         theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
      }
   }
   return theRequest;
}

var Request = new Object();
Request = GetRequest();
var orderNo
orderNo=Request['orderNo']

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
        url : '/showOrderDetail',
        where:{orderNo:orderNo},
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
            {field: 'CLOTH_PIECE_COUNT', title: '原米数', align:'cneter'},
            {field: 'EDIT_CLOTH_COUNT', title: '更改米数',edit:'true', align:'cneter'},
            {field: 'AMOUNT', title: '每米单价（元/米）', edit:'true', align:'cneter'},
            {field: 'REMARKS', title: '备注', edit:'true', align:'cneter'},
            {title: '操作', width:170, templet:'#newsListBar',fixed:"right",align:"center"}
        ]]
    });

    $(".orderNo").html(orderNo)

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

    //确认订单
    $(".setOrder_btn").click(function(){
            layer.confirm('核对码单后，确认下单？', {icon: 3, title: '提示信息'}, function (index) {
                 $.get("/placeOrder",{
                     id : orderNo  //将码单号传入
                 },function(data){
                    if(data==='success'){
                        top.layer.msg("下单成功！");
                        layer.closeAll("iframe");
                        //刷新父页面
                        parent.location.reload();
                    }
                 })
            })
    });

    //列表操作
    table.on('tool(newsList)', function(obj){
        var layEvent = obj.event,
            data = obj.data;
       if(layEvent === 'del'){ //删除
            layer.confirm('确定将布匹移出码单？',{icon:3, title:'提示信息'},function(index){
                 $.get("/removePiece",{
                    id : data.id  //将需要删除的newsId作为参数传入
                 },function(data){
                    tableIns.reload();
                    layer.close(index);
                 })
            });
        }else if(layEvent==='edit') {//修改
           layer.confirm('确认修改？', {icon: 3, title: '提示信息'}, function (index) {
               $.get("/editOrderPiece", {
                   id: data.id,  //将需要修改的newsId作为参数传入
                   EDIT_CLOTH_COUNT:data.EDIT_CLOTH_COUNT,
                   REMARKS : data.REMARKS,
                   AMOUNT : data.AMOUNT
               }, function (data) {
                   tableIns.reload();
                   layer.close(index);
               })
           });
       }
    });

})