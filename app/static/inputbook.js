/**
 * Created by Administrator on 2016/5/19.
 */

$(document).ready(function () {
    $.ajaxSetup({cache: false});
    $("#downres").empty();
});

$('body').on('hidden.bs.modal', '.modal', function () {
    $(this).removeData('bs.modal');
});

//全选
$("#selectall").on('click', function () {
    var checks = $(":checkbox");

    for (var i = 0; i < checks.length; i++) {
        checks[i].checked = true
    }
});

//全不选
$("#cancelselect").on('click', function () {
    var checks = $(":checkbox");

    for (var i = 0; i < checks.length; i++) {
        checks[i].checked = false
    }
});

function delselect() {
    var checks = $(":checkbox");
    for (var i = 0; i < checks.length; i++) {
        if (checks[i].checked == true) {

        }
    }
}

//删除书籍弹窗
function showdelmodal() {
    var checks = $(":checkbox");
    var s = 0;
    for (var i = 0; i < checks.length; i++) {
        if (checks[i].checked == true) {
            s = s + 1
        }
    }

    if (s > 0) {
        $("#delsubmit").modal('show');

        checkbooks = [];

        $("#delsubmit").on('shown.bs.modal', function () {
            $("#delbookinfo").empty();

            for (var i = 0; i < checks.length; i++) {
                if (checks[i].checked == true) {
                    var wantdel = $(checks[i]).parent().next().text();

                    $("#delbookinfo").append("<p>将要删除的书籍为：" + wantdel + "</p>");
                    checkbooks.push(checks[i].value);
                }
            }

            document.getElementById("delbtn").setAttribute("data-delbook", checkbooks);
            checkbooks = [];

        })
    }
}

//删除书籍调用
function delbook() {
    $("#resfooter").hide();
    delbookid = document.getElementById("delbtn").getAttribute("data-delbook");
    data = {'data': delbookid};

    url = '/hblib/delbook';
    $("#resinfo").empty();
    $("#resinfo").html("<div class='alert alert-info' role='alert'><strong>请稍等，正在处理中...</strong></div>");


    $.post(url, data, function (res, status) {
        $("#resinfo").empty();
        if (status == 'success' && res.result > 0) {
            $("#resinfo").html("<div class='alert alert-info' role='alert'><strong>已成功删除书籍" + res.result + "本</strong></div>")
        } else {
            $("#resinfo").html("<div class='alert alert-info' role='alert'><strong>删除失败!</strong></div>")
        }
        $("#resfooter").show();
        readinfo();

    }, 'json');

    $("#delsubmit").modal('hide');
    $("#resmodal").modal('show');
    document.getElementById("delbtn").removeAttribute("data-delbook");
}


/*
 根据关键字获取信息，页面展现整体封装
 */

function readinfo() {
    var booksinfo = [];

    $("#booklist").empty(); //清空数目列表

    var keytype = $("#qrytype").val(); //获取类型
    var keyword = $("#qryword").val(); //获取关键字
    var areaname = $("#area").text(); //获取区域


    binfourl = '/hblib/getbooklist';
    qrydata = {'keytype': keytype, 'keyword': keyword, 'areaname': areaname};

    $.get(binfourl, qrydata, function (respone) {
        booksinfo.push(respone.result);

        booksinfo.map(function (booklist) {
            showbook(booklist);
        })
    }, 'json');

}


/*
 于页面上展现获取的书目列表
 */
function showbook(booklist) {
    booklist.map(function (book) {

        var bookinfo =
            "<tr> " +
            "<td><input type='checkbox' value='" + book.id + "'></td>" +
            " <td> " + book.bookname + "</td> " +
            " <td> " + book.isbn + "</td> " +
            " <td> " + book.bookwriter + "</td> " +
            " <td> " + book.booksend + "</td> " +
            " <td> " + book.bookkind + "</td> " +
            " <td> " + book.booknumber + "</td> " +
            " <td> " + book.bookamount + "</td> " +
            " </tr>";

        $("#booklist").append(bookinfo);
    });
}


$("#bookfile").change(function () {
    $(".file-custom").text();
    var fileinfo = $("#bookfile").val().split('\\');
    var filename = fileinfo[fileinfo.length - 1];
    $(".file-custom").text(filename);
});


//导入书籍excel

function upload() {
    var filedata = new FormData(document.getElementById("file"));
    var $areaname = $("#area").text();
    document.getElementById("inputjson").removeAttribute('data-inputbook');
    $("#inputjson").show();

    $.ajax({
        url: "/hblib/upload",
        type: "POST",
        data: filedata,
        contentType: false,
        processData: false,
        cache: false,
        success: function (res) {
            if (res.result != 'Error' && res.result.length > 0) {
                $("#inputsubmit").modal('show');

                $("#inputsubmit").on('shown.bs.modal', function () {
                    $("#inputbookinfo").empty();
                    res.result.map(function (book) {
                        if (book[1] != 'isbn') {
                            if (book[7] == $areaname) {

                                $("#inputbookinfo").append("<p>" + book[0] + "</p>");
                            } else {
                                $("#inputbookinfo").append("<p>导入文件中的‘市州’字段内容与当前管理后台所属市州不符，请检查导入文件！");
                            }

                        }
                    })
                });

                var count = 0;
                var inputbooks = JSON.parse(JSON.stringify(res)).result;
                inputbooks.map(function (res) {
                    if (res[1] != 'isbn') {
                        if (res[7] == $areaname) {

                        } else {
                            count = count + 1;
                        }
                    }
                });

                if (count == 0) {
                    document.getElementById("inputjson").setAttribute('data-inputbook', JSON.stringify(res));
                } else {
                    $("#inputjson").hide();
                }
            }
        },
        dataType: 'json'
    })
}

//将书籍存入数据库
function saveinput() {

    $("#resfooter").hide();

    url = '/hblib/inputbook';
    $("#resinfo").empty();
    $("#resinfo").html("<div class='alert alert-info' role='alert'><strong>请稍等，正在处理中...</strong></div>");

    var jsondata = document.getElementById("inputjson").getAttribute("data-inputbook");

    $.post(url, jsondata, function (res, status) {
        $("#resinfo").empty();
        if (status == 'success' && res.result > 0) {
            $("#resinfo").html("<div class='alert alert-info' role='alert'><strong>已成功录入书籍" + res.result + "本</strong></div>")
        } else {
            $("#resinfo").html("<div class='alert alert-info' role='alert'><strong>录入失败!</strong></div>")
        }
        $("#resfooter").show();
        readinfo();
    }, 'json');

    $("#inputsubmit").modal('hide');
    $("#resmodal").modal('show');

    document.getElementById("inputjson").removeAttribute("data-inputbook");
}

//下载书籍图片
function downpic() {
    $("#downres").html("<div class='alert alert-info' role='alert'><strong>正在下载中，请稍等....</strong></div>");

    var areaname = $("#area").text();
    var params = {'areaname': areaname};
    url = '/hblib/downpic';

    $.get(url, params, function (res, status) {
        if (status == 'success' && res.result > 0) {
            $("#downres").html("<div class='alert alert-info' role='alert'><strong>" + res.result + "本书籍图片已更新</strong></div>");
        } else {
            $("#downres").html("<div class='alert alert-info' role='alert'><strong>无书籍图片需下载</strong></div>");
        }
    }, 'json')
}