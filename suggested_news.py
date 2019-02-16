import json
import pdb
import database

class SuggestedNews:
    mock_data = {'trump': [{'title': 'Vorwurf des Machtmissbrauchs', 'summary': 'WASHINGTON. Die Gefahr einer weiteren Haushaltssperre mit Verwaltungsstillstand in den USA ist vorerst abgewendet. Dafür haben sich die politischen Fronten massiv verhärtet.'}]}

    def __init__(self, user_id):
        self.user_id = user_id
        self.search_term = self.search_term()

    def search_url(self):
        return f'https://www.morgenweb.de/suche_cosearch,{self.term}.html'

    def search_term(self):
        return self.find_latest_tag()

    def mock_result(self):
        print(self.user_id)
        print(self.search_url)
        print(self.search_term)
        if self.search_term:
            result = self.mock_data.get(self.search_term, False)
            return result
        else
        return False

    def find_latest_tag(self):
        rows = database.TestDB().user_tags().fetchall()
        res_list = []
        for row in rows:
            if row[1] == self.user_id:
                if self.mock_data.get(row[2], False):
                    res_list.append(row[2])
        if res_list:
            return(res_list[-1])
        else:
            return False

