# pelican-injector

Pelican-Injector is a plugin for the Pelican static site generator that
allows users to inject custom code before or after specific HTML tags,
without modifying your theme.

## Requirements

* BeautifulSoup4

To install it using pip, type: `pip install bs4`

## Installation

Download the `pelican_injector.py` file and place it into your Pelican plugins directory.

Then add `pelican_injector` to your `PLUGINS` list in the `pelicanconf.py` file:

```
    PLUGINS_PATH = [
        # [...]
        'path/to/your/plugins'
    ]
    PLUGINS = [
         # [...]
        'pelican_injector',
    ]
```


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
Contributions are welcome! Please fork this repository and create a pull request with your changes.

## License
This project is licensed under the MIT License.

## Contact
If you have any questions or feedback, please open an issue on GitHub.
