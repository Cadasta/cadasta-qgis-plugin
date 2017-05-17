# -*- coding: utf-8 -*-
"""
Cadasta project - **Setting utilities**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import os
import logging
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import QSettings
from cadasta.utilities.resources import resources_path
from cadasta.utilities.resources import (
    resources_path,
    resource_url,
    get_project_path
)

LOGGER = logging.getLogger('CadastaQGISPlugin')

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '20/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

app_name = 'cadasta'
default_domain = 'https://platform-staging-api.cadasta.org/'


def set_setting(key, value):
    """ Set value to QSettings based on key.

    :param key: unique key for setting.
    :type key: QString

    :param value: value to be saved.
    :type value: QVariant

    """
    settings = QSettings()
    settings.setValue('%s/%s' % (app_name, key), value)


def delete_setting(key):
    """ Delete setting from QSettings.

    :param key: unique key for setting.
    :type key: QString

    """
    settings = QSettings()
    settings.remove('%s/%s' % (app_name, key))


def get_setting(key):
    """ Get setting from QSettings.

    This function will get setting from QSettings based on key param.
    If it is not saved before, it will return None instead.

    :param key: unique key for setting
    :type key: QString

    :return: value that saved in setting with unique key.
    :rtype: QVariant.
    """
    settings = QSettings()
    return settings.value('%s/%s' % (app_name, key), None)


def save_url_instance(url):
    """ Save url to QSettings.

    This need to be called on options ui when save the url instance.

    :param url: url instance that will saved
    :type url: QString

    """
    set_setting("url", url)


def get_url_instance():
    """ Get url instance from QSettings.

    This function will return url instance that saved fom QSetting.
    If url is not saved before, it will return default url.

    :return: url instance that saved.
    :rtype: QVariant
    """
    url = get_setting("url")
    if not url:
        url = default_domain
    return url.rstrip('/')


def delete_url_instance():
    """ Delete url instance from QSettings."""
    delete_setting("url")


def save_authtoken(authtoken):
    """ Save authtoken to QSettings.

    :param authtoken: authtoken that will saved
    :type authtoken: QString

    """
    set_setting("user/authtoken", authtoken)


def get_authtoken():
    """ Get authtoken from QSettings.

    :return: authtoken that saved
    :rtype: QVariant
    """
    return get_setting("user/authtoken")


def delete_authtoken():
    """ Delete authtoken from QSettings."""
    delete_setting("user/authtoken")
    delete_setting("user/organizations")


def save_user_organizations(organizations):
    """ Save user organizations to QSettings.

    :param organizations: organizations of user
    :type organizations: list

    """
    set_setting("user/organizations", ';'.join(organizations))


def get_user_organizations():
    """ Get user organizations from QSettings.

    :return: organizations of user
    :rtype: list
    """
    if get_setting("user/organizations"):
        return get_setting("user/organizations").split(';')
    else:
        return []


def get_path_data(organization_slug=None, project_slug=None):
    """ Path data based on organization and project slug.

    :param organization_slug: organization slug for the data location
    :type organization_slug: str

    :param project_slug: project slug for filename
    :type project_slug: str

    :return: Absoulte data path
    :rtype: str
    """
    data_path = get_project_path()
    data_path = os.path.join(
        data_path,
        'data'
    )
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if organization_slug:
        data_path = os.path.join(
            data_path,
            organization_slug
        )
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    if project_slug:
        data_path = os.path.join(
            data_path,
            '%s' % project_slug
        )
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path


def get_csv_path(organization_slug=None, project_slug=None, attribute=None):
    """ Path for csv file

    :param organization_slug: organization slug for the data location
    :type organization_slug: str

    :param project_slug: project slug for filename
    :type project_slug: str

    :param attribute: additional csv name
    :type attribute: str

    :return: Absoulte data path
    :rtype: str
    """
    data_path = get_path_data(
        organization_slug=organization_slug,
        project_slug=project_slug
    )

    if data_path:
        data_path = os.path.join(
            data_path,
            '%s.csv' % attribute
        )
    return data_path


def get_path_database(database=None):
    """Path databased based on database.

    :param database: database for the data location
    :type database: str

    :return: Absoulte database path
    :rtype: str
    """
    data_path = get_project_path()
    data_path = os.path.join(
        data_path,
        'database',
        'db'
    )
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if database:
        data_path = os.path.join(
            data_path,
            database
        )
    return data_path


def logo_element():
    """Create a sanitised local url to the logo for insertion into html.

    :returns: A sanitised local url to the logo.
    :rtype: str
    """
    path = os.path.join(
            resources_path(),
            'images',
            'cadasta-logo-transparent.png')

    if os.name == 'nt':
        path = 'file:///' + path

    url = QUrl(path)
    path = url.toLocalFile()
    return path
