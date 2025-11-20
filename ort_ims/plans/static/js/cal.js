
// 获取年月日和星期几
let date = new Date();
let Y = date.getFullYear();
let M = date.getMonth();
let isSelect = true;    //true为选择了月，false为选择了年（添加文本阴影）

// 更新当前年
let yearNow = document.getElementById("year");
yearNow.innerHTML = Y;
// 更新当前月
let monthNow = document.getElementById("month");
monthNow.innerHTML = monthAndMaxDay(Y, M)[0];
// 判断选中年还是月（添加文本阴影）
selected(isSelect);
//更新当前日
let days = document.getElementById("day");
updateAllDays(Y, M);

// 选择按月切换还是按年切换
yearNow.addEventListener("click", function () {
    isSelect = false
    selected(isSelect);
});
monthNow.addEventListener("click", function () {
    isSelect = true;
    selected(isSelect);
});

// 左右切换日期
let previous = document.getElementById("pre-month");
previous.addEventListener("click", function () { changePage(true); });
let next = document.getElementById("next-month");
next.addEventListener("click", function () { changePage(false); });

// 按日查询对应的星期几
function dayToStar(year, month, day) {
    let theDate = new Date(year, month, day);
    return theDate.getDay();
}

// 查询一个月对应的英文命名和最大天数
function monthAndMaxDay(year, month) {
    let month_now = "";
    let maxDay = 0;     // 一个月的最大天数
    switch (month + 1) {
        case 1: month_now = "一月"; maxDay = 31; break;
        case 2:
            month_now = "二月";
            if (year % 4 == 0) {
                maxDay = 29;
            } else {
                maxDay = 28;
            }
            break;
        case 3: month_now = "三月"; maxDay = 31; break;
        case 4: month_now = "四月"; maxDay = 30; break;
        case 5: month_now = "五月"; maxDay = 31; break;
        case 6: month_now = "六月"; maxDay = 30; break;
        case 7: month_now = "七月"; maxDay = 31; break;
        case 8: month_now = "八月"; maxDay = 31; break;
        case 9: month_now = "九月"; maxDay = 30; break;
        case 10: month_now = "十月"; maxDay = 31; break;
        case 11: month_now = "十一月"; maxDay = 30; break;
        case 12: month_now = "十二月"; maxDay = 31; break;
        default: month = "";
    }
    return [month_now, maxDay];
}

// 更新当前月的所有天数
function updateAllDays(year, month) {
    let offset = dayToStar(year, month, 1);
    let maxDay = monthAndMaxDay(year, month)[1];

    // 实现日期和星期对应
    for (let i = 0; i < offset; i++) {
        let day = document.createElement("li");
        day.className = "no-style";
        days.appendChild(day);
    }

    for (let i = 1; i <= maxDay; i++) {
        let day = document.createElement("li");
        let dateNow = new Date();
        // 当前日期有绿色背景
        if (year == dateNow.getFullYear() && month == dateNow.getMonth() && i == dateNow.getDate()) {
            day.className = "style-default bg-style"
        } else {
            day.className = "style-default";
        }
        day.id = i;
        day.innerText = i
        days.appendChild(day);
    }
}

// 选择按月切换还是按年切换
function selected(boolean) {
    if (boolean) {
        monthNow.style.textShadow = "2px 2px 2px rgb(121, 121, 121)";
        yearNow.style.textShadow = "none";
    } else {
        monthNow.style.textShadow = "none";
        yearNow.style.textShadow = "2px 2px 2px rgb(121, 121, 121)";
    }
}

// 点击切换事件
function changePage(boolean) {
    // 按年切换还是按月切换
    if (isSelect) {
        // 向前切换还是向后切换
        if (boolean) {
            M = M - 1;
            if (M == -1) {
                Y--;
                M = 11;
            }
        } else {
            M = M + 1;
            if (M == 11) {
                Y++;
                M = 0;
            }
        }
    } else {
        if (boolean) {
            Y--;
        } else {
            Y++;
        }
    }
    yearNow.innerHTML = Y;
    monthNow.innerHTML = monthAndMaxDay(Y, M)[0];
    // 清空一个月所有天数
    days.innerHTML = "";
    // 重新添加一个月所有天数
    updateAllDays(Y, M);
}