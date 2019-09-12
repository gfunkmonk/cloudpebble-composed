"""
Tests in this file can be run with run_tests.py
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()
from builtins import *
from django.test import TestCase
import ide.git


class UrlToReposTest(TestCase):
    def test_basic_url_to_repo(self):
        """
        Tests that a simple repo url is correctly recognized.
        """
        username, reponame = ide.git.url_to_repo("https://github.com/pebble/cloudpebble")
        self.assertEqual("pebble", username)
        self.assertEqual("cloudpebble", reponame)

    def test_strange_url_to_repo(self):
        """
        Tests that a non-standard repo url is correctly recognized.
        """
        username, reponame = ide.git.url_to_repo("git://github.com:foo/bar.git")
        self.assertEqual("foo", username)
        self.assertEqual("bar", reponame)

    def test_bad_url_to_repo(self):
        """
        Tests that a entirely different url returns None.
        """
        self.assertEqual(None, ide.git.url_to_repo("http://www.cuteoverload.com"))
