## SoPaper, So Easy
This is a project designed for researchers to conveniently access papers they need.

The command line tool ``sopaper`` can __automatically search and download__ paper
from Internet, given the title.
The downloaded paper will thus have a readable file name
(I wrote it at the beginning because I'm tired of seeing the file name being random strings).
It mainly supports searching papers in computer science.

<!-- -This project also comes with a naive server to provide integrated search/read/download experience.  -->

## How to Use
Install command line dependencies:
* [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) command line executable.
	+ Using pdftk on OSX10.11 might lead to hangs. See [here](http://stackoverflow.com/questions/32505951/pdftk-server-on-os-x-10-11) for more info.
* poppler-utils (optional)

Install python package:
``pip install --user sopaper``

Usage:
```bash
$ sopaper --help
$ sopaper "Distinctive image features from scale-invariant keypoints"
$ sopaper "https://arxiv.org/abs/1606.06160"
```
NOTE: If you are not in school, you may need proxy by environment variable `http_proxy` and `https_proxy`,
to be able to download from certain sites (such as 'dl.acm.org').

## Features
The ``searcher`` module will fuzzy search and analyse results in
* Google Scholar
* Google

and the ``fetcher`` module will further analyse the results and download papers from the following possible sources:
* direct pdf link
* [dl.acm.org](http://dl.acm.org/)
* [ieeexplore.ieee.org](http://ieeexplore.ieee.org)
* [arxiv.org](http://arxiv.org)

``Searcher`` and ``Fetcher`` are __extensible__ to support more websites.

The command line tool will directly download the paper with a __clean filename__.
All downloaded paper will be __compressed__ using `ps2pdf` from poppler-utils, if available.

<!--
   -The server provide:
   -* RESTful APIs on papers
   -* Interactive paper reading UI supported by [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX)
   -
   -Command line tool is sufficient to use. If you'd like to play with the server, you'll need:
   -* Python2 with virtualenv. Python headers are needed (python-dev on debian/ubuntu).
   -* ghostscript
   -* libcurl (libcurl4-{openssl,nss,gnutls}-dev on debian/ubuntu)
   -* xapian (libxapian-dev & python2-xapian on debian/ubuntu)
   -* pdf2htmlEx installed. See its [download guide](https://github.com/coolwanglu/pdf2htmlEX/wiki/Download)
   -* poppler-utils which provide the 'pdftotext' command line util
   -
   -Note: if you need to run server on debian/ubuntu, make sure you do *not* have 'python2-bson' package installed.
	 -->

## TODO
* Fetcher dedup: when arxiv abs/pdf apperas both in search results, page would be downloaded twice (maybe add a cache for requests)
* Don't trust arxiv link from google scholar
* Is title correctly updated for dlacm?
* Extract title from bibtex -- more accurate?
* Fetcher for other sites
