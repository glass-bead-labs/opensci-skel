opensci-skel
============

A skeleton for setting up an open science project with restricted-use data. If
possible, we should also use de-identified data. But we still minimizing
disclosure in any case.

Moderately exotic technologies
------------------------------

### `.gitignore`

Open-ended / exploratory work that may contain data disclosures, such as
interactive explorations in IPython notebooks, should be done in the `dmz`
folder, which is `.gitignore`d. More uses of `.gitignore` are detailed below.

### Git Annex

All committed / sync'd data should be kept in [git
annex](https://git-annex.branchable.com/), to allow free sharing of code and
results without disclosing data.

You'll note that the `raw-data/` folder is `gitignore`d to help prevent
accidentally pushing data to a public repo.

### Dexy

We manage our reports with [Dexy](http://dexy.it). To prepare a fresh checkout
of this repository, first run `dexy setup` in the root folder. Then, `dexy`
will regenerate the `output` folder.

Note that Dexy still lacks Python 2.x support (it wouldn't actually be that
hard to add). I recommend having a dedicated
[conda](http://conda.pydata.org/docs/using/envs.html) environment for your Dexy
install (or perhaps a Docker container).  You can usually use
[virtualenv](https://virtualenv.pypa.io/en/latest/) instead of conda, but this
[has problems with batch mode for matplotlib]().

There are some Dexy-specific things that are currently `.gitignore`d - see the
comments in that file.

### Standards-compliant web content

Dexy output will end up in the `output` folder for now. This directory *is*
managed by git, and can be zipped and sent to less technical partners. Thus, it
should contain only things that make sense from the perspective of a web
browser (including perhaps PDFs and similar).
