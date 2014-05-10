## SoPaper, So Easy
This is a project designed for researchers to conveniently getting papers they need.

It includes a command line tool ``paper-downloader.py``, to automatically search and download paper,
as well as a server to provide integrated search/read/download experience.

This project served as a course project for __Service Oriented Software Engineering(2014Spring)__
and __Search Engine Technology(2014Spring)__, developed by:
* [Yuxin Wu(ppwwyyxx)](mailto:ppwwyyxxc@gmail.com)
* Tiezheng Li
* Yichen Wang

This project is still in development stage. Ideas / issues are welcomed.

## Features
The ``searcher`` package will search and analyse results in
* Google Scholar
* Google

and the ``fetcher`` package is able to further analyse the result and download the paper from:
* direct pdf link
* [dl.acm.org](http://dl.acm.org/)
* [ieeexplore.ieee.org](http://ieeexplore.ieee.org)
* [arxiv.org](http://arxiv.org)

The command line tool will directly download the paper with a *clean filename*.

The server provide RESTful APIs to query papers,
and a interactive paper reading interface supported by [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX).

## How to Use
To run the command line tool, you'll need the following installed:
* [requests](http://docs.python-requests.org/en/latest/)
* [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [termcolor](https://pypi.python.org/pypi/termcolor)

Usage:
```bash
./paper-downloadr.py -t "Distinctive image features from scale-invariant keypoints" -d /tmp
```

To deploy the server, you'll need python2 with virtualenv. And then run the following command:

	cd manage
	./quickinstall

