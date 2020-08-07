# -*- coding: utf-8 -*-

from resources.lib.modules import log_utils
from resources.lib.modules import control

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

try:
    AddonVersion = control.addon('plugin.video.tempest').getAddonInfo('version')
    RepoVersion = control.addon('repository.tempest').getAddonInfo('version')

    log_utils.log(' TEMPEST PLUGIN VERSION: %s ' % str(AddonVersion), log_utils.LOGNOTICE)
    log_utils.log(' TEMPEST REPOSITORY VERSION: %s ' % str(RepoVersion), log_utils.LOGNOTICE)
except:
    log_utils.log('CURRENT TEMPEST VERSIONS REPORT ', log_utils.LOGNOTICE)
    log_utils.log('### ERROR GETTING TEMPEST VERSIONS - NO HELP WILL BE GIVEN AS THIS IS NOT AN OFFICIAL TEMPEST INSTALL. ', log_utils.LOGNOTICE)