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


class ABeanQuantityKind(object):
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
        'symbol': 'str',
        'uuid': 'str',
        'name': 'str'
    }

    attribute_map = {
        'symbol': 'symbol',
        'uuid': 'uuid',
        'name': 'name'
    }

    def __init__(self, symbol=None, uuid=None, name=None, _configuration=None):  # noqa: E501
        """ABeanQuantityKind - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._symbol = None
        self._uuid = None
        self._name = None
        self.discriminator = None

        self.symbol = symbol
        self.uuid = uuid
        self.name = name

    @property
    def symbol(self):
        """Gets the symbol of this ABeanQuantityKind.  # noqa: E501


        :return: The symbol of this ABeanQuantityKind.  # noqa: E501
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this ABeanQuantityKind.


        :param symbol: The symbol of this ABeanQuantityKind.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and symbol is None:
            raise ValueError("Invalid value for `symbol`, must not be `None`")  # noqa: E501

        self._symbol = symbol

    @property
    def uuid(self):
        """Gets the uuid of this ABeanQuantityKind.  # noqa: E501

        Unique identifier for a bean  # noqa: E501

        :return: The uuid of this ABeanQuantityKind.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this ABeanQuantityKind.

        Unique identifier for a bean  # noqa: E501

        :param uuid: The uuid of this ABeanQuantityKind.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and uuid is None:
            raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501

        self._uuid = uuid

    @property
    def name(self):
        """Gets the name of this ABeanQuantityKind.  # noqa: E501


        :return: The name of this ABeanQuantityKind.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ABeanQuantityKind.


        :param name: The name of this ABeanQuantityKind.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

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
        if issubclass(ABeanQuantityKind, dict):
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
        if not isinstance(other, ABeanQuantityKind):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ABeanQuantityKind):
            return True

        return self.to_dict() != other.to_dict()
