from html.parser import HTMLParser

class BeatmapParser(HTMLParser):
    __TAG_NAME = 'header'
    __CLASS_NAME = 'post-title entry-header'
    __ATTRIBUTES = ['author', 'date', 'song_name', 'difficulties', 'likes', 'dislikes']

    def __init__(self, html):
        HTMLParser.__init__(self)

        # parsing flags
        self.parsing_map = None
        self.current_attribute = 0

        # beatmap properties
        self.author = None
        self.date = None
        self.song_name = None
        self.difficulties = []
        self.likes = None
        self.dislikes = None

        # parse details from HTML
        self.feed(html)

    def __str__(self):
        return '-- "{2}" mapped by {0} on {1} for {3} (Likes: {4}, Dislikes: {5})'.format(self.author, self.date, self.song_name, self.difficulties, self.likes, self.dislikes)

    def handle_starttag(self, tag, attributes):
        if (tag == self.__TAG_NAME and self.parsing_map is None):
            for name, value in attributes:
                if name == 'class' and value == self.__CLASS_NAME:
                    self.parsing_map = True

    def handle_endtag(self, tag):
        if (tag == self.__TAG_NAME and self.parsing_map):
            self.parsing_map = False

    def handle_data(self, data):
        if (self.parsing_map):
            if (not data.isspace() and not data == 'Difficulties'):
                stripped_data = data.replace('\n', '').strip()
                if (self.__ATTRIBUTES[self.current_attribute] == 'difficulties'):
                    if (stripped_data.isnumeric()):
                        self.current_attribute += 1
                    else:
                        self.difficulties.append(stripped_data)
                        return
                setattr(self, self.__ATTRIBUTES[self.current_attribute], stripped_data)
                self.current_attribute += 1
    
    def get_ratio():
        return self.likes / (self.likes + self.dislikes)

    def get_date():
        return self.date