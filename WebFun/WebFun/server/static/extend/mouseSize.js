(function ($) {
    $.fn.dragDiv = function (options) {
        var def = {
            maxW:600,// 可伸缩的最大宽度
            minW:50// 可伸缩的最小宽度
        };// 参数默认值
        var opts = $.extend(def,options);// 扩展参数，使用默认值或传参
        //设置最大/最小宽度
        var max_width = opts.maxW,
            min_width = opts.minW;
 
        //记录鼠标相对left盒子x轴位置
        var mouse_x = 0;
        var left = $(this).parent('div')[0];
 
        //鼠标移动事件
        function mouseMove(e) {
            var e = e || window.event;
            var left_width = e.clientX - mouse_x;// 可伸缩div的宽度
            left_width = left_width < min_width ? min_width : left_width;
            left_width = left_width > max_width ? max_width : left_width;
            left.style.width = left_width + "px";
        }
        //终止事件
        function mouseUp() {
            document.onmousemove = null;
            document.onmouseup = null;
        }
        $(this).mousedown(function (e) {
            var e = e || window.event;
            //阻止默认事件
            e.preventDefault();
            mouse_x = e.clientX - left.offsetWidth;// 可伸缩div距离左侧边界的宽度
            document.onmousemove = function () {
                mouseMove()
            };
            document.onmouseup = function () {
                mouseUp()
            };
        })
    }
})(jQuery);