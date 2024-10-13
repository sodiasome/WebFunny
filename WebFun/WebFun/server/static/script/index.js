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

function JumpPage(id) {
    PageCliked($("#" + id).text());
}

function SearchClicked() {
    //获取需要查找内容
    let strSearch = $("input[name='searchterm']").val();
    //获取分类 查找域
    let strOption = $("select").find("option:selected").text();
    let mapSend = {
        "title": strSearch,
        "module": strOption
    };
    //发送查找请求
    $.ajax({
        type: "POST",
        data: JSON.stringify(mapSend),
        url: "/SearchArticle",
        dataType: "text",
        success: function (result) {
            //处理反馈
            //显示反馈
            var retData = JSON.parse(result);
            var strRet = "";
            for (key in retData) {
                if ("null" !== key) {
                    strRet += "<dd>" + (key + '<button id="jump-' + retData[key]+'" onclick="JumpPage(this.id)">' + retData[key] + "</button>") + "</dd>";
                } 
            }
            let iHtml = `
                <div style="overflow: auto;height: 154px;width: 100%;padding-left: 8px;border: 1px solid #ffffff;">
                    <dl style="background-color:"#d4d4d4";">
                        ${strRet}
                    </dl> 
                </div>
            `;
            searchRet = new Windows("body", "searchRet", "查找结果", iHtml);
            searchRet.OpenWindow();
            $("#winTitlesearchRet-close").click(function () {
                searchRet.CloseWindow();
            });
        }
    });
}

function InitUi() {
    //初始化伸缩栏
    var box = document.getElementById("test")
    var btn = document.getElementById("btn")
    btn.onclick = function () {
        if (box.offsetLeft == 0) {
            box.style['margin-left'] = -200 + "px"
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
            for (let i = g_currPageNmu; i <= (g_currPageNmu+10); i++) {
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
(function () {
    SetCurrTime();
    InitUi();
})();
