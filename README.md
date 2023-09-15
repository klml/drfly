# drfly

static website generator powered by Python, YAML, [Python-Markdown](https://python-markdown.github.io) and [mustache](https://github.com/defunkt/pystache).

There are many other and better [staticsitegenerators](http://staticsitegenerators.net), but I missed some features.
So drfly provides:

* __meta information__ for rendering (template, menue etc) or html metatags are at the __bottom__ of the page and only __optional__ (tried to use my own standard [PROSErial](https://github.com/klml/PROSErial)).
* the meta information is defined in `./meta.yaml` or in every directory (`meta.yaml`) or in the page  
* simple one-file templating with mustache, for plain websites.
* use source directories as __namespace__, with customizing namespaceseperators (```namespace:pagetitle```).
* include sourcefiles as __areas__ in templates (for menus, sidebars, trackingpixels).
* define [HTML Title element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title) ```<title>``` from first markdown heading as ```pagetitle``` if it is missing in meta (a function you have in [MkDocs](https://github.com/mkdocs/mkdocs/blob/master/docs/user-guide/writing-your-docs.md#meta-data)).
* non .md files (```.css```, ```.js``` or ```.txt```) get rendered with newlines as breaks (```<br>```).
* render specific files.


## usage

### cli

Change to source directory and render all pages:
```
cd /path/to/source/
drfly 
```

Render all pages from source directory:
```
drfly /path/to/source/ 
```

Render single page:
```
drfly /path/to/source/index.md 
```

### web
You can use git{hu|la}b as content webinterface and versioning system.

Get new commits with [webhook.py](drfly/webhook.py) (depends on [webpy.org](http://webpy.org))

```
pip3 install -r requirements-web.txt 
python3.6 drfly/webhook.py 8080 /path/to/source/
```

* Render a single page: `http://localhost:8080/render?page=index.md`
* Render all pages, by setting "webhook: renderall" `true` in [config](#config) and: `http://localhost:8080/render?all`
* Pull git repository and render all changed pages `curl -X PO http://localhost:8080/gitpull`


### config

There is the global config [drfly/meta.global.yaml](drfly/meta.global.yaml).
You can overwrite this values with a file `meta.yaml` in the root-directory oder every sub-directory.

## rendering

Drfly renders html and json files with [Python-Markdown](https://python-markdown.github.io/) using [Markdown Extra](https://python-markdown.github.io/extensions/extra/) with [Table of Contents](https://python-markdown.github.io/extensions/toc/), [WikiLinks](https://python-markdown.github.io/extensions/wikilinks/), [Sane Lists](https://python-markdown.github.io/extensions/sane_lists/) and [Admonition](https://python-markdown.github.io/extensions/admonition/).

You can add [Third-Party-Extensions](https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions) in [config](#config) `markdown: extensions:`