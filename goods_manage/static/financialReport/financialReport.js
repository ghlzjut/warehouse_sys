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

    //时间框
    laydate.render({
       elem:'#beginDate',
       type:"datetime"
    });
      laydate.render({
       elem:'#endDate',
       type:"datetime"
    });
    //新闻列表
    var tableIns = table.render({
        elem: '#Report',
        url : '/financialReport',
        cellMinWidth : 95,
        page : true,
        height : "full-125",
        limit : 15,
        limits : [10,15,20,25],
        id : "newsListTable",
        cols : [[
            {field: 'CUSTOMER', title: '客户名', align:'cneter', fixed:"left"},
            {field: 'CLOTH_CODE', title: '布样编码', align:'cneter'},
            {field: 'COUNT', title: '购买数量（米）', align:'cneter'},
            {field: 'AMOUNT', title: '购买金额(元)', align:'cneter', fixed:"right"},
        ]]
    });

    //搜索【此功能需要后台配合，所以暂时没有动态效果演示】
    $(".search_btn").on("click",function(){
        if($(".customerVal").val() != ''){
            table.reload("newsListTable",{
                url : '/financialReport',
                page: {
                    curr: 1 //重新从第 1 页开始
                },
                where: {
                    CUSTOMER: $(".customerVal").val(),  //搜索的关键字
                    BEGINDATE: $(".beginDateVal").val(),  //搜索的关键字
                    ENDDATE: $(".endDateVal").val(),  //搜索的关键字
                }
            })
        }else{
            layer.msg("请选择客户姓名");
        }
    });
    $(document).ready(function(){
       $.ajax({
            async:false,
            url:'/getCustomer',
            type:"GET",
            dataType:"json",
            success:function(data){
                if(data!=null)
                {
                    var customer=$('#customer');
                    var data=eval(data);
                    var html="";
                    // layer.msg('初始化客户姓名成功',{icon:1});
                    for(var i in data)
                    {
                        html += "<option value="+data[i].CUSTOMER+">"+data[i].CUSTOMER+"</option>";
                    }
                        customer.append(html);
                     form.render('select');
                }else
                {
                    layer.msg("初始化客户姓名失败",{icon:2});
                }
            }
        })
    })
})
