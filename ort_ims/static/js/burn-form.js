document.addEventListener('DOMContentLoaded', function() {
    // 从全局引入 Vue
    const { createApp, reactive, watch } = Vue;

    const app = createApp({
        setup() {
            const testHeaders = [
                { name: '机种名称', id: 'partno', type: 'text' },
                { name: '测试人员', id: 'technician', type: 'text' },
                { name: '测试开始时间', id: 'startdate', type: 'date' },
                { name: '测试结束时间', id: 'enddate', type: 'date' },
                { name: '单体数量', id: 'qty', type: 'number' }
            ];

            const roominfo = [
                { name: 'Room', id: 'BI_Room_No', type: 'text', class: "col-1" },
                { name: 'Area', id: 'BI_Area', type: 'text', class: "col-1" },
                { name: 'Place', id: 'BI_Place', type: 'text', class: "col-1" },
            ];
            const uutinfo = [
                { name: '版本', id: 'Rev', type: 'text', class: "col-1" },
                { name: '周期', id: 'DC', type: 'week', class: "col-1" },
                { name: '序列号', id: 'SN', type: 'text', class: "col-md-3  px-lg-2" },
                { name: '工令', id: 'WorkOrder', type: 'text', class: "col-md-2" },
            ];
            const pretest = [
                { name: '外观(前)', id: 'PRE_VisualInspection', type: 'select', selects: ["OK", "NO"], class: "col-1" },
                { name: '功能', id: 'PRE_FunctionCheck', type: 'select', selects: ["Pass", "Fail"], class: "col-1" }
            ];
            const posttest = [
                { name: '外观(后)', id: 'POST_VisualInspection', type: 'select', selects: ["OK", "NO"], class: "col-1" },
                { name: '功能', id: 'POST_FunctionCheck', type: 'select', selects: ["Pass", "Fail"], class: "col-1" },
                { name: 'Hi-Pot', id: 'POST_Hi_Pot', type: 'select', selects: ["OK", "NO"], class: "col-1" },
            ];

            // 合并所有测试结果字段
            const testResults = [...roominfo, ...uutinfo, ...pretest, ...posttest];

            const headerData = reactive({
                partno: '',
                technician: '',
                startdate: '',
                enddate: '',
                qty: 3 // 默认单体数量为 3
            });

            // 存储全局默认值
            const defaultValues = reactive({});

            // 初始化默认值对象
            testResults.forEach(item => {
                defaultValues[item.id] = item.type === 'select' ? item.selects[0] : ''; // select 默认选中第一个选项
            });

            // 为每一行维护独立的数据对象
            const rowDataList = reactive([]);

            // 初始化 rowDataList
            const initializeRows = () => {
                rowDataList.length = 0; // 清空现有数据
                for (let i = 0; i < headerData.qty; i++) {
                    const row = {};
                    testResults.forEach(item => {
                        row[item.id] = defaultValues[item.id]; // 使用全局默认值填充
                    });
                    rowDataList.push(row);
                }
            };

            // 监听 qty 变化，重新初始化行数据
            watch(
                () => headerData.qty,
                () => {
                    initializeRows();
                }
            );

            // 初始化一次
            initializeRows();

            // 监听输入完成事件（失去焦点时触发）
            const handleInputComplete = (fieldId, rowIndex, value) => {
                // 如果当前字段之前为空，则更新全局默认值
                if (!defaultValues[fieldId]) {
                    defaultValues[fieldId] = value;
                    // 将新默认值填充到后续行
                    for (let i = rowIndex + 1; i < rowDataList.length; i++) {
                        if (!rowDataList[i][fieldId]) {
                            rowDataList[i][fieldId] = value;
                        }
                    }
                }
                // 更新当前行的值
                rowDataList[rowIndex][fieldId] = value;
            };

            // 处理粘贴多行数据
            const handlePaste = (event) => {
                event.preventDefault(); // 阻止默认粘贴行为
                const pasteData = (event.clipboardData || window.clipboardData).getData('text'); // 获取粘贴的数据
                const rows = pasteData.split('\n'); // 按行分割
                
                // 计算需要多少行
                const neededRows = Math.max(rows.length, headerData.qty);
                
                // 如果粘贴的数据行数超过当前设置的行数，更新行数
                if(neededRows > headerData.qty) {
                    headerData.qty = neededRows;
                    // 重新初始化以适应新行数
                    setTimeout(() => {
                        // 解析每行数据并填入表格
                        for (let i = 0; i < Math.min(rows.length, rowDataList.length); i++) {
                            if (rows[i].trim() !== '') {
                                const columns = rows[i].split('\t'); // 按制表符分割列
                                
                                // 为当前行分配数据
                                testResults.forEach((field, j) => {
                                    if (columns[j] !== undefined) {
                                        rowDataList[i][field.id] = columns[j].trim();
                                        
                                        // 如果是第一次粘贴此字段，则更新默认值
                                        if (!defaultValues[field.id]) {
                                            defaultValues[field.id] = columns[j].trim();
                                        }
                                    }
                                });
                            }
                        }
                    }, 0);
                } else {
                    // 解析每行数据并填入表格
                    for (let i = 0; i < Math.min(rows.length, rowDataList.length); i++) {
                        if (rows[i].trim() !== '') {
                            const columns = rows[i].split('\t'); // 按制表符分割列
                            
                            // 为当前行分配数据
                            testResults.forEach((field, j) => {
                                if (columns[j] !== undefined) {
                                    rowDataList[i][field.id] = columns[j].trim();
                                    
                                    // 如果是第一次粘贴此字段，则更新默认值
                                    if (!defaultValues[field.id]) {
                                        defaultValues[field.id] = columns[j].trim();
                                    }
                                }
                            });
                        }
                    }
                }
            };

            return {
                testHeaders,
                headerData,
                roominfo,
                uutinfo,
                pretest,
                posttest,
                rowDataList,
                handleInputComplete,
                handlePaste
            };
        }
    });
    
    // 检查是否存在挂载点，然后挂载应用
    const mountElement = document.getElementById('burn-app');
    if(mountElement) {
        app.mount('#burn-app');
    }
});