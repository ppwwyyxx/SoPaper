## SoPaper, So Easy

## Dependency

  + Python2 with virtualenv

## Installation

In Linux, make sure you have python2 and virtualenv in ``PATH``, then run the following command:

	cd manage
	./quickinstall

*Notice* If you are using Windows, try running Linux-based operating system in a virtual machine.

## Run

Remember to put soa.pth on .env/lib/python2.7/site-packages.

then


# Website Infrastructure
We use ``Flask`` as WGSI server, and ``jinja2`` html template engine.
An important aspect is that the way we provide RESTful APIs

# Modules
The website is decoupled into several modules:

  + common: tools & configurations
  ++ lib: global utils
  + manage: scripts that help better manage the development
  + webapi: RESTful apis


# Test
If you are not familiar with python unittest, please read through [http://docs.python.org/2/library/unittest.html](http://docs.python.org/2/library/unittest.html)
to understand basic concepts and practices.
