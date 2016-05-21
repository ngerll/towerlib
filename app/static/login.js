/**
 * Created by Administrator on 2016/5/19.
 */

$(document).ready(function () {
    $("#changeform").hide();
    var loginmsg = $("#msg").text().length;
    if (loginmsg > 0) {
        $("#loginmsg").show();
    } else {
        $("#loginmsg").hide();
    }
});


function changepasswd() {
    $("#loginmsg").hide();
    $("#loginform").hide(500);
    $("#changeform").show(500);
}

function gotologin() {
    $("#loginmsg").hide();
    $("#changeform").hide(500);
    $("#loginform").show(500);
}


$("#changepass").on('click', function () {
    changeusername = $("#changeusername").val();
    oldpassword = $("#oldpassword").val();
    newpassword = $("#newpassword").val();


    data = {
        'username': changeusername,
        'oldpasswd': oldpassword,
        'newpasswd': newpassword
    };

    url = '/hblib/changepasswd';

    if (newpassword.length > 0) {
        $.post(url, data, function (res) {
            if (res.result == 1) {
                $("#loginmsg").text("密码修改成功，请返回登录页进行登录");
                $("#loginmsg").show();
            } else {
                $("#loginmsg").text("密码修改失败，请确认用户或原密码是否正确，且新密码不能与原密码相同!");
                $("#loginmsg").show();
            }

        }, 'json');
    } else {
        $("#loginmsg").text("新密码不能为空!");
        $("#loginmsg").show();
    }
});
