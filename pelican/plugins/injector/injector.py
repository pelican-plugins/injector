import logging

from bs4 import BeautifulSoup

from pelican import signals

log = logging.getLogger(__name__)


def perform_injections(soup_doc, injections):
    """Perform code injections."""
    for injection in injections:
        tag, code = injection[0], injection[1]
        position = "after" if len(injection) < 3 else injection[2]

        tag_to_inject = soup_doc.find(tag)
        if tag_to_inject:
            if position == "before":
                tag_to_inject.insert_before(BeautifulSoup(code, "html.parser"))
            else:
                tag_to_inject.append(BeautifulSoup(code, "html.parser"))
        else:
            log.warning("The specified tag was not found: %s", tag)

    return str(soup_doc)


def inject_content(instance):
    """Inject code."""
    if instance._content is None:
        return []

    soup_doc = BeautifulSoup(instance._content, "html.parser")

    injections = instance.settings.get("INJECTOR_ITEMS", [])
    failed_injections = []

    for injection in injections:
        if len(injection) not in (2, 3):
            log.warning("Invalid INJECTOR_ITEMS item: %s", injection)
            continue

        tag = injection[0]
        tag_to_inject = soup_doc.find(tag)

        if not tag_to_inject:
            failed_injections.append(injection)
            continue

        soup_doc = BeautifulSoup(
            perform_injections(soup_doc, [injection]), "html.parser"
        )

    instance._content = str(soup_doc)
    instance._context["failed_injections"] = failed_injections


def article_writer(instance, content):
    """Use callback for article_generator_write_article signal."""
    if instance.settings.get("INJECTOR_IN_ARTICLES", False):
        inject_content(content)


def page_writer(instance, content):
    """Use callback for page_generator_write_page signal."""
    if instance.settings.get("INJECTOR_IN_PAGES", False):
        inject_content(content)

def final_injection_attempt(path, context):
    """Try to perform injections that failed in inject_content()."""
    failed_injections = context.get("failed_injections", [])
    if not failed_injections:
        return

    with open(path, 'r') as f:
        content = f.read()

    soup_doc = BeautifulSoup(content, "html.parser")
    new_content = perform_injections(soup_doc, failed_injections)

    with open(path, 'w') as f:
        f.write(new_content)


def register():
    """Register plugin with Pelican."""
    signals.article_generator_write_article.connect(article_writer)
    signals.page_generator_write_page.connect(page_writer)
    signals.content_written.connect(final_injection_attempt)
