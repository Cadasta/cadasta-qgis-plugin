# coding=utf-8
"""Cadasta license about."""

from cadasta.utilities.i18n import tr
from cadasta.utilities.resources import get_about_path
from extras import messaging as m
from extras.messaging import styles

INFO_STYLE = styles.INFO_STYLE

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '04/25/17'


def about():
    """About message.

    :returns: A message object containing helpful information.
    :rtype: messaging.message.Message
    """

    message = m.Message()
    message.add(heading())
    message.add(content())
    return message


def heading():
    """Helper method that returns just the header.

    This method was added so that the text could be reused in the
    other contexts.

    :returns: A heading object.
    :rtype: safe.messaging.heading.Heading
    """
    message = m.Heading(tr('About Cadasta'), **INFO_STYLE)
    return message


def content():
    """Helper method that returns just the content.

    This method was added so that the text could be reused in the
    other contexts.

    :returns: A message object without brand element.
    :rtype: safe.messaging.message.Message
    """
    message = m.Message()

    license = open(get_about_path(), 'r+')
    message.add(m.Text(license.read()))

    return message
