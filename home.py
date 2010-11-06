import web
import os
from imdb import IMDb
import config
from moviedata import Movie

ia = IMDb()

urls = (
    '/', 'index'
)

app = web.application(urls, globals())
render = web.template.render("templates/")

class index(object):
    def __init__(self):
        import mplayer
        self.mplayer = mplayer.MPlayer()

    def show_current(self):
        curr = self.mplayer.state["movie"]
        assert curr is not None, "Movie must be playing to show current movie"
        movie = Movie(curr)
        is_playing = self.mplayer.state["playing"]
        return render.status(movie, is_playing)

    def show_library(self):
        assert self.mplayer.state["movie"] is None, "Attempted to show library while movie playing!"

        library = [os.path.join(config.MOVIE_DIR, file) for file in os.listdir(config.MOVIE_DIR)]
        library = [os.path.split(x)[-1] for x in library if os.path.isfile(x)]
        library = map(Movie, library)
        return render.library(library)
    
    def GET(self):
        if self.mplayer.state["movie"] is not None:
            return self.show_current()
        else:
            return self.show_library()

    def POST(self):
        action = web.input(action="none").action
        {"none":  lambda: None,
         "play":  self.mplayer.play,
         "pause": self.mplayer.pause,
         "stop":  self.mplayer.stop,
         "notstart": lambda: self.mplayer.notstart(web.input().file),
         "start": lambda: self.mplayer.start(web.input().file)}[action]()
        return self.GET()

if __name__ == "__main__":
    app.run()
