//����¼�
function Event() {
}
Event.prototype = {
    //����Ҽ��¼�
    MouseRightClick: function (menuEle, responseEle) {
        responseEle.oncontextmenu = function (e) {
            currClickEleId = e.srcElement.id;           //ȫ�ֱ���
            currClickEleClass = e.srcElement.className; //ȫ�ֱ���

            menuEle.style.left = e.clientX - 32 + "px"; // ƫ�� 32px
            menuEle.style.top = e.clientY + "px";
            menuEle.style.display = "block";

            return false; // ��ֹ��������Ҽ���Ӧ
        }
        responseEle.onclick = function () {
            menuEle.style.display = "none";
        }

    },
    //����Ҽ��˵���Ӧ
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