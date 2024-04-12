#encoding=utf-8
import requests



class BaseNews(object):
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            ,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
    
    def open_url(self, url):
        r = requests.get(url, headers = self.header)
        html = r.content.decode('utf8')
        print(r.headers)
        print('\n')
        return html

    def parse(self,html, re_func):
        '''
        parse html
        '''
        print('parse html, rewrite function')
    
    '''
    is_dingding: True 发送钉钉消息
    '''
    def run(self, url, is_dingding=False):
        html = self.open_url(url)
        self.parse(html, is_dingding)

if __name__ == '__main__':
    news = BaseNews()
    news.open_url('http://www.baidu.com')
