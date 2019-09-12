from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
import unittest

from projectinfo import ProjectInfo, Resource

EXPECTED_APPKEY_FILE = """#pragma once
#include <stdint.h>

extern uint32_t MESSAGE_KEY_ANOTHER_KEY;
extern uint32_t MESSAGE_KEY_AWESOME_KEY;
extern uint32_t MESSAGE_KEY_TEST_KEY;
"""

EXPECTED_RESOURCES_FILE = """#pragma once

#define RESOURCE_ID_CAT_BLACK 1
#define RESOURCE_ID_CAT_WHITE 2
#define RESOURCE_ID_ZEBRA 3
"""


class TestAppkeysHeader(unittest.TestCase):
    def test_no_appmessage_keys(self):
        info = ProjectInfo(messagekeys=[])
        file = info.make_messagekey_header()
        self.assertEqual(file, '#pragma once\n#include <stdint.h>\n\n')

    def test_with_own_keys(self):
        info = ProjectInfo(messagekeys=['another_key', 'awesome_key', 'TEST_KEY'])
        file = info.make_messagekey_header()
        self.assertEqual(file, EXPECTED_APPKEY_FILE)

    def test_with_own_and_library_keys(self):
        info = ProjectInfo(messagekeys=['another_key', 'TEST_KEY'], lib_messagekeys=['test_key', 'awesome_key'])
        file = info.make_messagekey_header()
        self.assertEqual(file, EXPECTED_APPKEY_FILE)


class TestResourcesHeader(unittest.TestCase):
    def test_no_resources(self):
        info = ProjectInfo(resources=[])
        file = info.make_resource_ids_header()
        self.assertEqual(file, '#pragma once\n\n')

    def test_with_own_keys(self):
        info = ProjectInfo(resources=[Resource('png-trans', 'CAT'), Resource('bitmap', 'ZEBRA')])
        file = info.make_resource_ids_header()
        self.assertEqual(file, EXPECTED_RESOURCES_FILE)

    def test_with_own_and_library_keys(self):
        info = ProjectInfo(resources=[Resource('png-trans', 'CAT')], lib_resources=[Resource('bitmap', 'ZEBRA')])
        file = info.make_resource_ids_header()
        self.assertEqual(file, EXPECTED_RESOURCES_FILE)
