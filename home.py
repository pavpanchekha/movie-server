#!/usr/bin/env python2.6

import web
import config

urls = (
    '/', 'index'
)

app = web.application(urls, globals())
render = web.template.render("templates/")

class index(object):
    def show_current(self, mod):
        return render.status(mod.current(), mod.is_playing())

    def show_library(self):
        items = [(mod.title, mod.library()) for mod in config.MODULES]
        return render.library(items)
    
    def GET(self):
        for mod in config.MODULES:
            if mod.is_running():
                return self.show_current(mod)
        else:
            return self.show_library()

    def POST(self):
        action = web.input(action="none").action
        if action == "none":
            return self.GET()

        for mod in config.MODULES:
            if mod.is_running():
                assert action != "start", "Attempted to start file when file already playing"
                {"play":  mod.play,
                 "pause": mod.pause,
                 "stop":  mod.stop}[action]()
                break
        else:
            assert action in ("none", "start"), "Attempted action on not playing file"
            type, id = web.input().file.split(":", 1)
            for mod in config.MODULES:
                if mod.title == type:
                    {"start": mod.start}[action](id)
                    break
            else:
                assert False, "No module can handle `%s` type" % type
        return web.seeother("/")

if __name__ == "__main__":
    app.run()
