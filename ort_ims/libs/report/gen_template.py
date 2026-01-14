import os
import openpyxl
            

def copy_sheet(excel, source_file: str, sheet_names: list[str] | str, target_file: str):
    """
    将 source_file 中指定名称的工作表完整复制到 target_file 中。

    Args:
        excel (): Excel 对象
        source_file (str): 源 Excel 文件路径（必须存在）
        sheet_names (list[str] | str): 指定的工作表名称
        target_file (str): 目标 Excel 文件路径（必须存在）
    """
    # 检查表格名称
    if isinstance(sheet_names, list):
        if len(sheet_names) == 0:
            return
    elif isinstance(sheet_names, str):
        if sheet_names == "*":
            sheet_names = [sheet.Name for sheet in source_wb.Worksheets]
        else:
            sheet_names = [sheet_names]
    else:
        raise ValueError("sheet_names 参数类型错误")

    # 检查文件是否存在
    if not os.path.exists(source_file):
        raise FileNotFoundError(f"源文件不存在: {source_file}")
    if not os.path.exists(target_file):
        raise FileNotFoundError(f"目标文件不存在: {target_file}")

    try:
        # 打开源工作簿和目标工作簿
        source_wb = excel.Workbooks.Open(os.path.abspath(source_file))
        target_wb = excel.Workbooks.Open(os.path.abspath(target_file))

        sheet_names.reverse()
        for sheet_name in sheet_names:
            # 检查源工作表是否存在
            sheet_names = [s.Name for s in source_wb.Sheets]
            if sheet_name not in sheet_names:
                raise ValueError(f"源文件中不存在工作表: {sheet_name}")

            # 可选：如果目标文件中已有同名工作表，先删除（避免重命名）
            try:
                target_wb.Sheets(sheet_name).Delete()
            except:
                pass  # 不存在则忽略

            # 复制工作表到目标工作簿的最前面
            source_sheet = source_wb.Sheets(sheet_name)
            source_sheet.Copy(Before=target_wb.Sheets(2))

            print(f"✅ 工作表 '{sheet_name}' 已成功复制到 {target_file}")

        # 保存目标工作簿
        target_wb.Save()

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        raise

    finally:
        # 关闭工作簿（不保存源文件）
        if "source_wb" in locals():
            source_wb.Close(SaveChanges=False)
        if "target_wb" in locals():
            target_wb.Close(SaveChanges=False)