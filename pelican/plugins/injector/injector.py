# -*- coding: utf8 -*-

import logging
from bs4 import BeautifulSoup
from pelican import signals

log = logging.getLogger(__name__)

def inject_content(instance):
    """
    Function for injecting code
    """
    if instance._content is None:
        return

    soup_doc = BeautifulSoup(instance._content, 'html.parser')

    injections = instance.settings.get('INJECTOR_ITEMS', [])

    for injection in injections:
        if len(injection) not in (2, 3):
            log.warning("Invalid INJECTOR_ITEMS item: %s", injection)
            continue

        tag, code = injection[0], injection[1]
        position = 'after' if len(injection) < 3 else injection[2]

        tag_to_inject = soup_doc.find(tag)
        if not tag_to_inject:
            log.warning("The specified tag was not found: %s", tag)
            continue

        if position == 'before':
            tag_to_inject.insert_before(BeautifulSoup(code, 'html.parser'))
        else:
            tag_to_inject.append(BeautifulSoup(code, 'html.parser'))

    instance._content = str(soup_doc)


def article_writer(instance, content):
    """
    Callback for article_generator_write_article signal
    """
    if instance.settings.get('INJECTOR_IN_ARTICLES', False):
        inject_content(content)


def page_writer(instance, content):
    """
    Callback for page_generator_write_page signal
    """
    if instance.settings.get('INJECTOR_IN_PAGES', False):
        inject_content(content)


# TODO: An enhancement to consider for the future is using the get_writer signal method,
# which is invoked in Pelican.get_writer. This can return a custom Writer.
# This would be called after Pelican writes .html files.
# Adding a regex to indicate which filenames/paths would be affected by injection
# might also be a useful feature for users, and this could be integrated into the get_writer method.
# A regex could be specified by the user, to indicate on which filenames/paths injection should occur.
#
# Example of how this might look:
#
# def get_writer(instance):
#     """
#     Callback for get_writer signal
#     """
#     if instance.settings.get('INJECTOR_IN_WRITER', False):
#         # Perform regex matching on filenames/paths here
#         # ...

def register():
    """
    Part of Pelican API
    """
    signals.article_generator_write_article.connect(article_writer)
    signals.page_generator_write_page.connect(page_writer)
    # signals.get_writer.connect(get_writer)  # Uncomment this when get_writer method is implemented
