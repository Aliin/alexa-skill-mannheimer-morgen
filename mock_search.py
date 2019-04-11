import urllib3
from bs4 import BeautifulSoup
import pdb
import re
import certifi
import boto3

dynamodb = boto3.resource('dynamodb')

class MorgenProvider:
    def __init__(self, url):
        try:
            http_pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            self.content = http_pool.request('GET',url).data.decode('utf-8')
            self.soup = BeautifulSoup(self.content, 'html.parser')
        except:
            self.content = False

    def result_titles(self):
        if self.content:
            try:
                return self.soup.select('.nfy-search-item h2')[:2]
            except:
                return False
        else:
            return False

    def result_descriptions(self):
        if self.content:
            try:
                return self.soup.select('.nfy-search-item p')[:2]
            except:
                return False
        else:
            return False

    def data(self):
        data = [{}, {}]
        if not self.result_titles() or not self.result_descriptions():
            return False
        for index, item in enumerate(self.result_titles()):
            try:
                data[index]['title'] = item.contents[0]
            except:
                next
        for index, item in enumerate(self.result_descriptions()):
            try:
                data[index]['summary'] = item.contents[0]
            except:
                next
        return data

    def third_item(self):
        try:
            item_data = [{
                'title': self.soup.select('.nfy-search-item h2')[3].contents[0],
                'summary': self.soup.select('.nfy-search-item p')[3].contents[0]
                }]
            return item_data
        except:
            return False

class MockSearch:
    # Class Name is not accurate anymore: The search is real now.

    def __init__(self, search_term, user_id):
        self.term = re.sub('\s+', '+', search_term)
        self.user_id = user_id
        self.search_url = f'https://www.morgenweb.de/suche_cosearch,{self.term}.html'
        self.save_search()

    def mock_result(self):
        result = MorgenProvider(self.search_url).data()
        return result or False

    def save_search(self):
        table = dynamodb.Table('user_tags')
        table.put_item(
            Item={
                'uuid': self.user_id,
                'tag': self.term
            }
        )
