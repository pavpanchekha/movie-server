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

@bottle.post("/hegemony")
def do_hegemony():
    servers = bottle.request.forms.get("server", [])
    for server in config.HOSTS:
        if server in servers:
            heg_ctl.start(server)
        else:
            heg_ctl.stop(server)
    return bottle.redirect("/")

    
@bottle.get("/movie/:id")
@bottle.view("movie")
def show_movie(id):
    mod = movie_ctl
    return dict(item=mod.info(id),
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
    return dict(item=mod.info(id),
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

@bottle.get("/")
def current():
    if movie_ctl.is_running():
        return bottle.redirect("/movie/%s" % movie_ctl.current())
    elif song_ctl.is_running():
        return bottle.redirect("/playlist" % movie_ctl.current())
    else:
        return bottle.redirect("/library")

if __name__ == "__main__":
    bottle.debug()
    bottle.run(host="0.0.0.0", port=8080, reloader=True)
