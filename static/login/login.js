layui.use(['form','layer','jquery'],function(){
    var form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer
        $ = layui.jquery;

    $(".loginBody .seraph").click(function(){
        layer.msg('功能暂未开发',{
            time:5000
        });
    })

    //登录按钮
    form.on("submit(login)",function(data){
        $.get("/loginSuccess/",{
                userName : $(".userName").val(),
                password : $(".password").val(),
                code : $(".code").val(),
            },function (res) {
                if(res=='fail'){
                    layer.msg('用戶名密碼錯誤')
                }
                else if(res=='success'){
                    window.location.href = "/index";
                }
                // parent.location.reload();
            })
        return false
        // $(this).text("登录中...").attr("disabled","disabled").addClass("layui-disabled");
        // setTimeout(function(){
        //     window.location.href = "/index";
        // },1000);
        // return false;
    })

    //表单输入效果
    $(".loginBody .input-item").click(function(e){
        e.stopPropagation();
        $(this).addClass("layui-input-focus").find(".layui-input").focus();
    })
    $(".loginBody .layui-form-item .layui-input").focus(function(){
        $(this).parent().addClass("layui-input-focus");
    })
    $(".loginBody .layui-form-item .layui-input").blur(function(){
        $(this).parent().removeClass("layui-input-focus");
        if($(this).val() != ''){
            $(this).parent().addClass("layui-input-active");
        }else{
            $(this).parent().removeClass("layui-input-active");
        }
    })
})
