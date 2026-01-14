import sys
from pathlib import Path

libs_path = Path(__file__).resolve()
base_path = Path(__file__).parent.parent.resolve()

# 转换为字符串并确保是绝对路径
libs_path_str = str(libs_path)
base_path_str = str(base_path)

# 只有当路径不存在于sys.path中时才添加
if libs_path_str not in sys.path:
    sys.path.insert(0, libs_path_str)
if base_path_str not in sys.path:
    sys.path.insert(0, base_path_str)

