from ajenti.api import *
from ajenti.plugins import *


info = PluginInfo(
    title='Teamspeak',
    icon='comments',
    dependencies=[
        PluginDependency('main'),
        PluginDependency('dashboard'),
        ModuleDependency('ts3'),
    ],
)


def init():
    import main
