/*!
 * style.jss
 * http://givemefive.top/
 *
 * Copyright 2020, huangdatian
 * Date: Sat Feb 13 22:33:48 2020
 */

var g_prevGrayBtn = 1;//上一个变灰的按钮
var g_currPageNmu = 1;//当前页码
var g_pageCount = 0;//页数

function SetCurrTime() {
    var today = new Date();
    var m_year = today.getFullYear();
    var m_mon = today.getMonth() + 1;
    var m_date = today.getDate();
    var m_day = today.getDay();
    var m_hour = today.getHours();
    var m_minute = today.getMinutes();
    var m_second = today.getSeconds();
    if (m_hour < 10) {
        m_hour = "0" + m_hour;
    }
    if (m_minute < 10) {
        m_minute = "0" + m_minute;
    }
    if (m_second < 10) {
        m_second = "0" + m_second;
    }

    var m_currWeek;
    switch (m_day) {
        case 0: m_currWeek = "星期日";
            break;
        case 1: m_currWeek = "星期一";
            break;
        case 2: m_currWeek = "星期二";
            break;
        case 3: m_currWeek = "星期三";
            break;
        case 4: m_currWeek = "星期四";
            break;
        case 5: m_currWeek = "星期五";
            break;
        case 6: m_currWeek = "星期六";
            break;
    }

    document.getElementById('date').innerHTML = m_year + "年\r" + m_mon + "月\r" + m_date + "日\r" + m_currWeek;
    document.getElementById('time').innerHTML = m_hour + ":" + m_minute + ":" + m_second;
    setTimeout(function () {
        SetCurrTime()
    }, 1000);
}

function PageCliked(id) {
    //alert(id);
    $("#" + id).css({ 'background-color': '#98FB98' });
    $("#" + g_prevGrayBtn).css({ 'background-color': '#AFEEEE' });
    g_prevGrayBtn = id;
    //发送post
    $.ajax({
        type: "POST",
        url: "/GetPage/" + id,
        dataType: "text",
        success: function (result) {
            /*alert(result);*/
            //处理返回html
            $("#content").attr("src", result);
        }
    });
}

function InitUi() {
    //初始化伸缩栏
    var box = document.getElementById("test")
    var btn = document.getElementById("btn")
    btn.onclick = function () {
        if (box.offsetLeft == 0) {
            box.style['margin-left'] = -100 + "px";
        } else {
            box.style['margin-left'] = 0 + "px"
        }
    }

    //请求最新消息
    $.ajax({
        type: "POST",
        data: "",
        url: "/GetUploadMsg",
        dataType: "text",
        success: function (result) {
            //右下角弹窗
            var jsonResult = JSON.parse(result);
            //刷新数据
            var strArtiles = "";
            var uploadTime = jsonResult["UploadTime"];
            var uploadPath = jsonResult["UploadPath"];
            var uploadAdmin = jsonResult["UploadAdmin"];
            var uploadBooks = jsonResult["UploadBooks"];
            g_pageCount = jsonResult["HistorySize"];
            for (let i = 0; i < jsonResult["LastUpload"].length; ++i) {
                strArtiles += jsonResult["LastUpload"][i] + " "
            }
            $("#rbj-title").html(strArtiles);
            $("#rbj-time").html(uploadTime);
            $("#rbj-path").html(uploadPath);
            $("#rbj-autho").html(uploadAdmin);
            $("#rbj-book").html(uploadBooks);
            $("#page-count").html(g_pageCount);

            $("#rbj").slideToggle(800);
            $("#rbj-close").click(function () {
                $("#rbj").slideToggle(800);
            });

            //初始化page-btn
            for (let i = g_currPageNmu; i <= 10; i++) {
                let li = '<li style="float:left;"><button class="page-btn" id="' + i + '" onclick="PageCliked(this.id)">' + i + '</button></li>'
                $(".page-bottom").append(li);
            }

            PageCliked(1);
        }
    });
    //上一页 下一页
    $("#prev-page").click(function () {
        if (g_currPageNmu > 1) {
            g_currPageNmu -= 1;
            $(".page-bottom").children("li").remove();
            for (let i = g_currPageNmu; i <= (g_currPageNmu + 10); i++) {
                let li = '<li style="float:left;"><button class="page-btn" id="' + i + '" onclick="PageCliked(this.id)">' + i + '</button></li>'
                $(".page-bottom").append(li);
            }
            PageCliked(g_currPageNmu);
        }
    });
    $("#next-page").click(function () {
        if ((g_currPageNmu + 10) <= g_pageCount) {
            $(".page-bottom").children("li").remove();
            for (let i = g_currPageNmu; i <= (g_currPageNmu + 10); i++) {
                let li = '<li style="float:left;"><button class="page-btn" id="' + i + '" onclick="PageCliked(this.id)">' + i + '</button></li>'
                $(".page-bottom").append(li);
            }
        }
        if (g_currPageNmu <= g_pageCount) {
            g_currPageNmu += 1;
            PageCliked(g_currPageNmu);
        }
    });
}

function EditCodeClicked() {
    //创建窗口
    let iHtml = `
        <textarea id="editor" spellcheck="false">Click to Editor...</textarea>
        <div style="background-color: #D8BFD8;width: 100%;">
            <input type="text" id="editcode-name"/>
            <select id="editcode-elect"></select>
            <input id="edit-Small" type="button" value="-" style="float:left;margin-left:4px;width:12px;">
            <input id="edit-Distance" type="text" value="10" style="float: left;width: 31px;">
            <input id="edit-Extend" type="button" value="+" style="float: left;width: 12px;margin-right: 1px;">
            <input id="edit-save" type="button" value="保存" style="width: 48px;margin-left: -3px;">
            <input id="edit-open" type="button" value="打开" style="width: 48px;margin-left: -3px;">
            <input id="edit-raname" type="button" value="重命名" style="width: 48px;margin-left: -3px;">
            </div>
        `;
    editCode = new Windows("body", "editCode", "编辑器", iHtml);
    $("#winTitleeditCode").css({ "height": "24px", "width": "100%;" });//标题
    $("#editCode").css({ "height": "372px", "width": "580px", "background-color": "#D8BFD8" });//窗体
    editCode.OpenWindow();
    $("#winTitleeditCode-close").click(function () {
        editCode.CloseWindow();
    });
    //允许输入tab键
    $("#editor").on('keydown', function (e) {
        if (e.keyCode == 9) {
            e.preventDefault();
            var indent = '    ';
            var start = this.selectionStart;
            var end = this.selectionEnd;
            var selected = window.getSelection().toString();
            selected = indent + selected.replace(/\n/g, '\n' + indent);
            this.value = this.value.substring(0, start) + selected + this.value.substring(end);
            this.setSelectionRange(start + indent.length, start + selected.length);
        }
    })
    //重命名
    $("#edit-raname").click(function () {
        var fileName = $("#editcode-name").val();

        let iHtml = `
        <div style="background-color: #D8BFD8;width: 100%;">
            <dd style="line-height: 30px;height: 90px;">
                <dl>旧文件名：${fileName}</dl>
                <dl>新文件名：<input id="rename-new" type="text"/></dl>
                <dl>
                    <input id="rename-ok" type="button" value="确定" style="width: 68px;margin-left: 50px;">
                    <input id="rename-cancle" type="button" value="取消" style="width: 68px;margin-left: 50px;">
                </dl>
            </dd>
        </div>
        `;
        tipWin = new Windows("body", "Rename", "提示", iHtml);
        $("#winTitleRename").css({ "height": "24px", "width": "100%;" });//标题
        $("#Rename").css({
            "height": "114px",
            "width": "300px",
            "background-color": "#D8BFD8",
            "border": "1px solid red"
        });//窗体
        tipWin.OpenWindow();
        $("#winTitleRename-close").click(function () {
            tipWin.CloseWindow();
        });
        $("#rename-cancle").click(function () {
            tipWin.CloseWindow();
        });
        
        $("#rename-ok").click(function () {
            var strNewName = $("#rename-new").val();
            if (fileName !== "" && strNewName !== "") {
                var mapSend = {
                    "FileName": fileName,
                    "NewFileName": strNewName
                };
                $.ajax({
                    type: "POST",
                    data: JSON.stringify(mapSend),
                    url: "/EditCodeRename",
                    dataType: "text",
                    success: function (result) {
                        alert(result);
                    }
                });
            }
            else {
                alert("文件名不能为空！");
            }
            tipWin.CloseWindow();

        });
    });
    //保存
    document.getElementById("edit-save").onclick = function (e) {
        var content = $("#editor").val();
        var fileName = $("#editcode-name").val();

        let iHtml = `
        <div style="background-color: #D8BFD8;width: 100%;">
            <dd style="line-height: 30px;height: 90px;">
                <dl>文件是否保存为：</dl>
                <dl style="margin-left: 20px;color: red;">${fileName}</dl>
                <dl>
                    <input id="edit-ok" type="button" value="确定" style="width: 68px;margin-left: 50px;">
                    <input id="edit-cancle" type="button" value="取消" style="width: 68px;margin-left: 50px;">
                </dl>
            </dd>
        </div>
        `;
        tipWin = new Windows("body", "Tip", "提示", iHtml);
        $("#winTitleTip").css({ "height": "24px", "width": "100%;" });//标题
        $("#Tip").css({
            "height": "114px",
            "width": "300px",
            "background-color": "#D8BFD8",
            "border": "1px solid red"
        });//窗体
        tipWin.OpenWindow();
        $("#winTitleTip-close").click(function () {
            tipWin.CloseWindow();
        });
        $("#edit-cancle").click(function () {
            tipWin.CloseWindow();
        });

        $("#edit-ok").click(function () {
            if (fileName !== "") {
                var mapSend = {
                    "FileName": fileName,
                    "Content": content
                };
                $.ajax({
                    type: "POST",
                    data: JSON.stringify(mapSend),
                    url: "/EditCodeSave",
                    dataType: "text",
                    success: function (result) {
                        alert(result);
                    }
                });
            }
            else {
                alert("文件名不能为空！");
            }
            tipWin.CloseWindow();

        });

        

    };
    //请求代码文件
    $.ajax({
        type: "POST",
        url: "/GetEditFile",
        dataType: "text",
        success: function (result) {
            var jsonRet = JSON.parse(result);
            for (let i = 0; i < jsonRet["EdiitFile"].length; ++i) {
                $("#editcode-elect").append("<option>" + jsonRet["EdiitFile"][i] + "</option>");
            }
            $("#editcode-elect").click(function () {
                var editFile = $("#editcode-elect").val();
                $("#editcode-name").val(editFile);
            });
        }
    });
    //打开文件请求
    $("#edit-open").click(function () {
        var fileName = $("#editcode-name").val();
        $.ajax({
            type: "POST",
            data: fileName,
            url: "/EditCodeOpen",
            dataType: "text",
            success: function (result) {
                //alert(result);
                var jsonData = JSON.parse(result);
                var strCode = "";
                for (let i = 0; i < jsonData["code"].length; ++i) {
                    strCode += jsonData["code"][i];
                }
                $("#editor").val(strCode);
            }
        });
    });
    //缩放
    EdigCodeResize();
}

function EdigCodeResize() {
    var nSize = $("#editCode").width();
    $("#edit-Extend").click(function () {
        if (nSize < 1040) {
            var nadd = $("#edit-Distance").val();
            nSize += Math.abs(nadd);
        }
        var resizeWidth = nSize + "px";
        $("#editCode").css({ "width": resizeWidth });//窗体
    });
    $("#edit-Small").click(function () {
        if (nSize > 450) {
            var nadd = $("#edit-Distance").val();
            nSize -= Math.abs(nadd);
        }
        var resizeWidth = nSize + "px";
        $("#editCode").css({ "width": resizeWidth });//窗体

    });
}


(function () {
    SetCurrTime();
    InitUi();

    //g_event.MouseRightClick(document.getElementById("rightMenu"), document.getElementById("btn"));
    //g_event.OnRightMenu();
})();
