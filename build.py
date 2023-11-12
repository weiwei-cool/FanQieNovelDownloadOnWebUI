import os
import shutil

# 运行 'cnpm run build' 命令
os.system('cnpm run build')

# 删除指定目录下的文件
directory_path = 'D:\\bc\\python\\FanQieNovelDownloadOnWeb\\assets'
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Failed to delete file {file_path}: {str(e)}")

# 复制文件到其他目录
source_assets_directory = './dist/assets'
destination_assets_directory = 'D:\\bc\\python\\FanQieNovelDownloadOnWeb\\assets'
for filename in os.listdir(source_assets_directory):
    source_file_path = os.path.join(source_assets_directory, filename)
    if os.path.isfile(source_file_path):
        try:
            shutil.copy2(source_file_path, os.path.join(destination_assets_directory, filename))
            print(f"Copy file: {source_file_path}")
        except Exception as e:
            print(f"Failed to copy file {source_file_path}: {str(e)}")

source_history_directory = './dist/history'
destination_history_directory = 'D:\\bc\\python\\FanQieNovelDownloadOnWeb\\templates\\history'
for filename in os.listdir(source_history_directory):
    source_file_path = os.path.join(source_history_directory, filename)
    if os.path.isfile(source_file_path):
        try:
            shutil.copy2(source_file_path, os.path.join(destination_history_directory, filename))
            print(f"Copy file: {source_file_path}")
        except Exception as e:
            print(f"Failed to copy file {source_file_path}: {str(e)}")

# 复制HTML文件到其他目录
shutil.copy2('D:\\bc\\html\\DownloadFanqiePassageInWeb\\dist\\index.html',
            'D:\\bc\\python\\FanQieNovelDownloadOnWeb\\templates')

