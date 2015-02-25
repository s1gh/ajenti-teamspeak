from __future__ import print_function

from ajenti.api import *
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui.binder import Binder

from backend import TeamspeakBackend


@plugin
class Teamspeak(SectionPlugin):
    def init(self):
        self.title = 'Teamspeak'
        self.icon = 'comments'
        self.category = _('Software')
        self.append(self.ui.inflate('teamspeak3:main'))
        self.backend = TeamspeakBackend.get()
        self.users = []
        self.binder = Binder(self, self)

        def post_item_bind(object, collection, item, ui):
            ui.find('poke').on('click', self.on_poke, item)
            ui.find('kick').on('click', self.on_kick, item)

        self.find('users').post_item_bind = post_item_bind

    def on_poke(self, item):
        self.context.notify('info', 'Client has been poked!')
        self.backend.clientpoke(item.uid)

    def on_kick(self, item):
        self.context.notify('info', 'Client has been kicked!')
        self.backend.clientkick(item.uid)

    def on_page_load(self):
        self.refresh()

    def refresh(self):
        try:
            self.backend.initialize()
        except Exception as err:
            self.context.notify('error', err.message)
            self.context.launch('configure-plugin', plugin=self.backend)
            return

        self.binder.update()
        self.users = self.backend.clientlist()
        self.binder.populate()