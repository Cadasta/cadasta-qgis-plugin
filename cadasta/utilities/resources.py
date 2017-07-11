# coding=utf-8
"""This module contains utilities for locating application resources (img etc).
"""
import os
import re
import codecs

# This import is to enable SIP API V2
# noinspection PyUnresolvedReferences
import qgis  # pylint: disable=unused-import
from qgis.PyQt import QtCore, uic


def html_footer():
    """Get a standard html footer for wrapping content in.

    :returns: A header containing a web page closing content in html - up to
        and including the body close tag.
    :rtype: str
    """
    file_path = os.path.join(resources_path(), 'footer.html')
    with file(file_path) as header_file:
        content = header_file.read()
    return content


def html_header():
    """Get a standard html header for wrapping content in.

    :returns: A header containing a web page preamble in html - up to and
        including the body open tag.
    :rtype: str
    """
    file_path = os.path.join(resources_path(), 'header.html')

    with codecs.open(file_path, 'r', encoding='utf8') as header_file:
        content = header_file.read()
        content = content.replace('PATH', resources_path())
    return content


def resources_path(*args):
    """Get the path to our resources folder.

    .. versionadded:: 3.0

    Note that in version 3.0 we removed the use of Qt Resource files in
    favour of directly accessing on-disk resources.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: list

    :return: Absolute path to the resources folder.
    :rtype: str
    """
    path = os.path.dirname(__file__)
    path = os.path.abspath(
        os.path.join(path, os.path.pardir, os.path.pardir, 'resources'))
    for item in args:
        path = os.path.abspath(os.path.join(path, item))

    return path


def resource_url(path):
    """Get the a local filesystem url to a given resource.

    .. versionadded:: 3.0

    Note that in version 3.0 we removed the use of Qt Resource files in
    favour of directly accessing on-disk resources.

    :param path: Path to resource e.g. /home/timlinux/foo/bar.png
    :type path: str

    :return: A valid file url e.g. file:///home/timlinux/foo/bar.png
    :rtype: str
    """
    url = QtCore.QUrl.fromLocalFile(path)
    return str(url.toString())


def is_valid_url(url):
    """
    Check if url is valid

    :param url: Url to be checked
    :return: bool
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
        r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(url) is not None


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.

    :param ui_file: The file of the ui in safe.gui.ui
    :type ui_file: str
    """
    ui_file_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'gui',
            'ui',
            ui_file
        )
    )
    return uic.loadUiType(ui_file_path)[0]


def get_project_path():
    """
    Get absolute project path
    :rtype: basetring
    :return absolute project path
    """
    project_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir
        )
    )
    return project_path


def get_license_path():
    """Get absolute license file path.

    :rtype: basetring
    :return absolute license path
    """
    project_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'LICENSE.txt'
        )
    )
    return project_path


def get_about_path():
    """Get about file path.
    
    :rtype: basestring
    :return absolute about path
    """
    about_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'ABOUT.txt'
        )
    )
    return about_path


def get_metadata_path():
    """Get absolute metadata file path.

    :rtype: basetring
    :return absolute metadata path
    """
    project_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'metadata.txt'
        )
    )
    return project_path


def get_plugin_version():
    """Get plugin version from metadata.

    :rtype: basetring
    :return absolute metadata path
    """
    # get version
    with open(get_metadata_path()) as metadata_file:
        contents = metadata_file.readlines()
    version = ''
    for content in contents:
        content = content.replace('\n', '')
        if 'version=' in content:
            version = content.split('=')[1]
            break
    return version
