#!/usr/bin/env python2.7

import web
import config

urls = (
    '/', 'index'
)

app = web.application(urls, globals())
render = web.template.render("templates/")

class index(object):
    def __init__(self):
        from moviedir import VLCDir
        self.movie_ctl = VLCDir(config.MOVIEDIR, config.TMPDIR)
        from mpdaemon import MPDaemon
        self.song_ctl = MPDaemon()
        from hegemony import Hegemony
        self.heg_ctl = Hegemony(config.HOSTS)
    
    def show_movie(self):
        mod = self.movie_ctl
        return render.movie(mod.current(), mod.is_playing(), config.HOSTS, self.heg_ctl.status_all())

    def show_playlist(self):
        mod = self.song_ctl
        return render.playlist(mod.current(), mod.is_playing(), config.HOSTS, self.heg_ctl.status_all())

    def show_library(self):
        movies = self.movie_ctl.library()
        playlists = self.song_ctl.library()
        return render.library(movies, playlists)
    
    def GET(self):
        if self.movie_ctl.is_running():
            return self.show_movie()
        elif self.song_ctl.is_running():
            return self.show_playlist()
        else:
            return self.show_library()

    def POST(self):
        action = web.input(action="none").action

        if action == "hegemony":
            servers = web.input(server=[]).server
            for server in config.HOSTS:
                if server in servers:
                    self.heg_ctl.start(server)
                else:
                    self.heg_ctl.stop(server)
            return web.seeother("/")

        cmod = self.movie_ctl if self.movie_ctl.is_running() else \
               self.song_ctl  if self.song_ctl.is_running()  else \
               None
        if cmod:
            if action == "play":
                cmod.play()
            elif action == "pause":
                cmod.pause()
            elif action == "stop":
                cmod.stop()
            elif cmod == self.song_ctl and action == "skip":
                pos = int(web.input().position) + 1;
                cmod.skip(pos);
        else:
            if action == "start":
                type, id = web.input().file.split(":", 1)
                if type == "movie":
                    self.movie_ctl.start(id)
                elif type == "playlist":
                    self.song_ctl.start(id)
                else:
                    raise ValueError("Unknown type `%s`" % type)
        return web.seeother("/")

if __name__ == "__main__":
    app.run()
