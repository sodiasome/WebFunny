function Windows(parentElement, winId, titleText, contentHtml) {
    this.winID = winId;
    //Windows.prototype.mapMindows = {};
    this.winParent = parentElement;
    this.winTitle = titleText;
    this.winTitleID = "winTitle" + winId;
    this.CreateWindowElement(contentHtml);
    this.SetWindowCss();
    this.MoveWindow();
}

Windows.prototype = {
    SetWindowCss: function () {
        $("#" + this.winID).css(
            {
                "background-color": "#BDB76B",
                "color": "#ffffff",
                "position": "fixed",
                "top": "40%",
                "left": "40%",
                "height": "200px",
                "width": "280px",
                "display": "block",
            }
        );
        $("#" + this.winTitleID).css(
            {
                "background-color": "#BDB76B",
                "font-weight": "bold",
                "color": "#ffffff",
                "width": "100%",
            }
        );
    },
    GetWindowId: function () {
        return this.winID;
    },
    CreateWindowElement: function (contentHtml) {
        var winBody = document.createElement("div");
        winBody.id = this.winID;
        $(this.winParent).append(winBody);
        var winHtml = `<div id="${this.winTitleID}">${this.winTitle}
            <input type="button" id="${this.winTitleID}-close" value="X" style="float:right;color:red;" />
            </div>` + contentHtml;
        $("#" + this.winID).html(winHtml);
    },
    //窗口动画
    MoveWindow: function () {
        var windowEle = document.getElementById(this.winID);
        $("#" + this.winTitleID).mousedown(function (e) {
            var e = e || event;
            var disX = e.clientX - windowEle.offsetLeft;
            var disY = e.clientY - windowEle.offsetTop;
            if (windowEle.setCapture) {
                windowEle.setCapture; //将鼠标锁定在该控件上
            }
            document.onmousemove = function (ev) {
                var ev = ev || event;
                windowEle.style.top = ev.clientY - disY + 'px';
                windowEle.style.left = ev.clientX - disX + 'px';
            }
            document.onmouseup = function () {
                document.onmousemove = null;
                if (windowEle.releaseCapture) {
                    windowEle.releaseCapture()
                }
            }
            return false;
        });
    },
    //接口
    OpenWindow: function () {
        document.getElementById(this.winID).style.display = "block";
    },
    CloseWindow: function () {
        $("#" + this.winID).remove();
    }
}
