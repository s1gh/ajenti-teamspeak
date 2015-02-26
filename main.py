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
        self.servers = []
        self.banlist = []
        self.binder = Binder(self, self)

        def post_item_bind_users(object, collection, item, ui):
            ui.find('poke').on('click', self.on_poke, item)
            ui.find('kick').on('click', self.on_kick, item)
            ui.find('ban').on('click', self.on_ban, item)

        def post_item_bind_banlist(object, collection, item, ui):
            ui.find('unban').on('click', self.on_unban, item)

        self.find('users').post_item_bind = post_item_bind_users
        self.find('banlist').post_item_bind = post_item_bind_banlist

    def on_poke(self, item):
        self.backend.clientpoke(item.uid)
        self.context.notify('info', 'Client has been poked!')

    def on_kick(self, item):
        self.backend.clientkick(item.uid)
        self.refresh()
        self.context.notify('info', 'Client has been kicked from the server!')

    def on_ban(self, item):
        self.backend.clientban(item.username)  # @todo Change this to IP Address!
        self.refresh()
        self.context.notify('info', 'Client has been banned from the server!')

    def on_unban(self, item):
        self.backend.clientunban(item.banid)
        self.refresh()
        self.context.notify('info', 'Client has been unbanned from the server!')

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
        self.servers = self.backend.serverinfo()
        self.banlist = self.backend.banlist()
        self.binder.populate()