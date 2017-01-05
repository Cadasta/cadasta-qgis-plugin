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
        'Cadasta QGIS Plugin is a tool to publish and retrieve projects and '
        'data from Cadasta in QGIS. It will help you with easy wizard '
        'to create, download or update Cadasta project.')))
    message.add(m.Paragraph(tr(
        'There are 3 main wizard that will help you '
        'to manage your project.')))

    bullets = m.BulletedList()
    bullets.add(m.Text(
        m.ImportantText(tr('Download Project'))))
    bullets.add(m.Text(
        m.ImportantText(tr('Create Project'))))
    bullets.add(m.Text(
        m.ImportantText(tr('Update Project'))))
    message.add(bullets)

    message.add(m.Paragraph(tr(
        'There are also others dialog that will help you to manaage '
        'cadasta project. They are :')))
    bullets = m.BulletedList()
    bullets.add(m.Text(
        m.ImportantText(tr('Options')),
        tr(
            '- Define your instance url, to be used as default for Cadasta.'
            'And also, define username that will be used for create '
            'and update project.')
    ))
    bullets.add(m.Text(
        m.ImportantText(tr('Contact')),
        tr(
            '- It help you to save contact that will be used for projects '
            'creation.'
        )
    ))
    message.add(bullets)
    return message
