import database
import mock_search

class SuggestedNews:
    def __init__(self, user_id):
        self.user_id = user_id
        self.search_term = self.search_term()

    def search_url(self):
        return f'https://www.morgenweb.de/suche_cosearch,{self.search_term}.html'

    def search_term(self):
        return self.find_latest_tag()

    def mock_result(self):
        if self.search_term:
            try:
                res = mock_search.MorgenProvider(self.search_url()).third_item()
                return res
            except:
                return False
        else:
            return False

    def find_latest_tag(self):
        rows = database.TestDB().user_tags().fetchall()
        res_list = []
        for row in rows:
            if row[1] == self.user_id:
                try:
                    res_list.append(row[2])
                except:
                    return False
        if res_list:
            return(res_list[-1])
        else:
            return False
