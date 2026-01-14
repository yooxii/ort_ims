import os
import zipfile
from pathlib import Path


def zip_folder(directory: Path, zipname):
    """
    压缩文件夹, zip格式

    :param directory: 待压缩文件夹
    :param zipname: 生成压缩包的名称
    """
    with zipfile.ZipFile(f"{zipname}.zip", "w", zipfile.ZIP_LZMA) as harzip:
        for root, _dirs, files in os.walk(directory):
            for file in files:
                if not file.endswith("txt"):
                    continue
                file_path = Path(root) / Path(file)
                # 防止路径遍历攻击 - 规范化路径并验证
                abs_file_path = file_path.resolve()
                abs_directory = directory.resolve()

                # 确保文件路径在目标目录下
                if not str(abs_file_path).startswith(str(abs_directory) + os.sep):
                    print(f"警告: 跳过路径遍历尝试: {file_path}")
                    continue

                arcname = str(abs_file_path.relative_to(abs_directory))
                harzip.write(abs_file_path, arcname=arcname)
