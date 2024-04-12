#encoding=utf-8
import meilisearch

# 插入数据 索引没有primary key，就要在添加数据的时候加key


class SearchEngine(object):
    def __init__(self, master_key=None, host='http://127.0.0.1:7700'):
        if master_key is None:
            self.client = meilisearch.Client(host) # masterKey
        else:
            self.client = meilisearch.Client(host, master_key) # masterKey
    
    def get_index(self, index_name):
        return self.client.index(index_name)

    def add_document(self, index_name, docs, primary_key=None):
        if docs is None or len(docs) == 0:
            return None
        index = self.get_index(index_name)
        if primary_key is None:
            ret = index.add_documents(docs)
        else:
            ret = index.add_documents(docs, primary_key)
            
        return ret
    
    def get_document(self, index_name):
        return self.client.index(index_name).get_documents({
            'limit':10,
            'fields': ['share_url'],
        })
    
    def create_index(self, index_name, primary_key):
        return self.client.create_index(index_name, {"primaryKey": primary_key })
    
    #判断索引是否存在
    def has_index(self, index_name):
        infos = self.client.get_indexes()
        if infos is None:
            return False
        for index in infos['results']:
            if index_name == index:
                return True
        return False

    def get_infos(self):
        infos = self.client.get_indexes()
        for index in infos['results']:
            docs = index.get_documents()
            print('infos: ', index.uid, docs.total)

if __name__ == '__main__':
    SearchEngine()
