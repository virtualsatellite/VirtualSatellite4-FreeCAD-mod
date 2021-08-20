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


class BeanPropertyEnum(object):
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
        'unit': 'str',
        'property_type': 'str',
        'value': 'str'
    }

    attribute_map = {
        'unit': 'unit',
        'property_type': 'propertyType',
        'value': 'value'
    }

    def __init__(self, unit=None, property_type=None, value=None, _configuration=None):  # noqa: E501
        """BeanPropertyEnum - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._unit = None
        self._property_type = None
        self._value = None
        self.discriminator = None

        if unit is not None:
            self.unit = unit
        if property_type is not None:
            self.property_type = property_type
        if value is not None:
            self.value = value

    @property
    def unit(self):
        """Gets the unit of this BeanPropertyEnum.  # noqa: E501

        Unit of the enum  # noqa: E501

        :return: The unit of this BeanPropertyEnum.  # noqa: E501
        :rtype: str
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """Sets the unit of this BeanPropertyEnum.

        Unit of the enum  # noqa: E501

        :param unit: The unit of this BeanPropertyEnum.  # noqa: E501
        :type: str
        """

        self._unit = unit

    @property
    def property_type(self):
        """Gets the property_type of this BeanPropertyEnum.  # noqa: E501

        Always returns constant: \"enum\"  # noqa: E501

        :return: The property_type of this BeanPropertyEnum.  # noqa: E501
        :rtype: str
        """
        return self._property_type

    @property_type.setter
    def property_type(self, property_type):
        """Sets the property_type of this BeanPropertyEnum.

        Always returns constant: \"enum\"  # noqa: E501

        :param property_type: The property_type of this BeanPropertyEnum.  # noqa: E501
        :type: str
        """
        allowed_values = ["BOOLEAN", "STRING", "INT", "FLOAT", "ENUM", "RESOURCE", "REFERENCE", "EREFERENCE", "COMPOSED"]  # noqa: E501
        if (self._configuration.client_side_validation and
                property_type not in allowed_values):
            raise ValueError(
                "Invalid value for `property_type` ({0}), must be one of {1}"  # noqa: E501
                .format(property_type, allowed_values)
            )

        self._property_type = property_type

    @property
    def value(self):
        """Gets the value of this BeanPropertyEnum.  # noqa: E501

        Name of an enum  # noqa: E501

        :return: The value of this BeanPropertyEnum.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this BeanPropertyEnum.

        Name of an enum  # noqa: E501

        :param value: The value of this BeanPropertyEnum.  # noqa: E501
        :type: str
        """

        self._value = value

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
        if issubclass(BeanPropertyEnum, dict):
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
        if not isinstance(other, BeanPropertyEnum):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BeanPropertyEnum):
            return True

        return self.to_dict() != other.to_dict()
