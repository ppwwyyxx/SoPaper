## SoPaper, So Easy
This is a project designed for researchers to conveniently getting papers they need.

It includes a command line tool ``paper-downloader.py``, to automatically search and download paper,
as well as a server to provide integrated search/read/download experience.

This project served as a course project for *Service Oriented Software Engineering(2014Spring)*
and *Search Engine Technology(2014Spring)*, developed by:
* [Yuxin Wu (ppwwyyxx)](mailto:ppwwyyxxc@gmail.com)
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

The command line tool will directly download the paper with a __clean filename__.

The server provide:
* RESTful APIs on papers
* Interactive paper reading UI supported by [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX)

## How to Use
To run the command line tool, you'll need the following installed:
* [requests](http://docs.python-requests.org/en/latest/)
* [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [termcolor](https://pypi.python.org/pypi/termcolor)

Usage:
```bash
./paper-downloader.py -t "Distinctive image features from scale-invariant keypoints" -d /tmp
```

To deploy the server, you'll need:
* Python2 with virtualenv. Python headers are needed (python-dev on debian/ubuntu).
* ghostscript
* libcurl (libcurl4-{openssl,nss,gnutls}-dev on debian/ubuntu)
* xapian (libxapian-dev & python2-xapian on debian/ubuntu)
* pdf2htmlEx installed. See its [download guide](https://github.com/coolwanglu/pdf2htmlEX/wiki/Download)
* poppler-utils which provide the 'pdftotext' command line util

Note: on debian/ubuntu, make sure you do *not* have 'python2-bson' package installed.

Run the following command to install all the python packages needed, and setup virtualenv

	cd manage
	./quickinstall

