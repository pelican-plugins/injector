# -*- coding: utf8 -*-

import logging
from bs4 import BeautifulSoup
from pelican import signals

log = logging.getLogger(__name__)

def content_object_init(instance):
    """
    Pelican callback
    """
    if instance._content is None:
        return

    soup_doc = BeautifulSoup(instance._content, 'html.parser')

    injector_config = instance.settings.get('INJECTOR_CONFIG', [])
    
    for config in injector_config:
        if len(config) not in (2, 3):
            log.warning("Invalid INJECTOR_CONFIG item: %s", config)
            continue

        tag, code = config[0], config[1]
        position = 'after' if len(config) < 3 else config[2]

        tag_to_inject = soup_doc.find(tag)
        if not tag_to_inject:
            log.warning("The specified tag was not found: %s", tag)
            continue

        if position == 'before':
            tag_to_inject.insert_before(BeautifulSoup(code, 'html.parser'))
        else:
            tag_to_inject.append(BeautifulSoup(code, 'html.parser'))

    instance._content = str(soup_doc)


def register():
    """
    Part of Pelican API
    """
    signals.content_object_init.connect(content_object_init)
