#!/usr/bin/env python2.7

import bottle
import config

# Init

from moviedir import VLCDir
movie_ctl = VLCDir(config.MOVIEDIR, config.TMPDIR)
from mpdaemon import MPDaemon
song_ctl = MPDaemon()
from hegemony import Hegemony
heg_ctl = Hegemony(config.HOSTS)
    
@bottle.get("/movie/:id")
@bottle.view("movie")
def show_movie(id):
    mod = movie_ctl
    return dict(item=mod.current(id),
                name=id,
                is_playing=mod.is_playing(),
                hosts=config.HOSTS,
                heg=heg_ctl.status_all())

@bottle.post("/movie/:id")
def post_movie(id):
    action = bottle.request.forms.get("action", "none")

    if action == "start":
        movie_ctl.start(id)
    elif action == "play":
        movie_ctl.play()
    elif action == "pause":
        movie_ctl.pause()
    elif action == "stop":
        movie_ctl.stop()

    return show_movie(id)

@bottle.get("/playlist/:id")
@bottle.view("playlist")
def show_playlist(id):
    mod = song_ctl
    return dict(item=mod.current(id),
                name=id,
                is_playing=mod.is_playing(),
                hosts=config.HOSTS,
                heg=heg_ctl.status_all())

@bottle.post("/playlist/:id")
def post_playlist(id):
    action = bottle.request.forms.get("action", "none")

    if action == "start":
        song_ctl.start(id)
    elif action == "play":
        song_ctl.play()
    elif action == "pause":
        song_ctl.pause()
    elif action == "stop":
        song_ctl.stop()
    elif action == "skip":
        pos = int(bottle.request.forms.get("position", 0)) + 1;
        song_ctl.skip(pos);

    return show_playlist(id)

@bottle.get("/library")
@bottle.view("library")
def show_library():
    movies = movie_ctl.library()
    playlists = song_ctl.library()
    return dict(movies=movies, playlists=playlists)

@bottle.get("/library/playlists")
@bottle.view("libplaylists")
def show_playlists():
    playlists = song_ctl.library()
    return dict(playlists=playlists)

@bottle.get("/library/movies")
@bottle.view("libmovies")
def show_movies():
    movies = movie_ctl.library()
    return dict(movies=movies)

@bottle.route("/static/:filename")
def static(filename):
    return bottle.static_file(filename, root='static/')

@bottle.get("/current")
def current():
    if movie_ctl.is_running():
        return bottle.redirect("/movie")
    elif song_ctl.is_running():
        return bottle.redirect("/playlist")
    else:
        return bottle.redirect("/library")

@bottle.get("/")
def index():
    return bottle.redirect("/current")

@bottle.post("/")
def POST():
    req = bottle.request
    action = req.forms.get("action", "none")

    if action == "hegemony":
        servers = req.forms.get("server", [])
        for server in config.HOSTS:
            if server in servers:
                heg_ctl.start(server)
            else:
                heg_ctl.stop(server)
        return bottle.redirect("/current")

    cmod = movie_ctl if movie_ctl.is_running() else \
           song_ctl  if song_ctl.is_running()  else \
           None
    if cmod:
        if action == "play":
            cmod.play()
        elif action == "pause":
            cmod.pause()
        elif action == "stop":
            cmod.stop()
        elif cmod == song_ctl and action == "skip":
            pos = int(req.forms.get("position", 0)) + 1;
            cmod.skip(pos);
    else:
        if action == "start":
            type, id = req.forms.get("file", "").split(":", 1)
            if type == "movie":
                movie_ctl.start(id)
                return bottle.redirect("/movie/%s" % id)
            elif type == "playlist":
                song_ctl.start(id)
                return bottle.redirect("/playlist/%s" % id)
            else:
                raise ValueError("Unknown type `%s`" % type)
    return bottle.redirect("/current")

if __name__ == "__main__":
    bottle.debug()
    bottle.run(host="localhost", port=8080, reloader=True)
