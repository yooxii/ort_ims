/* global $ */

function hideMenu() {
    // 隐藏自定义右键菜单
    $("#rclick-menu").hide();
    $("#rclick-th-menu").hide();
}
$(document).on("contextmenu", "#datas_table thead th", function (event) {
    event.preventDefault();

    hideMenu();

    $("#rclick-th-menu").css({
        top: event.clientY,
        left: event.clientX
    }).show();
});

$(document).on("click", function () {
    hideMenu();
});

$(document).on("click", "#delete_data", function (event) {
    hideMenu();
    if (!confirm("确认删除吗？")) {
        event.preventDefault();
    }
});