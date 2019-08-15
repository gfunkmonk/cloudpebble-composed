import collections
from itertools import chain

Resource = collections.namedtuple('Resource', ('type', 'name'))

RESOURCE_HEADER_NAME = 'build/src/resource_ids.auto.h'
MESSAGEKEY_HEADER_NAME = 'build/src/message_keys.auto.h'


class ProjectInfo(object):
    def __init__(self, messagekeys=None, resources=None, lib_messagekeys=None, lib_resources=None):
        """ Set up the initial data for a ProjectInfo object
        :param messagekeys: An array of messagekey strings belonging to the app
        :param resources: An array of Resource objects/tuples belonging to the app
        :param lib_messagekeys: An array of messagekey strings belonging to dependencies
        :param lib_resources: An array of Resource objects/tuples belonging to dependencies
        """
        self.messagekeys = messagekeys if messagekeys else []
        self.resources = resources if resources else []
        self.lib_messagekeys = lib_messagekeys if lib_messagekeys else []
        self.lib_resources = lib_resources if lib_resources else []

    def get_merged_messagekeys(self):
        return sorted(set(chain(self.messagekeys, self.lib_messagekeys)))

    def make_messagekey_header(self):
        merged_keys = self.get_merged_messagekeys()
        return "#pragma once\n#include <stdint.h>\n\n" + "".join("extern uint32_t MESSAGE_KEY_{};\n".format(k) for k in merged_keys)

    def get_merged_resource_ids(self):
        out = set()
        for kind, resource_id in chain(self.resources, self.lib_resources):
            if kind == 'png-trans':
                out.add("%s_BLACK" % resource_id)
                out.add("%s_WHITE" % resource_id)
            else:
                out.add(resource_id)
        return sorted(out)

    def make_resource_ids_header(self):
        merged_keys = self.get_merged_resource_ids()
        return '#pragma once\n\n' + ''.join('#define RESOURCE_ID_%s %d\n' % (name, i + 1) for i, name in enumerate(merged_keys))
