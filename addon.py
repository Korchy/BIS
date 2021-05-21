# Nikita Akimov
# interplanety@interplanety.org

from distutils.version import StrictVersion
import addon_utils


class Addon:

    _addon_name = 'BIS'
    node_group_first_version = '1.9.0'  # minimum available version

    @classmethod
    def version_equal_or_higher(cls, version_num):
        return StrictVersion(cls.current_version()) >= StrictVersion(version_num)

    @classmethod
    def version_equal_or_less(cls, version_num):
        return StrictVersion(cls.current_version()) <= StrictVersion(version_num)

    @classmethod
    def node_group_version_higher(cls, node_group_version, version_num):
        node_group_version = node_group_version if node_group_version else cls.node_group_first_version
        return StrictVersion(node_group_version) > StrictVersion(version_num)

    @classmethod
    def node_group_version_equal_or_less(cls, node_group_version, version_num):
        node_group_version = node_group_version if node_group_version else cls.node_group_first_version
        return StrictVersion(node_group_version) <= StrictVersion(version_num)

    @classmethod
    def current_version(cls):
        version_tuple = [addon.bl_info['version'] for addon in addon_utils.modules()
                         if addon.bl_info['name'] == cls._addon_name][0]   # (1, 4, 2)
        return '.'.join(map(str, version_tuple))    # '1.4.2'
