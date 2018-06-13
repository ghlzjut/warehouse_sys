layui.use(['form','layer','jquery'],function(){
    var form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer
        $ = layui.jquery;

    $(".loginBody .seraph").click(function(){
        layer.msg('功能暂未开发',{
            time:5000
        });
    });

    form.verify({
      userName: function(value, item){ //value：表单的值、item：表单的DOM对象
        if(!new RegExp("^[a-zA-Z0-9_\u4e00-\u9fa5\\s·]+$").test(value)){
          return '用户名不能有特殊字符';
        }
        if(/(^\_)|(\__)|(\_+$)/.test(value)){
          return '用户名首尾不能出现下划线\'_\'';
        }
        if(/^\d+\d+\d$/.test(value)){
          return '用户名不能全为数字';
        }
      }
      //我们既支持上述函数式的方式，也支持下述数组的形式
      //数组的两个值分别代表：[正则匹配、匹配不符时的提示文字]
      ,password: [
        /^[\S]{6,12}$/
        ,'密码必须6到12位，且不能出现空格'
      ]
    });
    //登录按钮
    // form.on("submit(login)",function(data){
    //     $.get("/loginSuccess/",{
    //             userName : $(".userName").val(),
    //             password : $(".password").val(),
    //             code : $(".code").val(),
    //         },function (res) {
    //             if(res=='fail'){
    //                 layer.msg('用戶名密碼錯誤')
    //             }
    //             else if(res=='success'){
    //                 window.location.href = "/index";
    //             }
    //             // parent.location.reload();
    //         });
    //     return false
    //     // $(this).text("登录中...").attr("disabled","disabled").addClass("layui-disabled");
    //     // setTimeout(function(){
    //     //     window.location.href = "/index";
    //     // },1000);
    //     // return false;
    // });

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
