from bs4 import BeautifulSoup

# 将HTML内容存储在一个字符串中
html = """
<span class="info">Comments:</span> 29
"""

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html, 'html.parser')

# 找到包含"Comments:"的<span>元素
comments_span = soup.find('span', class_='info', string='Comments:')
if comments_span:
    # 获取<span>元素的下一个兄弟元素，即包含数字的文本节点
    comments_text = comments_span.find_next_sibling(string=True)
    # 提取文本节点的内容（即数字部分）
    comments = comments_text.strip()
    print(f"评论数量: {comments}")
else:
    print("未找到评论数量信息")
