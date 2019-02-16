from requests_html import HTMLSession
import database
import pdb

class MorgenProvider:
    def __init__(self, url):
        self.session = HTMLSession()
        try:
            self.content = self.session.get(url)
        except:
            self.content = False


    def result_titles(self):
        if self.content:
            try:
                return self.content.html.find('.nfy-search-item h2')[:2]
            except:
                return False
        else:
            return False

    def result_descriptions(self):
        if self.content:
            try:
                return self.content.html.find('.nfy-search-item p')[:2]
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
                data[index]['title'] = item.text
            except:
                next
        for index, item in enumerate(self.result_descriptions()):
            try:
                data[index]['summary'] = item.text
            except:
                next
        return data

    def third_item(self):
        try:
            item_data = [{
                'title': self.content.html.find('.nfy-search-item h2')[3].text,
                'summary': self.content.html.find('.nfy-search-item p')[3].text
                }]
            return item_data
        except:
            return False

class MockSearch:
    # Class Name is not accurate anymore: The search is real now.

    def __init__(self, search_term, user_id):
        self.term = search_term
        self.user_id = user_id
        self.search_url = f'https://www.morgenweb.de/suche_cosearch,{self.term}.html'
        self.save_search()

    def mock_result(self):
        result = MorgenProvider(self.search_url).data()
        return result or False

    def save_search(self):
        connection = database.TestDB().connection

        sql = ''' INSERT INTO user_tags(USER_UUID, TAG)
              VALUES(?,?) '''
        connection.execute(sql, (self.user_id, self.term))

        connection.commit()
        connection.close()
