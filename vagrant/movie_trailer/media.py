import webbrowser
class Movie:
    # This class creates a movie object with a predefined class variable. 
    VALID_RATINGS=["G", "PG", "PG-13", "R", "NC17", "X"]
    #self has to be the first var being declared
    def __init__(self, movie_title, movie_storyline,valid_rating, poster_image, trailer_youtube):
        self.title = movie_title
        self.storyline = movie_storyline
        self.valid_rating = valid_rating
        self.poster_image_url =poster_image
        self.trailer_youtube_url =trailer_youtube
    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)