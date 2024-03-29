# coding: utf-8

"""
    The Model API

    API to access the Virtual Satellite data model  # noqa: E501

    OpenAPI spec version: v0.0.1

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from plugins.VirtualSatelliteRestPlugin.generated_api.v0_0_1.swagger_client.configuration import Configuration


class BeanUnitPrefixed(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'prefix_bean': 'BeanPrefix'
    }

    attribute_map = {
        'prefix_bean': 'prefixBean'
    }

    def __init__(self, prefix_bean=None, _configuration=None):  # noqa: E501
        """BeanUnitPrefixed - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._prefix_bean = None
        self.discriminator = None

        self.prefix_bean = prefix_bean

    @property
    def prefix_bean(self):
        """Gets the prefix_bean of this BeanUnitPrefixed.  # noqa: E501


        :return: The prefix_bean of this BeanUnitPrefixed.  # noqa: E501
        :rtype: BeanPrefix
        """
        return self._prefix_bean

    @prefix_bean.setter
    def prefix_bean(self, prefix_bean):
        """Sets the prefix_bean of this BeanUnitPrefixed.


        :param prefix_bean: The prefix_bean of this BeanUnitPrefixed.  # noqa: E501
        :type: BeanPrefix
        """
        if self._configuration.client_side_validation and prefix_bean is None:
            raise ValueError("Invalid value for `prefix_bean`, must not be `None`")  # noqa: E501

        self._prefix_bean = prefix_bean

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(BeanUnitPrefixed, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BeanUnitPrefixed):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BeanUnitPrefixed):
            return True

        return self.to_dict() != other.to_dict()
