#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ome documentation build configuration file, created by
# sphinx-quickstart on Wed Feb 22 20:24:38 2012.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# Append the top level directory of the docs, so we can import from the config dir.
sys.path.insert(0, os.path.abspath('../common'))
from conf import *
sys.path.insert(1, os.path.abspath('../omero'))
import conf_autogen


# -- General configuration -----------------------------------------------------

# General information about the project.
project = u'OMERO'
title = project + u' Documentation'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
if "OMERO_RELEASE" in os.environ and len(os.environ.get('OMERO_RELEASE')) > 0:
    release = os.environ.get('OMERO_RELEASE')
    [majornumber, minornumber, patchnumber] = split_release(release)

    # Define Sphinx version and release variables and development branch
    version = ".".join(str(x) for x in (majornumber, minornumber))

    if patchnumber > 0:
        tags.add('point_release')
    previousversion = get_previous_version(majornumber, minornumber)
else:
    version = 'UNKNOWN'
    previousversion = 'UNKNOWN'
    release = 'UNKNOWN'

rst_prolog = """
.. note:: **This documentation is for the new OMERO 5.1. version.** See the `latest OMERO 5.0.x
    version <http://www.openmicroscopy.org/site/support/omero5.0/>`_ or the
    :legacy_plone:`previous versions <>` page to find documentation for the
    OMERO version you are using if you have not upgraded yet.
"""

rst_epilog += """
.. |OmeroPy| replace:: :doc:`/developers/Python`
.. |OmeroCpp| replace:: :doc:`/developers/Cpp`
.. |OmeroJava| replace:: :doc:`/developers/Java`
.. |OmeroMatlab| replace:: :doc:`/developers/Matlab`
.. |OmeroApi| replace:: :doc:`/developers/Modules/Api`
.. |OmeroWeb| replace:: :doc:`/developers/Web`
.. |OmeroClients| replace:: :doc:`/developers/GettingStarted`
.. |OmeroGrid| replace:: :doc:`/sysadmins/grid`
.. |OmeroSessions| replace:: :doc:`/developers/Server/Sessions`
.. |OmeroModel| replace:: :doc:`/developers/Model`
.. |ExtendingOmero| replace:: :doc:`/developers/Server/ExtendingOmero`
.. |BlitzGateway| replace:: :doc:`/developers/Python`
.. |DevelopingOmeroClients| replace:: :doc:`/developers/GettingStarted/AdvancedClientDevelopment`
.. _Spring: http://spring.io
.. |previousversion| replace:: %s
.. |current_dbver|  replace:: %s
.. |previous_dbver|  replace:: %s
.. |iceversion| replace:: 3.5.1
""" % (previousversion, conf_autogen.current_dbver,
       conf_autogen.previous_dbver)

# OMERO-specific extlinks
omero_extlinks = {
    # Github links
    'source' : (omero_github_root + 'blob/'+ branch + '/%s', ''),
    'sourcedir' : (omero_github_root + 'tree/'+ branch + '/%s', ''),
    'commit' : (omero_github_root + 'commit/%s', ''),
    'omedocs' : (doc_github_root + '%s', ''),
    # API links
    'javadoc' : (downloads_root + '/latest/omero5.1/api/%s', ''),
    'pythondoc' : (downloads_root + '/latest/omero5.1/api/python/%s', ''),
    # Miscellaneous links
    'springdoc' : ('http://docs.spring.io/spring/docs/%s', ''),
    'ivydoc' : ('http://ant.apache.org/ivy/history/2.3.0/%s', ''),
    }
extlinks.update(omero_extlinks)

# Edit on GitHub prefix
edit_on_github_prefix = 'omero'

# -- Options for HTML output ---------------------------------------------------

# Custom sidebar templates, maps document names to template names.
html_sidebars['**'].insert(1, 'globalomerotoc.html')

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path.extend(['themes'])

# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
target = project + '-' + release + '.tex'
latex_documents = [
  (master_doc, target, title, author, 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = 'images/omero-logo.pdf'


# -- Options for the linkcheck builder ----------------------------------------

# Regular expressions that match URIs that should not be checked when doing a linkcheck build
linkcheck_ignore += [r'http://localhost:\d+/?', 'http://localhost/',
    'http://www.hibernate.org',
    r'^https?://www\.openmicroscopy\.org/site/team/.*',
    r'.*[.]?example\.com/.*',
    r'^https://spreadsheets.google.com/.*']
