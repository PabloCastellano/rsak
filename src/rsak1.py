#!/usr/bin/env python
# GPL
# Pablo castellano

PLUGINSDIR = "plugins"
pluginfiles = os.listdir(PLUGINSDIR)
plugins = [os.path.splitext(f)[0] for f in pluginslist]
map(__import__, PLUGINSDIR+pluginfiles)

f = getattr(backend, funcname)
self.__setattr__(funcname, f)

#http://pytute.blogspot.com/2007/04/python-plugin-system.html
