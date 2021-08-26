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


class BeanDiscipline(object):
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
        'user': 'str',
        'name': 'str'
    }

    attribute_map = {
        'uuid': 'uuid',
        'user': 'user',
        'name': 'name'
    }

    def __init__(self, uuid=None, user=None, name=None, _configuration=None):  # noqa: E501
        """BeanDiscipline - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._uuid = None
        self._user = None
        self._name = None
        self.discriminator = None

        self.uuid = uuid
        self.user = user
        self.name = name

    @property
    def uuid(self):
        """Gets the uuid of this BeanDiscipline.  # noqa: E501

        Unique identifier for a bean  # noqa: E501

        :return: The uuid of this BeanDiscipline.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this BeanDiscipline.

        Unique identifier for a bean  # noqa: E501

        :param uuid: The uuid of this BeanDiscipline.  # noqa: E501
        :type: str
        """
        # if self._configuration.client_side_validation and uuid is None:
        #     raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501

        self._uuid = uuid

    @property
    def user(self):
        """Gets the user of this BeanDiscipline.  # noqa: E501

        Name of the user assigned to the discipline  # noqa: E501

        :return: The user of this BeanDiscipline.  # noqa: E501
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this BeanDiscipline.

        Name of the user assigned to the discipline  # noqa: E501

        :param user: The user of this BeanDiscipline.  # noqa: E501
        :type: str
        """
        # if self._configuration.client_side_validation and user is None:
        #     raise ValueError("Invalid value for `user`, must not be `None`")  # noqa: E501

        self._user = user

    @property
    def name(self):
        """Gets the name of this BeanDiscipline.  # noqa: E501

        Name of the discipline  # noqa: E501

        :return: The name of this BeanDiscipline.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this BeanDiscipline.

        Name of the discipline  # noqa: E501

        :param name: The name of this BeanDiscipline.  # noqa: E501
        :type: str
        """
        # if self._configuration.client_side_validation and name is None:
        #     raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

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
        if issubclass(BeanDiscipline, dict):
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
        if not isinstance(other, BeanDiscipline):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BeanDiscipline):
            return True

        return self.to_dict() != other.to_dict()
