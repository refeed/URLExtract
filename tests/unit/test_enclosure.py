#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. Licence MIT
.. codeauthor:: Jan Lipovský <janlipovsky@gmail.com>, janlipovsky.cz
"""
import pytest

from urlextract import URLExtract


@pytest.fixture(scope="module")
def urlextract():
    return URLExtract()


@pytest.mark.parametrize("text, expected", [

    ("a(sa\"enclosure.net/bracketext\"as)asd",
     ['enclosure.net/bracketext']),
    ("<email@address.net>",
     ['email@address.net']),
    ("`https://coala.io/200`",
     ['https://coala.io/200']),
    ("(enclosure.net/bracket)",
     ['enclosure.net/bracket']),
    ("{enclosure.net/curly}",
     ['enclosure.net/curly']),
    ("[enclosure.net/square]",
     ['enclosure.net/square']),
    ("\"enclosure.net/dqoute\"",
     ['enclosure.net/dqoute']),
    ("\\enclosure.net/slash\\",
     ['enclosure.net/slash']),
    ("'enclosure.net/qoute'",
     ['enclosure.net/qoute']),
    ("asd(enclosure.net/bracketext)asd",
     ['enclosure.net/bracketext']),
    ("Foo (http://de.wikipedia.org/wiki/Agilit%C3%A4t_(Management)) Bar",
     ["http://de.wikipedia.org/wiki/Agilit%C3%A4t_(Management)"]),
    ("asd(http://de.wikipedia.org/wiki/(Agilit%C3(%A4t_(Manag)ement))) Bar",
     ["http://de.wikipedia.org/wiki/(Agilit%C3(%A4t_(Manag)ement))"]),
    ("asd(enclosure.net/rbracketless",
     ['enclosure.net/rbracketless']),
    ("asd)enclosure.net/lbracketless",
     ['enclosure.net/lbracketless']),
    ("asd{enclosure.net",
     ['enclosure.net']),
    ("asd}enclosure.net",
     ['enclosure.net']),
    ("asd[enclosure.net",
     ['enclosure.net']),
    ("asd]enclosure.net",
     ['enclosure.net']),


])
def test_find_urls(urlextract, text, expected):
    """
    Testing find_urls returning all URLs

    :param fixture urlextract: fixture holding URLExtract object
    :param str text: text in which we should find links
    :param list(str) expected: list of URLs that has to be found in text
    """
    assert expected == urlextract.find_urls(text)


def test_get_enclosures(urlextract):
    assert urlextract._enclosure == urlextract.get_enclosures()


def test_add_enclosure(urlextract):

    old_enclosure = urlextract.get_enclosures().copy()
    old_enclosure.add(("%", "%"))
    urlextract.add_enclosure("%", "%")

    assert old_enclosure == urlextract.get_enclosures()

    with pytest.raises(AssertionError):
        urlextract.remove_enclosure("aa", "ss")

    with pytest.raises(AssertionError):
        urlextract.remove_enclosure("", "")


def test_remove_enclosure(urlextract):
    old_enclosure = urlextract.get_enclosures().copy()
    old_enclosure.remove(("%", "%"))
    urlextract.remove_enclosure("%", "%")

    assert old_enclosure == urlextract.get_enclosures()

    with pytest.raises(AssertionError):
        urlextract.remove_enclosure("asd", "dddsa")

    with pytest.raises(AssertionError):
        urlextract.remove_enclosure("", "")
