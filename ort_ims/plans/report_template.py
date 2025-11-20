# \\bnt56\品保部\ORT實驗資料\13. 臨時試驗報告\BI EMI\2025 EMI & 168H 完成

import openpyxl as xl
import os

wb = xl.load_workbook("D:\\Desktop_Li\\2025.成品領用記錄.xlsx", rich_text=True)
ws = wb["七月領用"]

cell = ws.cell(row=25,column=6)

print(cell.value)
print(cell.font.name)
print(cell.font.size)
print(cell.font.color.rgb)








