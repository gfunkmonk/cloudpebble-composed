""" These tests check that the Project model behaves as expected."""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from ide.models import Project
from django.test import TestCase


class TestProjectModel(TestCase):
    def test_uses_array_message_keys_property(self):
        """ Check that uses_array_message_keys functions as intended """
        self.assertTrue(Project(app_keys="[]").uses_array_message_keys)
        self.assertFalse(Project(app_keys="{}").uses_array_message_keys)
