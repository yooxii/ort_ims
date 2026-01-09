import os
import zipfile


def zip_folder(directory, zipname):
    """
    压缩文件夹, zip格式

    :param directory: 待压缩文件夹
    :param zipname: 生成压缩包的名称
    """
    with zipfile.ZipFile(f"{zipname}.zip", "w", zipfile.ZIP_LZMA) as HarZip:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if not file.endswith("txt"):
                    continue
                file_path = os.path.join(root, file)
                # 防止路径遍历攻击 - 规范化路径并验证
                abs_file_path = os.path.abspath(file_path)
                abs_directory = os.path.abspath(directory)

                # 确保文件路径在目标目录下
                if not abs_file_path.startswith(abs_directory + os.sep):
                    print(f"警告: 跳过路径遍历尝试: {file_path}")
                    continue

                arcname = os.path.relpath(abs_file_path, abs_directory)
                HarZip.write(abs_file_path, arcname=arcname)
