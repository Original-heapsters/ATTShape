import json
import os
import config
import random
from watson_developer_cloud import PersonalityInsightsV3

watson_mapping = {
    'war' : 'military',
    'science-fiction' : 'science fiction',
    'historical' : 'documentary'
}

class GenreGenerator(object):

    def __init__(self, txt_file, movieFile, dest):
        self.txtfile = txt_file
        self.movieFile = movieFile
        self.dest = dest

        self.personality_insights = PersonalityInsightsV3(
            version='2016-10-20',
            username = config.ConfigVars['watKey'],
            password = config.ConfigVars['watPassword'],
            url = config.ConfigVars['waturl']
        )
        self.sure_list = []
        self.genre_dict = {}
        self.genre_list = self._send_personality_request()
        self._filter_movies_by_genre()

        self.cid_list = []
        self._generate_cid_list()
        self.generate_random_cid_list('romance')

    def _send_personality_request(self):
        """
        Sends out the api request and recieves a dictionary of the results.
        Getting the dictionary, the function strips away everything but the genres of movies
        watson predicts.
        Returns the list of genres that would match the user
        """
        with open( os.path.abspath(self.txtfile)) as personality_text:
            insights = self.personality_insights.profile(text=personality_text.read(), content_type='text/plain',
                raw_scores=True, consumption_preferences=True)

        with open('test.json', 'w') as f:
            json.dump(insights, f, indent=4)

        preference = insights.get('consumption_preferences')

        for pref in preference:
            if pref.get('consumption_preference_category_id') == 'consumption_preferences_movie':
                genre_list = []
                for genres in pref.get('consumption_preferences'):
                    if genres['score'] > 0:
                        genre_name = genres['name'].split(' ')[3]
                        genre_list.append(watson_mapping.get(genre_name, genre_name))

        return genre_list

    def _filter_movies_by_genre(self):
        """
        With the list of genres the function will reference the movies database json file.
        """
        with open(self.movieFile, 'r') as f:
            movie = json.load(f)

        for g in self.genre_list:
            self.genre_dict[g] = []

        for k, v in movie.items():
            if v.get('GENRE', None) is not None:
                m_g = v.get('GENRE').lower().replace(' ','').split(',')
                if len(m_g) > 1:
                    count = 0
                    for x in m_g:
                        if x in self.genre_list:
                            count += 1
                    if count > 1:
                        self.sure_list.append(k)
                for gen in self.genre_list:
                    if gen in v.get('GENRE').lower():
                        self.genre_dict[gen].append(k)


        with open(self.dest, 'w') as f:
            json.dump(self.genre_dict, f, indent=4, sort_keys=True)

    def _generate_cid_list(self, count=6):
        initial_list = []
        tmp_genre_dict = self.genre_dict
        while len(initial_list) < count:
            for k, v in tmp_genre_dict.items():
                v.sort()
                initial_list.append(v[0])
                v.remove(v[0])

        self.cid_list = initial_list[0:6]


    def generate_random_cid_list(self, genre, count=6):
        if genre not in self.genre_list:
            raise KeyError('genre: %s is not in genre_list: %s' % (genre, self.genre_list))
        
        ran_list = []
        tmp_genre_list = self.genre_dict[genre]

        while len(ran_list) < count:
            random_choice = random.choice(tmp_genre_list)
            ran_list.append(random_choice)
            tmp_genre_list.remove(random_choice)

        return ran_list[0:6]

    def get_cid_list(self):
        return self.cid_list

    def GetGenreList(self):
        return self.genre_list
