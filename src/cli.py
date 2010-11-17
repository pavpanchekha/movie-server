#!/usr/bin/env python

from moviedir import VLCDir
movie_ctl = VLCDir("/srv/movie-server/movies")
from mpdaemon import MPDaemon
song_ctl = MPDaemon()

def show_movie():
    out = movie_ctl.current()
    print "[%s] %s [%s]" % ("playing" if movie_ctl.is_playing() else "paused", out["title"], "*" * out["rating"])
    print
    print "%s (%s)" % (out["description"], out["duration"])

def show_playlist():
    out = song_ctl.current()
    print "[%s] %s" % ("playing" if song_ctl.is_playing() else "paused", out["title"])
    print
    for i, title in out["songs"][out["position"] - 2 : out["position"] + 3]:
        print "%2d: %s" % (i + 1, title)

def show_library():
    import textwrap
    movies = movie_ctl.library()
    playlists = song_ctl.library()

    maxid = max(len(obj["id"]) for obj in movies + playlists)

    print "== [Movies] =="
    for movie in movies:
        print (movie["id"] + ":").ljust(maxid+1), movie["title"], "[%s]" % ("*" * movie["rating"])
    print
    print "== [Playlists] =="
    for playlist in playlists:
        print (playlist["id"] + ":").ljust(maxid+1), playlist["title"]

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    if len(args) == 0 or args[0] == "status":
        if movie_ctl.is_running():
            show_movie()
        elif song_ctl.is_running():
            show_playlist()
        else:
            print "[error] No currently-playing media"
    elif len(args) == 1 and args[0] == "library":
        show_library()
    elif len(args) == 1 and args[0] in ("play", "pause", "stop"):
        cmod = self.movie_ctl if self.movie_ctl.is_running() else \
               self.song_ctl  if self.song_ctl.is_running()  else \
               None
        if cmod == "None":
            print "[error] No currently-playing media to %s" % args[0]
        else:
            getargs(cmod, args[0])()
    elif len(args) == 2 and args[0] == "skip":
        cmod = self.movie_ctl if self.movie_ctl.is_running() else \
               self.song_ctl  if self.song_ctl.is_running()  else \
               None
        try:
            id = int(args[1])
        except ValueError:
            print "[error] `%s` is not a valid integer" % args[1]
        else:
            if cmod == "None":
                print "[error] No currently-playing media to %s" % args[0]
            else:
                cmod.skip(id)
    elif len(args) == 2 and args[0] in ("movie", "playlist"):
        mod = movie_ctl if args[0] == "movie" else song_ctl
        try:
            mod.start(args[1])
        except Exception as e:
            print "[error] %s" % e
    else:
        print "Control movie-server from the command line"
        print
        print "USAGE: movie-server status           Show information about the current media"
        print "     | movie-server library          Show media library"
        print "     | movie-server movie <name>     Play movie <name>"
        print "     | movie-server playlist <name>  Start playlist <name>"
        print "     | movie-server skip <id>        Skip to song <id> on playlist"
        print "     | movie-server play"
        print "     | movie-server pause"
        print "     | movie-server stop"
