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

    //上传缩略图
    upload.render({
        elem: '.thumbBox',
        url: '../../json/userface.json',
        method : "get",  //此处是为了演示之用，实际使用中请将此删除，默认用post方式提交
        done: function(res, index, upload){
            var num = parseInt(4*Math.random());  //生成0-4的随机数，随机显示一个头像信息
            $('.thumbImg').attr('src',res.data[num].src);
            $('.thumbBox').css("background","#fff");
        }
    });

    //格式化时间
    function filterTime(val){
        if(val < 10){
            return "0" + val;
        }else{
            return val;
        }
    }
    //定时发布
    var time = new Date();
    var submitTime = time.getFullYear()+'-'+filterTime(time.getMonth()+1)+'-'+filterTime(time.getDate())+' '+filterTime(time.getHours())+':'+filterTime(time.getMinutes())+':'+filterTime(time.getSeconds());
    laydate.render({
        elem: '#release',
        type: 'datetime',
        trigger : "click",
        done : function(value, date, endDate){
            submitTime = value;
        }
    });
    form.on("radio(release)",function(data){
        if(data.elem.title == "定时发布"){
            $(".releaseDate").removeClass("layui-hide");
            $(".releaseDate #release").attr("lay-verify","required");
        }else{
            $(".releaseDate").addClass("layui-hide");
            $(".releaseDate #release").removeAttr("lay-verify");
            submitTime = time.getFullYear()+'-'+(time.getMonth()+1)+'-'+time.getDate()+' '+time.getHours()+':'+time.getMinutes()+':'+time.getSeconds();
        }
    });

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
        //截取文章内容中的一部分文字放入文章摘要
        var abstract = layedit.getText(editIndex).substring(0,50);
        //弹出loading
        $.post("/addClothSuccess/",{
            ID: $(".ID").val(),  //布样ID
            newsCode : $(".newsCode").val(),  //布样标题
            newsName : $(".newsName").val(),  //布样标题
            newsFactory : $(".newsFactory").val(),  //布样标题
            content : layedit.getContent(editIndex).split('<audio controls="controls" style="display: none;"></audio>')[0],  //文章内容
            newsImg : $(".thumbImg").attr("src"),  //缩略图
            CLOTH_REMAIN : $(".CLOTH_REMAIN").val(),//库存
            CLOTH_DEAL_REMAIN : $(".CLOTH_DEAL_REMAIN").val() //加工
        },function(res){
            // window.location.href="/addgoods/"
            if(res=='success'){
                top.layer.msg("布样添加成功！");
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