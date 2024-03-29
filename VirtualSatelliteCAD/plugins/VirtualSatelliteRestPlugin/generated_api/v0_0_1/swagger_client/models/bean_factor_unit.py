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


class BeanFactorUnit(object):
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
        'uuid': 'str',
        'unit_bean': 'ABeanUnit',
        'exponent': 'float'
    }

    attribute_map = {
        'uuid': 'uuid',
        'unit_bean': 'unitBean',
        'exponent': 'exponent'
    }

    def __init__(self, uuid=None, unit_bean=None, exponent=None, _configuration=None):  # noqa: E501
        """BeanFactorUnit - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._uuid = None
        self._unit_bean = None
        self._exponent = None
        self.discriminator = None

        self.uuid = uuid
        self.unit_bean = unit_bean
        self.exponent = exponent

    @property
    def uuid(self):
        """Gets the uuid of this BeanFactorUnit.  # noqa: E501

        Unique identifier for a bean  # noqa: E501

        :return: The uuid of this BeanFactorUnit.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this BeanFactorUnit.

        Unique identifier for a bean  # noqa: E501

        :param uuid: The uuid of this BeanFactorUnit.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and uuid is None:
            raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501

        self._uuid = uuid

    @property
    def unit_bean(self):
        """Gets the unit_bean of this BeanFactorUnit.  # noqa: E501


        :return: The unit_bean of this BeanFactorUnit.  # noqa: E501
        :rtype: ABeanUnit
        """
        return self._unit_bean

    @unit_bean.setter
    def unit_bean(self, unit_bean):
        """Sets the unit_bean of this BeanFactorUnit.


        :param unit_bean: The unit_bean of this BeanFactorUnit.  # noqa: E501
        :type: ABeanUnit
        """
        if self._configuration.client_side_validation and unit_bean is None:
            raise ValueError("Invalid value for `unit_bean`, must not be `None`")  # noqa: E501

        self._unit_bean = unit_bean

    @property
    def exponent(self):
        """Gets the exponent of this BeanFactorUnit.  # noqa: E501


        :return: The exponent of this BeanFactorUnit.  # noqa: E501
        :rtype: float
        """
        return self._exponent

    @exponent.setter
    def exponent(self, exponent):
        """Sets the exponent of this BeanFactorUnit.


        :param exponent: The exponent of this BeanFactorUnit.  # noqa: E501
        :type: float
        """
        if self._configuration.client_side_validation and exponent is None:
            raise ValueError("Invalid value for `exponent`, must not be `None`")  # noqa: E501

        self._exponent = exponent

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
        if issubclass(BeanFactorUnit, dict):
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
        if not isinstance(other, BeanFactorUnit):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BeanFactorUnit):
            return True

        return self.to_dict() != other.to_dict()
