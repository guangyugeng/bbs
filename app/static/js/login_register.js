var log = function() {
  console.log(arguments)
}




var bindEventLoginToggle = function(){
    log("login toggle")
    $(".check-box").on("click", "ul.nav-tabs li" ,function(event) {
        log('Toggle')
        $("ul.nav-tabs li").removeClass("active");
        $(this).addClass("active");
        $(".login-register-item").addClass("hide");
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).removeClass("hide");
        log('pass')
        return false;
    });

}


var bindEventLogin = function(event){
    $("#login-form").submit(function(event) {

        var view = $(event.target).closest('#login-box')
        var username = $(view).find('.username').first().val()
        var password = $(view).find('.password').first().val()
        var form = {
            'username': username,
            'password': password
        }
        log(username,password)

        var response = function(r){
            log(r,r.valid,r.msg)
            if (r.valid){
                window.location.href = document.referrer
            }
            else{
                var message = r.msg
                for (var k in message){
                    var p_message = $(view).find(k).first()
                    p_message.text(message[k])
                    p_message.addClass('error')
                }
            }
        }
        api.login(form, response)
    });
}


var bindEventRegister = function(event){
    $("#register-form").submit(function(event) {

    var view = $(event.target).closest('#register-box')
    var username = $(view).find('.username').first().val()
    var nickname = $(view).find('.nickname').first().val()
    var password = $(view).find('.password').first().val()
    var email = $(view).find('.email').first().val()

    var form = {
        'username': username,
        'nickname': nickname,
        'password': password,
        'email': email
    }
    log(form.email,email,username,password,nickname)
    var response = function(r){
        log(r,r.valid,r.msg)
        if (r.valid){
            alert("success")
            window.location.href = document.referrer
        }
        else{
            alert("fail")
            var message = r.msg
            log(message)
            for (var k in message){
                var p_message = $(view).find(k).first()
                p_message.text(message[k])
               p_message.addClass('error')
            }
        }
    }
    api.register(form, response)
    });
}


var bindEventRegisterValid = function(){

    var view = '#register-box'
    var username = $(view).find('.username').first()
    var password = $(view).find('.password').first()
    var confirm = $(view).find('.confirm-password').first()
    var email = $(view).find('.email').first()

    username.keyup(function()
    {
      log('keyup')
      name= username.val();//val()方法返回或设置被选元素的值。
      if(name.length < 4){//调用下面的自定义len函数
      username.next('.help-username').html("<font color=red>注册名称必须大于等于4位</font>");
      }else{
      log('keyup f')
      username.next('.help-username').html("<font color=red>符合要求</font>");
      }
    })
    username.blur(function(){
    name= username.val()
    log('blur')
    })

}




var bindLoginRegisterEvents = function() {
    log("bindEventLoginToggle")
    bindEventLoginToggle()
    bindEventRegister()
    bindEventLogin()
}


$(document).ready(function(){
    log('L_R')
    bindLoginRegisterEvents()

})