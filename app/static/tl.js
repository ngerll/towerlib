/**
 * Created by Administrator on 2016/4/21.
 */

//
// $('#submitresult').on('hidden.bs.modal', function () {
//     location.reload();
// });
/*
 初始化页面
 */
area = {
    'branch': '省分',
    'wuhan': '武汉',
    'huangshi': '黄石',
    'huanggang': '黄冈',
    'suizhou': '随州',
    'jianghhan': '江汉',
    'yichang': '宜昌',
    'jingzhou': '荆州',
    'xiangyang': '襄阳',
    'xiaogan': '孝感',
    'shiyan': '十堰',
    'enshi': '恩施',
    'xianning': '咸宁',
    'jingmen': '荆门',
    'ezhou': '鄂州'
};

$(document).ready(function () {
    var areacode = $("#areacode").text();
    var areaname = area[areacode];
    $("#areaname").text(areaname);

    $.ajaxSetup({cache: false});
    readinfo();

});


/*
 根据关键字获取信息，页面展现整体封装
 */


function readinfo() {

    var booksinfo = [];

    $("#bookinfos").empty(); //清空数目列表


    $("#bookinfos").masonry().masonry('destroy'); //初始化masonry状态


    var keytype = $("#qrytype").val(); //获取类型
    var keyword = $("#qryword").val(); //获取关键字
    var areaname = $("#areaname").text(); //获取区域


    binfourl = '/hblib/getbooklist';
    qrydata = {'keytype': keytype, 'keyword': keyword, 'areaname': areaname};

    /*  $.get(binfourl, qrydata, function (respone) {
     booksinfo.push(respone.result);

     booksinfo.map(function (booklist) {
     showbook(booklist);
     })
     }, 'json'); */

    $.ajax({
        url: binfourl,
        data: qrydata,
        dataType: "json"
    }).done(function (res) {
        booksinfo.push(res.result);
        booksinfo.map(function (booklist) {
            showbook(booklist);
        });
    }).done(function () {
        $("#bookinfos").imagesLoaded(function () {
            $("#bookinfos").masonry({
                itemSelector: '.book',
                isAnimated: true,
                percentPosition: true
            });
        });
    });
}

/*
 于页面上展现获取的书目列表
 */
function showbook(books) {
    books.map(function (book) {
        if (book.bookamount > 0) {
            var bookinfo = "<div class='book'> " +
                " <div class='col-xs-6 text-center'>" +
                " <img class='bimg' " +
                " src='/static/bookpic/" + book.isbn + ".jpg '> " +
                " </div>" +
                " <div class='col-xs-6 bookdetails'> " +
                " <p class='text-danger btitle'>" + book.bookname + "</p>" +
                " <p class='text-info bkind'>" + book.bookkind + "</p> " +
                " <p class='card-text text-primary bwriter'>" + book.bookwriter + "</p> " +
                " <p class='card-text text-primary'>剩余：" + book.bookamount + "本</p>" +
                " <button class='btn btn-danger btn-sm' data-toggle='modal' data-target='#buttonalert' " +
                " data-bookname= '" + book.bookname + "'" +
                " data-isbn= '" + book.isbn + "'" +
                " >就这本</button> " +
                " </div> " +
                " </div> ";
        } else {
            var bookinfo = "<div class='book'> " +
                " <div class='col-xs-6 text-center'>" +
                " <img class='bimg' " +
                " src='/static/bookpic/" + book.isbn + ".jpg '> " +
                " </div>" +
                " <div class='col-xs-6 bookdetails'> " +
                " <p class='text-danger btitle'>" + book.bookname + "</p>" +
                " <p class='text-info bkind'>" + book.bookkind + "</p> " +
                " <p class='card-text text-primary bwriter'>" + book.bookwriter + "</p> " +
                " <p class='card-text text-muted'>剩余：" + book.bookamount + "本</p>" +
                " <button class='btn btn-secondary btn-sm' data-toggle='modal' data-target='#buttonalert' " +
                " data-bookname= '" + book.bookname + "'" +
                " data-isbn= '" + book.isbn + "'" +
                " disabled >借出ing..</button> " +
                " </div> " +
                " </div> ";
        }

        $("#bookinfos").append(bookinfo);
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
 借阅弹窗
 */


$('body').on('hidden.bs.modal', '.modal', function () {
    $(this).removeData('bs.modal');
    $("#borrowbookuser").val("");
});

$('#cancelborrow').on('click', function () {
    $('#buttonalert').modal('hide');
});

/*
 给弹窗中的提交数据绑定数据
 */


$("#buttonalert").on('show.bs.modal', function (event) {
    $('#collapsename').collapse('hide');
    var button = $(event.relatedTarget);

    var bookname = button.data('bookname'); //书名
    var isbn = button.data('isbn');  //isbn编号


    $('#borrowconfirm').data('bookname', bookname);
    $('#borrowconfirm').data('isbn', isbn);

});

/*
 确定弹窗的数据提交
 */

$('#borrowconfirm').on('click', function () {
    var borrowdate = new Date().format("yyyy-MM-dd hh:mm:ss"); //借阅时间
    var bookname = $('#borrowconfirm').data('bookname');
    var isbn = $('#borrowconfirm').data('isbn');

    subconfirm(bookname, isbn, borrowdate);

});

/*
 提交数据
 */

function subconfirm(bookname, isbn, borrowdate) {
    var borrowuser = $("#borrowbookuser").val(); //借阅人
    var areaname = $("#areaname").text(); //获取区域

    if (borrowuser == null || borrowuser == "") {
        $('#collapsename').collapse('show');
    } else {
        $('#buttonalert').modal('hide');
        borrowInfosave(isbn, borrowuser, bookname, borrowdate, areaname);
        $('#submitresult').modal('show');
    }

};


/*
 借阅书籍封装
 */
function borrowInfosave(isbn, borrowuser, bookname, borrowdate, areaname) {

    var borrowinfourl = '/hblib/getborrowinfo';
    var data = {
        'isbn': isbn,
        'borrowuser': borrowuser,
        'areaname': areaname
    };
    $.get(borrowinfourl, data, function (respone) {
        if (respone.result.length > 0) {
            console.log(respone.result);

            $('#subresult').text('这本书您正在借阅，尚未归还');
        } else {
            var userbrowdat = {'isbn': '', 'borrowuser': borrowuser, 'areaname': areaname};

            $.get(borrowinfourl, userbrowdat, function (res) {
                if (res.result.length > 0) {
                    $('#subresult').html("您有书未归还，请归还后再借阅，谢谢！");
                } else {
                    saveBorrowInfo(isbn, borrowuser, bookname, borrowdate, areaname);
                    var borrowinfo = "您好,<strong>" + borrowuser + "</strong> : </br>您成功借阅 : <strong>《" + bookname + "》</strong></br>借阅时间 : <strong>" + borrowdate + '</strong>';
                    $('#subresult').html(borrowinfo);
                }
            }, 'json');

        }
    }, 'json');
}

/*
 存储借阅记录
 */
function saveBorrowInfo(isbn, borrowuser, bookname, borrowdate, areaname) {

    var savebinfourl = '/hblib/saveborrowinfo';
    var data = {
        'isbn': isbn,
        'borrowuser': borrowuser,
        'bookname': bookname,
        'borrowdate': borrowdate,
        'areaname': areaname
    };
    $.get(savebinfourl, data, function (respone) {
        readinfo();
    }, 'json');
}
