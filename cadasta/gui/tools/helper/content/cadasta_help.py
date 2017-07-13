# coding=utf-8
"""Cadasta main helper."""

from cadasta.utilities.i18n import tr
from extras import messaging as m
from extras.messaging import styles

INFO_STYLE = styles.INFO_STYLE

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '03/01/17'


def cadasta_help():
    """Help message for Cadasta.

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
    message = m.Heading(tr('Cadasta Help'), **INFO_STYLE)
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
        'The Cadasta QGIS Plugin is a tool for retrieving, editing and publishing '
        'You can find updated documentation and suggested workflows on our main '
        'documentation pages: <a href="https://docs.cadasta.org/en/11-qgis-plugin.html">QGIS chapter</a> ')))
    message.add(m.Paragraph(tr(
        'There are three windows that will help you '
        'to manage your project\'s data.')))

    bullets = m.BulletedList()
    bullets.add(m.Text(
        m.ImportantText(tr('Download Project'))))
    bullets.add(m.Text(
        m.ImportantText(tr('Create Project'))))
    bullets.add(m.Text(
        m.ImportantText(tr('Update Project'))))
    message.add(bullets)

    message.add(m.Paragraph(tr(
        'Use the "User Settings" window to log in to your account and get started!'
        '')))
    return message
