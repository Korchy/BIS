# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

# attribute class

# now newer used, can be used for more logic between node.py and bl_types.py

from .bl_types import BlTypes


class Attribute:

    @classmethod
    def to_json(cls, attribute, attribute_name):
        attribute_json = {}
        if isinstance(attribute, (int, float, bool, set, str)):
            # attribute = attribute_json
            attribute_json[attribute_name] = attribute
        else:
            print('complex attr', attribute_name, attribute)
        return attribute_json

    @classmethod
    def from_json(cls, attribute_name, attribute_owner, attribute_json, attachments_path):
        # fill attribute from json
        if isinstance(getattr(attribute_owner, attribute_name), (int, float, bool, set, str)):
            attribute = attribute_json
        else:
            attribute = BlTypes.from_json(
                instance_name=attribute_name,
                instance_owner=attribute_owner,
                instance_json=attribute_json['instance'][attribute_name],
                attachments_path=attachments_path
            )
        return attribute
