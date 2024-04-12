#encoding=utf-8
from base_news import BaseNews
import json
import re
import time
import os
from meiliSearchObject import SearchEngine
import hashlib

class Document(object):
    def __init__(self, title, share_url, ctime, brief, stock_list):
        self.ctime = ctime if ctime is not None else ""
        self.title = title if title is not None else ""
        self.share_url = share_url if share_url is not None else ""
        self.brief = brief if brief is not None else ""
        self.stock_list = stock_list if stock_list is not None else []
    
    def toString(self):
        return '''
            Document: 
            "title" + %s,
            "share_url" + %s,
            "ctime" + %s,
            "brief" + %s
        ''' % (self.title, self.share_url, self.ctime, self.brief)
    
    def toEngine(self):
        return {
            "title": self.title,
            "share_url": self.share_url,
            "ctime": self.ctime,
            "brief": self.brief,
            "md5_id": hashlib.md5(self.share_url.encode('utf-8')).hexdigest(),
            "stock_list": self.stock_list
        }

class ClsNews(BaseNews):
    def __init__(self, url, master_key, host):
        super().__init__()
        self.url = url
        self.dot = re.compile('<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', re.S|re.M)
        self.record_path = 'record/%s' % 'cls_record.dat'
        self.record = set(self.open_file(self.record_path))
        self.document_list = list()

        #engion 
        self.engine = SearchEngine(master_key=master_key, host=host)
        self.index_name = 'test_cls_5'
        primary_key = 'md5_id'
        
        # if index exists
        if not self.engine.has_index(self.index_name): 
            self.engine.create_index(self.index_name, primary_key)
    
    def main(self):
        self.run(self.url, False)
    
    def open_file(self, path):
        def has_file(path):
            if not os.path.isfile(path):
                with open(path, 'w') as f:
                    pass
        has_file(path)                        
        with open(path) as f:
            for line in f:
                yield line.strip()
    
    def save_file(self, data_list, path):
        data_string = '\n'.join(data_list)
        with open(path, 'w') as fw:
            fw.write(data_string)


    def get_ctime(self, time_stramp): # 
        time_arr = time.localtime(time_stramp)
        ctime = time.strftime("%Y-%m-%d %H:%M:%S", time_arr)
        return ctime
    
    def parse(self, html, is_dingding):
        # print(html)
        item_list = self.dot.findall(html)
        for item in item_list:
            dic = json.loads(item)
            news_list = dic['props']['initialState']['telegraph']['telegraphList']
            dd_str = '@lrj'
            
            for idx, doc in enumerate(news_list):
                ctime = self.get_ctime(doc['modified_time'])
                title = '' if doc['title'] == '' else '【%s】' % doc['title']
                share_url = doc['shareurl']
                brief = doc['brief']
                stock_list = doc['stock_list']

                document = Document(title.strip(), share_url.strip(),
                    ctime.strip(), brief.strip(), stock_list)
		
		        #过滤重复	
                if share_url in self.record:
                    continue
		
                #增加新的item到过滤列表
                self.record.add(document.share_url)
                self.document_list.append(document)

        self.save_file(self.record, self.record_path)
        dds = [ doc.toEngine() for doc in self.document_list]
        
        #index_name = 'test_cls_5'
        #primary_key = 'md5_id'
        #self.engine.create_index(index_name, primary_key)

        ret = self.engine.add_document(self.index_name, dds)
        #ss = self.engine.get_document(self.index_name)
        self.engine.get_infos()

if __name__ == '__main__':
    url = 'https://www.cls.cn/telegraph'
    master_key = 'YqvEfpsUzmCtT5HK0aobSvssCwfQLpj-tdMbiY7mpW4'
    host = 'http://127.0.0.1:7701'
    cls = ClsNews(url, master_key, host)
    cls.main()
