# coding=utf-8
"""Help for create download."""

from cadasta.utilities.i18n import tr
from extras import messaging as m
from extras.messaging import styles

INFO_STYLE = styles.INFO_STYLE

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '03/01/17'


def create_project_help():
    """Help message for Create Project.

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
    message = m.Heading(tr('Create Project Help'), **INFO_STYLE)
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
        'Create Project is one of main wizard that will help you to create'
        'project in qgis and update it to Cadasta with easy steps.')))

    message.add(m.Paragraph(tr('There are 3 step in this wizard.')))
    message.add(m.ImportantText(tr('1. Project Definition.')))

    message.add(m.Paragraph(tr(
        'This step will provide you \'get available organisation\' button. '
        'This button will get available organisation from cadasta and show '
        'it in list, in the left of button. Selecting organisation is '
        'required.')))

    message.add(m.Paragraph(tr(
        'There are 3 another required field, which are :')))

    bullets = m.BulletedList()
    bullets.add(m.Text(
        m.ImportantText(tr('Project Name')),
        tr('- it is name for new project')
    ))
    bullets.add(m.Text(
        m.ImportantText(tr('Project Url')),
        tr('- it is url for new project')
    ))
    bullets.add(m.Text(
        m.ImportantText(tr('Layer to upload')),
        tr('- select the layer that was created.')
    ))
    message.add(bullets)
    return message
