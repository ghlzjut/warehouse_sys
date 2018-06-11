layui.use(['form','layer','layedit','laydate','upload'],function(){
    var form = layui.form
        layer = parent.layer === undefined ? layui.layer : top.layer,
        laypage = layui.laypage,
        upload = layui.upload,
        layedit = layui.layedit,
        laydate = layui.laydate,
        $ = layui.jquery;

    //用于同步编辑器内容到textarea
    layedit.sync(editIndex);


    //格式化时间
    function filterTime(val){
        if(val < 10){
            return "0" + val;
        }else{
            return val;
        }
    }


    // form.verify({
    //     newsName : function(val){
    //         if(val == ''){
    //             return "文章标题不能为空";
    //         }
    //     },
    //     content : function(val){
    //         if(val == ''){
    //             return "文章内容不能为空";
    //         }
    //     }
    // })
    form.on("submit(addNews)",function(data){
        //弹出loading
        $.post("/addOrderSuccess/",{
            ID: $(".ID").val(),  //码单号
            CUSTOMER : $(".CUSTOMER").val(),  //客户名
            CLOTH_PIECE : $(".CLOTH_PIECE").val(),  //布匹数
            CLOTH_COUNT : $(".CLOTH_COUNT").val(),  //总米数
            AMOUNT : $(".AMOUNT").val(),  //总金额
            ORDER_TIME : $(".ORDER_TIME").val(),//下单时间
        },function(res){
            // window.location.href="/addgoods/"
            if(res=='success'){
                top.layer.msg("码单添加成功！");
                layer.closeAll("iframe");
                //刷新父页面
                parent.location.reload();
            }
            else{
                layer.msg("请填写所有字段！")
            }
        })
        return false;
    })

    //预览
    form.on("submit(look)",function(){
        layer.alert("功能暂未开发，尽请期待！");
        return false;
    })

    //创建一个编辑器
    var editIndex = layedit.build('news_content',{
        height : 535,
        uploadImage : {
            url : "../../json/newsImg.json"
        }
    });

})