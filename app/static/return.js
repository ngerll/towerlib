

$(document).ready(function () {
    var areaneme = $('#username').text();
    $('#area').text(areaneme);
    $.ajaxSetup({cache: false});
});


function getborrowbookinfo() {
    $("#bookinfos").empty();
    $("#noborrow").empty();
    var borrowname = $("#nameqry").val();

    // if (borrowname == null || borrowname == "") {
    //     $("#bookinfos").empty();
    //     $("#noinfo").hide().show(500).html("<strong>请输入您的姓名</strong>");
    // } else {
    $("#noinfo").hide();
    readinfo(borrowname);
    // }

}

//
/*
 于页面上展现获取的书目列表
 */

function readinfo(borrowname) {
    getbook(borrowname);
}

/*
 获取借阅记录
 */

function getbook(borrowname) {

    var areaname = $("#username").text();
    var booksinfo = [];

    var binfoarry = {
        'borrowuser': borrowname,
        'isbn': '',
        'areaname': areaname
    };

    var binfourl = '/hblib/getborrowinfo';

    $.get(binfourl, binfoarry, function (respone) {

        if (respone.result.length < 1) {
            $("#noinfo").hide();
            $("#noinfo").show(500).html(borrowname + "没有未归还书籍");
            $("#nameqry").val("");
        } else {
            $("#noinfo").hide();
            booksinfo.push(respone.result);
            booksinfo.map(function (bk) {
                showbook(bk);
            });
        }
    }, 'json');
}

/*
 卡片封装

 submitresult
 */

function showbook(books) {

    books.map(function (book) {
        var borrowdate = book.borrowdate.replace('T', ' ');


        if (book.object_out == '0') {
            var bookinfo =

                "<tr> " +
                " <td> " + book.bookname + "</td> " +
                " <td> " + book.b_user + "</td> " +
                " <td> " + borrowdate + "</td> " +
                " <td> " +

                " <button class='btn btn-danger btn-sm' data-toggle='modal' data-target='#submitresult' " +
                " data-b_order= '" + book.b_order + "'" +
                " data-isbn= '" + book.isbn + "'" +
                " data-object= '" + book.object_out + "'" +
                " >发放实物</button> "

                + "</td> " +
                " </tr>"

        } else {
            var bookinfo =

                "<tr> " +
                " <td> " + book.bookname + "</td> " +
                " <td> " + book.b_user + "</td> " +
                " <td> " + borrowdate + "</td> " +
                " <td> " +

                " <button class='btn btn-info btn-sm' data-toggle='modal' data-target='#submitresult' " +
                " data-b_order= '" + book.b_order + "'" +
                " data-isbn= '" + book.isbn + "'" +
                " data-object= '" + book.object_out + "'" +
                " >归还图书</button> "

                + "</td> " +
                " </tr>"
        }

        $("#bookinfos").append(bookinfo);

        // if (book.object_out == '0'){
        //     var bookinfo = "<div class='card card-block text-center'> " +
        //     " <img class='card-img-top' " +
        //     " src='http://www.cisotec.net/static/bookpic/" + book.isbn + ".jpg '> " +
        //     " <hr class='divider'> " +
        //     " <div class='card-block'> " +
        //     " <h5 class='card-title text-danger'>" + book.bookname + "</h5> " +
        //     " <hr class='divider'> " +
        //     " <p class='card-text text-primary'>借阅人：" + book.b_user + "</p> " +
        //     " <p class='card-text text-primary'>借阅时间：" + borrowdate + "</p>" +
        //     " <button class='btn btn-danger btn-sm' data-toggle='modal' data-target='#submitresult' " +
        //     " data-b_order= '" + book.b_order + "'" +
        //     " data-isbn= '" + book.isbn + "'" +
        //     " data-object= '" + book.object_out + "'" +
        //     " >发放实物</button> " +
        //     " </div> " +
        //     " </div> ";
        // }else {
        //     var bookinfo = "<div class='card card-block text-center'> " +
        //     " <img class='card-img-top' " +
        //     " src='http://www.cisotec.net/static/bookpic/" + book.isbn + ".jpg '> " +
        //     " <hr class='divider'> " +
        //     " <div class='card-block'> " +
        //     " <h5 class='card-title text-danger'>" + book.bookname + "</h5> " +
        //     " <hr class='divider'> " +
        //     " <p class='card-text text-primary'>借阅人：" + book.b_user + "</p> " +
        //     " <p class='card-text text-primary'>借阅时间：" + borrowdate + "</p>" +
        //     " <button class='btn btn-info btn-sm' data-toggle='modal' data-target='#submitresult' " +
        //     " data-b_order= '" + book.b_order + "'" +
        //     " data-isbn= '" + book.isbn + "'" +
        //     " data-object= '" + book.object_out + "'" +
        //     " >归还图书</button> " +
        //     " </div> " +
        //     " </div> ";
        // }

        // $("#bookinfos").append(bookinfo);
    });


}


/*
 格式化日期
 */
Date.prototype.format = function (format) {
    var o = {
        "M+": this.getMonth() + 1, //month
        "d+": this.getDate(),    //day
        "h+": this.getHours(),   //hour
        "m+": this.getMinutes(), //minute
        "s+": this.getSeconds(), //second
        "q+": Math.floor((this.getMonth() + 3) / 3),  //quarter
        "S": this.getMilliseconds() //millisecond
    };
    if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
        (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)if (new RegExp("(" + k + ")").test(format))
        format = format.replace(RegExp.$1,
            RegExp.$1.length == 1 ? o[k] :
                ("00" + o[k]).substr(("" + o[k]).length));
    return format;
};


/*
 归还弹窗
 } */

$("#submitresult").on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);

    var back_date = new Date().format("yyyy-MM-dd hh:mm:ss"); //归还时间
    var b_order = button.data('b_order'); //借阅记录order
    var isbn = button.data('isbn'); //isbn编码
    var object = button.data('object'); //是否发放实物
    var areaname = $("#username").text(); //书籍归属地市


    if (object == '0') {
        giveobjec(b_order);
    } else {
        backbook(b_order, back_date, isbn, areaname);
    }


});


$('body').on('hidden.bs.modal', '.modal', function () {
    $(this).removeData('bs.modal');
});


/*
 还书封装
 */

function backbook(b_order, back_date, isbn, areaname) {

    var binfoarry = {
        'b_order': b_order,
        'back_date': back_date,
        'isbn': isbn,
        'areaname': areaname
    };

    var backurl = '/hblib/backbook';

    $.ajax({
        url: backurl,
        data: binfoarry,
        success: function (respone) {
            if (respone.result > 0) {
                $('#subresult').html("<strong>还书操作成功!<br/>请将实物归还图书架，谢谢!</strong>");
            } else if (respone.result == 'Error') {
                $('#subresult').html("<strong>还书失败!<br/>请重新操作，谢谢!</strong>");
            }
        },
        dataType: 'json'
    });
}


/*
 发放实物封装
 */

function giveobjec(b_order) {

    var goarry = {
        'b_order': b_order
    };
    
    var gourl = '/hblib/objectsubmit';

    $.get(gourl, goarry, function (res) {
        if (res.result > 0) {
            $('#subresult').html("<strong>发放实物成功！</strong>");
        } else if (res.result == 'Error') {
            $('#subresult').html("<strong>系统错误!<br/>请重新操作，谢谢!</strong>");
        }
    }, 'json');
}
