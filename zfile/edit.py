# import pandas as pd
# import io

# # 读取Markdown文件内容
# with open('/Users/xhl/note-book/AmericaDream/MiddleEnglishWord.md', 'r', encoding='utf-8') as file:
#     md_content = file.read()

# # 在Markdown文件中找到表格的起始位置和结束位置
# start = md_content.find('|')  # 找到第一个表格的起始位置
# end = md_content.find('\n\n')  # 找到第一个表格的结束位置

# # 提取表格数据
# table = md_content[start:end]
# df = pd.read_csv(io.StringIO(table), sep="|")

# # df = pd.read_csv(pd.compat.StringIO(table), sep="|")

# # 获取第一列数据
# first_column = df.iloc[:, 1]  # 获取第一列，注意索引从0开始，这里选择第二列的数据

# print("第一列数据：")
# print(first_column)


# # 打开Markdown文件


def extract_content(text):
    start = text.find('|')  # 找到第一个 '|'
    if start != -1:
        end = text.find('|', start + 1)  # 找到第二个 '|'
        if end != -1:
            content = text[start + 1: end].strip()  # 提取两个 '|' 之间的内容并去除首尾空格
            return content

def get_first_word(text):
    words = text.split()  # 使用 split() 方法根据空格分割字符串
    if len(words) > 0:
        return words[0]  # 返回第一个单词
    else:
        return None  # 如果输入为空串，则返回 None

with open('/Users/xhl/note-book/AmericaDream/MiddleEnglishWord.md', 'r', encoding='utf-8') as file:
    # 逐行读取文件内容
    for line in file:
        res1 = extract_content(line)
        if res1 != None:
            with open('../zfile/a.txt', 'a') as file:  # 以追加模式打开文件
                res = get_first_word(res1)
                if res != None:
                    res = res.lower()
                    re = f"insert into  words(word, master_level) values('{res}',null);"
                # print(re)
                    if re != None:
                        file.write(re + "\n")
            
        # 检查当前行是否包含 "*"
        # if '*' in line:
        #     print(line.strip())  # 打印包含 "*" 的行并去除首尾空格