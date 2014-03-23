## Automatically search and download paper

This script will search and analyse results in:
* Google Scholar
* Google

and support downloading pdf from:

* direct pdf link
* [dl.acm.org](http://dl.acm.org/)
* [ieeexplore.ieee.org](http://ieeexplore.ieee.org)
* [arxiv.org](http://arxiv.org)

using:

* [requests](http://docs.python-requests.org/en/latest/)
* wget

## Dependencies
* [requests](http://docs.python-requests.org/en/latest/)
* [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)


## Usage
```bash
./paper-downloadr.py -t "Distinctive image features from scale-invariant keypoints" -d /tmp
```
