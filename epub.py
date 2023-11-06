#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/31 15:01:58
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''

from json.tool import main
import epubs
import pandas as pd
import re
import warnings
import configparser
import mysql.connector

warnings.filterwarnings("ignore")

def contains_num(s):
    return bool(re.search(r'\d', s))


def read_epub(file,word_map):
    book_total_word = {}
    not_in_db_word = {}
    text = epubs.to_text(file)
    for i in str(text).split():
        res = clean_str(i)
        if res != None:
            res = res.lower()
            # 处理英语中所写的问题
            res = re.sub(r"(’s|’t|’re|’ve|’d|’ll|’m|n’t)","",res)
            if res != None and not contains_num(res) and len(res) != 1:
                book_total_word[res] = book_total_word.get(res, 0) + 1
                if res not in word_map :
                    not_in_db_word[res] = not_in_db_word.get(res, 0) + 1

    book_total_word = dict(sorted(book_total_word.items(), key=lambda item: item[1], reverse=True)) # Ture表示倒序排列
    not_in_db_word = dict(sorted(not_in_db_word.items(), key=lambda item: item[1], reverse=True)) # Ture表示倒序排列

    # 将不认识的单词处输出到文件中
    with open('./output/unknow_words.txt', 'w') as file:  # 覆盖写入
        for word, count in not_in_db_word.items():
            file.write(f"{word}: {count}" + "\n")

    return book_total_word,not_in_db_word

def clean_str(input_str):
    # 定义一个正则表达式，匹配所有的数字
    pattern = r"[.|'|,|:|/|©|“|_|(|)|*|\]|\[|#|!|?|\”|;|@]"
       
    # 使用 re.sub() 
    res = re.sub(pattern, '', input_str)
    if res != '':
        return res

def get_mysql_conn():

    # 创建一个ConfigParser对象
    config = configparser.ConfigParser()
    # 读取INI文件
    config.read('./conf/db.ini')
    # 获取特定键的值
    word_host = config.get('word_conf', 'word_host')
    word_port = int(config.get('word_conf', 'word_port'))
    word_user = config.get('word_conf', 'word_user')
    word_pwd = config.get('word_conf', 'word_pwd')
    
    return mysql.connector.connect(host=word_host,
                                port=word_port, 
                                user=word_user,
                                password = word_pwd,
                                database='dataease'
                                )

def map_builder(conn):
    word_map = {}

    # 从数据库中读取数据
    cursor = conn.cursor()
    query = "select word from words"
    cursor.execute(query)

    # 获取数据并构建map结构
    for word in cursor:
        # print(word)
        word = word[0].lower()
        word_map[word] = True

        # 关闭连接
    cursor.close()
    conn.close()
    return word_map


def init_dictionary():
    dictionary = pd.read_csv(
        './input/英汉大词典_del_ipa_edited.txt', sep='⬄', header=0,engine='python',
        names=['word', 'interpretation'])

    def check(series):
        return series['word'].strip()

    dictionary['word'] = dictionary.apply(check, axis=1)
    dictionary.set_index('word', inplace=True)
    return dictionary

def get_translate(dictionary, word):
    if word in dictionary.index.values:
        return dictionary.loc[word].values.tolist()[0]
    else:
        return None


def trans_unknow_words(not_in_db_word,dictionary):

    with open('./output/unknow_words_trans.txt', 'w') as file:  # 覆盖写入
        for word in not_in_db_word.keys():
            chinese = get_translate(dictionary,word)
            # if (chinese) != None:
            #     print(f"{word}" + "\n" + f"{chinese}" + "\n\n")
            if (chinese) != None:
                file.write(f"{word}" + "\n" + f"{chinese}" + "\n\n")


if __name__ == '__main__':

    # 获取 MySQL连接
    conn = get_mysql_conn()    
    
    # 将自建单词库存储在内存中 
    word_map = map_builder(conn)
    
    epub_file = '/Users/xhl/Documents/books/Clear Thinking.epub'
    # epub_file = '/Users/xhl/Documents/books/chip war.epub'
    
    # 扫描 epub文件，返回全部单词列表，和不认识的单词列表
    book_total_word,not_in_db_word = read_epub(epub_file,word_map)


    # init the local dictionary into memroy
    dictionary = init_dictionary()

    trans_unknow_words(not_in_db_word,dictionary)
 
    print("不在自建词汇库中的单词数为：", len(not_in_db_word.keys()))
    print("当前电子书单词总数为：", len(book_total_word.keys()))
    