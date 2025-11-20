(function ($) {
    'use strict';

    // 表格列宽调整插件
    $.fn.resizableTable = function (options) {
        var settings = $.extend({
            resizable: true,
            minWidth: 50,
            saveToLocalStorage: true
        }, options);

        return this.each(function () {
            var $table = $(this);
            var tableId = $table.attr('id') || 'resizable-table';
            var isResizing = false;
            var $currentTh = null;
            var startX = 0;
            var startWidth = 0;

            // 初始化
            function init() {
                // 设置表格样式
                $table.addClass('resizable-table');

                // 为每个表头添加调整手柄
                $table.find('thead th').each(function () {
                    var $th = $(this);
                    var $handle = $('<div class="resize-handle"></div>');
                    $th.append($handle);
                    $th.css('position', 'relative');
                });

                // 绑定事件
                bindEvents();

                // 如果启用了本地存储，加载保存的列宽
                if (settings.saveToLocalStorage) {
                    loadColumnWidths(tableId);
                }

                // 如果没有保存的宽度，则根据内容自动调整
                setTimeout(function () {
                    if (!hasSavedWidths(tableId)) {
                        adjustToContent();
                    }
                }, 100);
            }

            // 检查是否有保存的宽度
            function hasSavedWidths(tableId) {
                try {
                    return localStorage.getItem('table-widths-' + tableId) !== null;
                } catch (e) {
                    return false;
                }
            }

            // 根据内容自动调整列宽
            function adjustToContent() {
                // 获取每列的最大内容宽度
                var columnWidths = [];
                var columnCount = $table.find('thead th').length;

                // 初始化列宽数组
                for (var i = 0; i < columnCount; i++) {
                    columnWidths[i] = settings.minWidth;
                }

                // 遍历表头，获取标题宽度
                $table.find('thead th').each(function (index) {
                    var $th = $(this);
                    var textWidth = getTextWidth($th.text(), $th);
                    columnWidths[index] = Math.max(columnWidths[index], textWidth + 30); // 添加一些内边距
                });

                // 遍历表体，获取内容宽度
                $table.find('tbody tr').each(function () {
                    $(this).find('td').each(function (index) {
                        var $td = $(this);
                        // 特殊处理包含换行的内容
                        var content = $td.text();
                        var textWidth = getTextWidth(content, $td);
                        columnWidths[index] = Math.max(columnWidths[index], textWidth + 30);
                    });
                });

                // 应用计算出的宽度
                $table.find('thead th').each(function (index) {
                    $(this).css('width', columnWidths[index] + 'px');
                });

                $table.find('tbody tr').first().find('td').each(function (index) {
                    $(this).css('width', columnWidths[index] + 'px');
                });
            }

            // 获取文本宽度
            function getTextWidth(text, $element) {
                var $temp = $('<span></span>')
                    .text(text)
                    .css({
                        'font-family': $element.css('font-family'),
                        'font-size': $element.css('font-size'),
                        'font-weight': $element.css('font-weight'),
                        'visibility': 'hidden',
                        'position': 'absolute',
                        'white-space': 'nowrap'
                    })
                    .appendTo('body');

                var width = $temp.width();
                $temp.remove();
                return width;
            }

            // 绑定事件
            function bindEvents() {
                // 鼠标按下事件 - 开始调整
                $table.on('mousedown', '.resize-handle', function (e) {
                    if (!settings.resizable) return;

                    isResizing = true;
                    $currentTh = $(this).parent();
                    startX = e.pageX;
                    startWidth = $currentTh.width();

                    // 添加调整中的样式
                    $('body').addClass('resizing');
                    e.preventDefault();
                    e.stopPropagation();
                });

                // 鼠标移动事件 - 调整列宽
                $(document).on('mousemove', function (e) {
                    if (!isResizing) return;

                    var newWidth = startWidth + (e.pageX - startX);
                    newWidth = Math.max(settings.minWidth, newWidth);

                    if ($currentTh) {
                        $currentTh.css('width', newWidth + 'px');

                        // 同步调整表头对应的所有单元格
                        var index = $currentTh.index();
                        $table.find('tbody tr').each(function () {
                            $(this).find('td').eq(index).css('width', newWidth + 'px');
                        });
                    }
                });

                // 鼠标释放事件 - 结束调整
                $(document).on('mouseup', function () {
                    if (!isResizing) return;

                    isResizing = false;
                    $('body').removeClass('resizing');
                    $currentTh = null;

                    // 如果启用了本地存储，保存列宽
                    if (settings.saveToLocalStorage) {
                        saveColumnWidths(tableId);
                    }
                });
            }

            // 保存列宽到本地存储
            function saveColumnWidths(tableId) {
                var widths = [];
                $table.find('thead th').each(function () {
                    widths.push($(this).width());
                });

                try {
                    localStorage.setItem('table-widths-' + tableId, JSON.stringify(widths));
                } catch (e) {
                    console.warn('无法保存表格列宽到本地存储:', e);
                }
            }

            // 从本地存储加载列宽
            function loadColumnWidths(tableId) {
                try {
                    var widthsStr = localStorage.getItem('table-widths-' + tableId);
                    if (widthsStr) {
                        var widths = JSON.parse(widthsStr);
                        $table.find('thead th').each(function (index) {
                            if (widths[index]) {
                                $(this).css('width', widths[index] + 'px');
                                var $th = $(this);
                                var index = $th.index();
                                $table.find('tbody tr').each(function () {
                                    $(this).find('td').eq(index).css('width', widths[index] + 'px');
                                });
                            }
                        });
                    }
                } catch (e) {
                    console.warn('无法从本地存储加载表格列宽:', e);
                }
            }

            // 初始化插件
            init();
        });
    };

})(jQuery);
(function ($) {
    'use strict';

    // 表格列宽调整插件
    $.fn.resizableTable = function (options) {
        var settings = $.extend({
            resizable: true,
            minWidth: 50,
            saveToLocalStorage: true
        }, options);

        return this.each(function () {
            var $table = $(this);
            var tableId = $table.attr('id') || 'resizable-table';
            var isResizing = false;
            var $currentTh = null;
            var startX = 0;
            var startWidth = 0;

            // 初始化
            function init() {
                // 设置表格样式
                $table.addClass('resizable-table');

                // 为每个表头添加调整手柄
                $table.find('thead th').each(function () {
                    var $th = $(this);
                    var $handle = $('<div class="resize-handle"></div>');
                    $th.append($handle);
                    $th.css('position', 'relative');
                });

                // 绑定事件
                bindEvents();

                // 如果启用了本地存储，加载保存的列宽
                if (settings.saveToLocalStorage) {
                    loadColumnWidths(tableId);
                }

                // 如果没有保存的宽度，则根据内容自动调整
                setTimeout(function () {
                    if (!hasSavedWidths(tableId)) {
                        adjustToContent();
                    }
                }, 100);
            }

            // 检查是否有保存的宽度
            function hasSavedWidths(tableId) {
                try {
                    return localStorage.getItem('table-widths-' + tableId) !== null;
                } catch (e) {
                    return false;
                }
            }

            // 根据内容自动调整列宽
            function adjustToContent() {
                // 获取每列的最大内容宽度
                var columnWidths = [];
                var columnCount = $table.find('thead th').length;

                // 初始化列宽数组
                for (var i = 0; i < columnCount; i++) {
                    columnWidths[i] = settings.minWidth;
                }

                // 遍历表头，获取标题宽度
                $table.find('thead th').each(function (index) {
                    var $th = $(this);
                    var textWidth = getTextWidth($th.text(), $th);
                    columnWidths[index] = Math.max(columnWidths[index], textWidth + 20); // 添加一些内边距
                });

                // 遍历表体，获取内容宽度
                $table.find('tbody tr').each(function () {
                    $(this).find('td').each(function (index) {
                        var $td = $(this);
                        // 特殊处理包含换行的内容
                        var content = $td.text();
                        var textWidth = getTextWidth(content, $td);
                        columnWidths[index] = Math.max(columnWidths[index], textWidth + 20);
                    });
                });

                // 应用计算出的宽度
                $table.find('thead th, tbody tr td').each(function () {
                    var index = $(this).index();
                    $(this).css('width', columnWidths[index] + 'px');
                });
            }

            // 获取文本宽度
            function getTextWidth(text, $element) {
                var $temp = $('<span></span>')
                    .text(text)
                    .css({
                        'font-family': $element.css('font-family'),
                        'font-size': $element.css('font-size'),
                        'font-weight': $element.css('font-weight'),
                        'visibility': 'hidden',
                        'position': 'absolute',
                        'white-space': 'nowrap'
                    })
                    .appendTo('body');

                var width = $temp.width();
                $temp.remove();
                return width;
            }

            // 绑定事件
            function bindEvents() {
                // 鼠标按下事件 - 开始调整
                $table.on('mousedown', '.resize-handle', function (e) {
                    if (!settings.resizable) return;

                    isResizing = true;
                    $currentTh = $(this).parent();
                    startX = e.pageX;
                    startWidth = $currentTh.width();

                    // 添加调整中的样式
                    $('body').addClass('resizing');
                    e.preventDefault();
                });

                // 鼠标移动事件 - 调整列宽
                $(document).on('mousemove', function (e) {
                    if (!isResizing) return;

                    var newWidth = startWidth + (e.pageX - startX);
                    newWidth = Math.max(settings.minWidth, newWidth);

                    // 设置当前列的宽度
                    $currentTh.css('width', newWidth + 'px');

                    // 创建临时样式元素来同步所有行的对应列宽度
                    var index = $currentTh.index();
                    var style = $('<style type="text/css">');
                    style.text('table tr td:nth-child(' + (index + 1) + ') { width: ' + newWidth + 'px !important; }');
                    $('head').append(style);

                    // 移除旧的样式
                    if ($table.data('resizer-style')) {
                        $table.data('resizer-style').remove();
                    }
                    $table.data('resizer-style', style);
                });

                // 鼠标释放事件 - 结束调整
                $(document).on('mouseup', function () {
                    if (!isResizing) return;

                    isResizing = false;
                    $('body').removeClass('resizing');

                    // 清除临时样式
                    if ($table.data('resizer-style')) {
                        $table.data('resizer-style').remove();
                        $table.removeData('resizer-style');
                    }

                    // 如果启用了本地存储，保存列宽
                    if (settings.saveToLocalStorage) {
                        saveColumnWidths(tableId);
                    }
                });
            }

            // 保存列宽到本地存储
            function saveColumnWidths(tableId) {
                var widths = [];
                $table.find('thead th').each(function () {
                    widths.push($(this).width());
                });

                try {
                    localStorage.setItem('table-widths-' + tableId, JSON.stringify(widths));
                } catch (e) {
                    console.warn('无法保存表格列宽到本地存储:', e);
                }
            }

            // 从本地存储加载列宽
            function loadColumnWidths(tableId) {
                try {
                    var widthsStr = localStorage.getItem('table-widths-' + tableId);
                    if (widthsStr) {
                        var widths = JSON.parse(widthsStr);
                        $table.find('thead th').each(function (index) {
                            if (widths[index]) {
                                $(this).css('width', widths[index] + 'px');
                                var $th = $(this);
                                var index = $th.index();
                                $table.find('tbody tr').each(function () {
                                    $(this).find('td').eq(index).css('width', widths[index] + 'px');
                                });
                            }
                        });
                    }
                } catch (e) {
                    console.warn('无法从本地存储加载表格列宽:', e);
                }
            }

            // 初始化插件
            init();
        });
    };

})(jQuery);