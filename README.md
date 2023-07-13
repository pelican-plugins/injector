# Injector: A Plugin for Pelican

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/injector/main.yml?branch=main)](https://github.com/pelican-plugins/injector/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-injector)](https://pypi.org/project/pelican-injector/)
![License](https://img.shields.io/pypi/l/pelican-injector?color=blue)

Injector is a plugin for the [Pelican](https://github.com/getpelican/pelican) static site generator that allows users to inject custom code before or after specific HTML tags, without modifying your theme.

## Installation

This plugin can be installed via:

    python -m pip install pelican-injector

As long as you have not explicitly added a `PLUGINS` setting to your Pelican settings file, then the newly-installed plugin should be automatically detected and enabled. Otherwise, you must add `injector` to your existing `PLUGINS` list. For more information, please see the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

## Settings

To configure the plugin, set the `INJECTOR_ITEMS` variable in your
Pelican settings file. This should be a list of tuples, each with two
or three elements, according to this table:

| Tuple Element | Description |
| ------ | ----------- |
| First | Name of the HTML tag where you want to inject your code |
| Second | The code you want to inject |
| Third (optional) | Specifies where to inject the code: 'before' or 'after'. If not provided, it defaults to 'after' |

```python
INJECTOR_ITEMS = [
    ('head', '<script>...</script>', 'after'),
    ('body', '<div>...</div>', 'before'),
    // add more tags and code as needed
]
```

In the following example, a script logging "Hello, world!" to the console is
injected into the `<head>` tag of each page, and a style block is injected
before the `<body>` tag.

```python
INJECTOR_ITEMS = [
    ('head', '<script>console.log("Hello, world!");</script>'),
    ('body', '<style>.custom-style { color: red; }</style>', 'before'),
]
INJECTOR_IN_PAGES = True
INJECTOR_IN_ARTICLES = False
```

## Contributing

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/injector/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

## License

This project is licensed under the [MIT license](https://opensource.org/licenses/MIT).

## Contact

If you have any questions or feedback, please open an issue on GitHub.
