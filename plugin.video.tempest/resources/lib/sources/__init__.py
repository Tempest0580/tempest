# -*- coding: utf-8 -*-

import pkgutil
import os.path

from resources.lib.modules import log_utils

try:
    from resources.lib.modules import cfscrape
    cfscrape = cfscrape.create_scraper(delay=5)
except:
    pass

__all__ = [x[1] for x in os.walk(os.path.dirname(__file__))][0]


def sources():
    try:
        sourceDict = []
        for i in __all__:
            for loader, module_name, is_pkg in pkgutil.walk_packages([os.path.join(os.path.dirname(__file__), i)]):
                if is_pkg:
                    continue

                try:
                    module = loader.find_module(module_name).load_module(module_name)
                    sourceDict.append((module_name, module.source()))
                except Exception as e:
                    log_utils.log('Could not load "%s": %s' % (module_name, e), log_utils.LOGDEBUG)
        return sourceDict
    except:
        return []


def getAllHosters():
    def _sources(sourceFolder, appendList):
        sourceFolderLocation = os.path.join(os.path.dirname(__file__), sourceFolder)
        sourceSubFolders = [x[1] for x in os.walk(sourceFolderLocation)][0]
        for i in sourceSubFolders:
            for loader, module_name, is_pkg in pkgutil.walk_packages([os.path.join(sourceFolderLocation, i)]):
                if is_pkg:
                    continue
                try: mn = str(module_name).split('_')[0]
                except: mn = str(module_name)
                appendList.append(mn)
    sourceSubFolders = [x[1] for x in os.walk(os.path.dirname(__file__))][0]
    appendList = []
    for item in sourceSubFolders:
        if item != 'modules':
            _sources(item, appendList)
    return list(set(appendList))
