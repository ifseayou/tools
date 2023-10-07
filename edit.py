import os

# 指定目标目录
target_directory = '~/work/edw_code_prd/ods/x'

# 将波浪号（~）扩展为用户的家目录
expanded_directory = os.path.expanduser(target_directory)

# 检查目录是否存在
if not os.path.exists(expanded_directory):
    # 如果目录不存在，创建它
    os.makedirs(expanded_directory)
    print(f'已创建目录：{expanded_directory}')
else:
    print(f'目录已存在：{expanded_directory}')
