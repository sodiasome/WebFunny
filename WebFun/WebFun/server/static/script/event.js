//鼠标事件
function Event() {
}
Event.prototype = {
    //鼠标右键事件
    MouseRightClick: function (menuEle, responseEle) {
        responseEle.oncontextmenu = function (e) {
            currClickEleId = e.srcElement.id;           //全局变量
            currClickEleClass = e.srcElement.className; //全局变量

            menuEle.style.left = e.clientX - 32 + "px"; // 偏移 32px
            menuEle.style.top = e.clientY + "px";
            menuEle.style.display = "block";

            return false; // 禁止浏览器的右键响应
        }
        responseEle.onclick = function () {
            menuEle.style.display = "none";
        }

    },
    //鼠标右键菜单响应
    OnRightMenu: function () {
        document.getElementById("menu_1").onclick = function () {
            alert("menu_1");
        }
        document.getElementById("menu_2").onclick = function () {
            alert("menu_2");
        }
        document.getElementById("menu_3").onclick = function () {
            alert("menu_3");
        }
    },
}
g_event = new Event();