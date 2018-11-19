# 整合新浪新闻的内文信息
import requests
from bs4 import BeautifulSoup
import json

# 原新闻链接： https://news.sina.com.cn/c/2018-11-14/doc-ihmutuec0089225.shtml
# 提取：newsid：hmutuec0089225
def getCommentCounts(news_url):
    comment_url = 'https://comment.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3' # 使用大括号
    news_id = news_url.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
    # 也可以通过正则表达式来获取news_id
    # m = re.search('doc-i(.*).shtml', news_url)
    # news_id = m.group(1)
    comments = requests.get(comment_url.format(news_id))  # 将news_id放到comment_url中,获取评论的数据
    jd = json.loads(comments.text)
    return jd['result']['count']['total']  # 返回评论数


# 获取新闻的详细信息
def getNewsDetail(news_url):
    results = {}  # 存储结果
    res = requests.get(news_url)  # 获取新闻页面
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')  # 解析
    results['title'] = soup.select('.main-title')[0].text  # 取标题
    results['date'] = soup.select('.date')[0].text  # 提取时间
    results['source'] = soup.select('.source')[0].text  # 提取来源

    article = []
    # 提取新闻内容，因为倒数第一个<p>是责任编辑，要去掉
    for p in soup.select('#article p')[:-1]:
        article.append(p.text.strip())

    results['article'] = ' '.join(article)  # 新闻内容连接成字符串，存到results中
    # 取倒数第一个<p>标签中的内容,即责任编辑
    results['editor'] = soup.select(".show_author")[0].text.strip('责任编辑：')
    results['counts'] = getCommentCounts(news_url)  # 获取评论数
    return results


# 原新闻链接： https://news.sina.com.cn/c/2018-11-14/doc-ihmutuec0089225.shtml
if __name__ == "__main__":
    news = "https://news.sina.com.cn/c/2018-11-14/doc-ihmutuec0089225.shtml"
    results = getNewsDetail(news)  # 获取新闻内容信息
    print(results)
