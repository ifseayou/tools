from json.tool import main
import requests
from bs4 import BeautifulSoup

# 发送HTTP GET请求获取Bilibili首页的HTML内容
url = "https://www.xxxx.com/index.php"

# 尝试设置User-Agent标头，以使请求看起来更像是来自普通的浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

response = requests.get(url, headers=headers)

# 初始化列表来存储提取的信息
video_links = []
video_titles = []
video_views = []

video_favorites = []
video_divs = ''


# 检查请求是否成功
if response.status_code == 200:
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    # 找到每个视频块的<div>元素
    video_divs = soup.find_all('div', class_='col-xs-12 col-sm-4 col-md-3 col-lg-3')
    # print(video_divs[0])
    # print(video_divs[1])

    # 遍历视频块
    for video_div in video_divs:
        # 提取视频链接
        a_tag = video_div.find('a')
        video_link = a_tag['href']
        video_links.append(video_link)

        # 提取视频标题
        video_title = a_tag.find('span', class_='video-title').string.strip()
        video_titles.append(video_title)

        # 提取视频观看数
        views_span = video_div.find('span', class_='info', string='Views:')
        if views_span:
            # 获取<span>元素的下一个兄弟元素，即包含数字的文本节点
            views_text = views_span.find_next_sibling(string=True)
            # 提取文本节点的内容（即数字部分）
            video_view = views_text.strip()
            video_views.append(video_view)
        else:
            video_views.append(0)
    
        # 提取视频收藏数
        favorites_span = video_div.find('span', class_='info', string='Favorites:')
        if favorites_span:
            # 获取<span>元素的下一个兄弟元素，即包含数字的文本节点
            favorites_text = favorites_span.find_next_sibling(string=True)
            # 提取文本节点的内容（即数字部分）
            video_favorite = favorites_text.strip()
            video_favorites.append(video_favorite)
        else:
            video_favorites.append(0)

    # 打印提取的信息
    for i in range(len(video_links)):
        print(f"视频链接: {video_links[i]}")
        print(f"视频标题: {video_titles[i]}")
        print(f"视频观看数: {video_views[i]}")
        print(f"视频收藏数: {video_favorites[i]}")
    #     print("=" * 40)

