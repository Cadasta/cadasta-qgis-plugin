# coding=utf-8
"""Cadasta license about."""

from cadasta.utilities.i18n import tr
from extras import messaging as m
from extras.messaging import styles

INFO_STYLE = styles.INFO_STYLE

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '03/01/17'


def overview():
    """License about for Cadasta.

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
    message = m.Heading(tr('QGIS Cadasta plugin'), **INFO_STYLE)
    return message


def content():
    """Helper method that returns just the content.

    This method was added so that the text could be reused in the
    other contexts.

    :returns: A message object without brand element.
    :rtype: safe.messaging.message.Message
    """
    message = m.Message()
    message.add(m.Paragraph(tr(
        'The plugin integrates with the cadasta.org platform'
    )))
    message.add(m.Paragraph(tr(
        'developed by kartoza.com'
    )))
    return message
