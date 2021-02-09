import requests
from beatmap_parser import BeatmapParser

class BeatmapScraper():
    __ROOT_URL = 'https://bsaber.com/songs/{0}/'
    __RATIO_THRESHOLD = 0.95
    __LIKE_THRESHOLD = 500
    __DISLIKE_THRESHOLD = 5

    def __init__(self, beatmap_ids):
        # beatmap is considered "important" based on likes and dislikes
        important_beatmaps = []

        # iterate over beatmaps to find important ones
        for beatmap_id in beatmap_ids:
            # retrieve page content
            URL = self.__ROOT_URL.format(beatmap_id)
            page = requests.get(URL)
            html = page.content.decode("utf-8")
            # parse details
            beatmap = BeatmapParser(html)
            likes, dislikes = beatmap.get_likes(), beatmap.get_dislikes()
            # save map
            if (self.should_save_map(likes, dislikes)):
                print('~ Adding map to save list')
                important_beatmaps.append(beatmap_id)
        print(important_beatmaps)


    def should_save_map(self, likes, dislikes):
        if (likes is None or dislikes is None):
            return False
        elif (likes >= self.__LIKE_THRESHOLD and dislikes >= self.__DISLIKE_THRESHOLD and (likes / (likes + dislikes)) >= self.__RATIO_THRESHOLD):
            return True
        return False