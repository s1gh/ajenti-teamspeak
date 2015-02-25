import ts3
from ajenti.api import plugin, BasePlugin
from ajenti.plugins.configurator.api import ClassConfigEditor


class User(object):
    def __init__(self, user, channelid, userid, icon='user'):
        self.username = user
        self.channel = channelid
        self.uid = userid
        self.icon = icon

@plugin
class TeamspeakClassConfigEditor(ClassConfigEditor):
    title = 'Teamspeak'
    icon = 'comments'

    def init(self):
        self.append(self.ui.inflate('teamspeak3:config'))


@plugin
class TeamspeakBackend(BasePlugin):
    default_classconfig = {'addr': '127.0.0.1:10011', 'username': 'serveradmin', 'password': ''}
    classconfig_editor = TeamspeakClassConfigEditor

    def initialize(self):
        addr = self.classconfig['addr'].rsplit(':')
        username = self.classconfig['username']
        password = self.classconfig['password']

        if not addr:
            raise Exception('No address specified!')

        try:
            self._connection = ts3.TS3Server(addr[0], int(addr[1]))  # Stupid casting (Needs to be done though)
            self._connection.login(username, password)
            self._connection.use(1)
        except Exception as err:
            raise Exception(str(err))

    def clientlist(self):
        clients = self._connection.clientlist()
        clients_dic = []

        for key, client in clients.iteritems():
            clients_dic.append(User(client['client_nickname'], client['cid'], client['clid']))

        return clients_dic

    def channellist(self):
        channels = self._connection.send_command('channellist')
        return channels

    def clientpoke(self, clid, message='Hello!'):
        self._connection.clientpoke(clid, message)
        return

    def clientkick(self, clid, message='Get out!'):
        self._connection.clientkick(clid, message=message)
        return