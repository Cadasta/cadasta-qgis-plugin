# coding=utf-8
"""Help for project download."""

from cadasta.utilities.i18n import tr
from extras import messaging as m
from extras.messaging import styles

INFO_STYLE = styles.INFO_STYLE

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '03/01/17'


def download_project_help():
    """Help message for Download Project.

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
    message = m.Heading(tr('Download Project Help'), **INFO_STYLE)
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
        'Download Project is one of main wizard that will help you to get '
        'data from Cadasta. With easy step, you will get data from Cadasta, '
        'and show it to QGIS.')))

    message.add(m.Paragraph(tr('There are 2 step in this wizard.')))
    message.add(m.ImportantText(tr('1. Get project step.')))

    message.add(m.Paragraph(tr(
        'This step will provide you \'get available project\' button. '
        'This button will get available project from Cadasta and show '
        'the result in list, in the left of button.')))

    message.add(m.Paragraph(tr(
        'On the buttom of list, there will be a description of project, '
        'and change everytime the project is selected in list.')))

    message.add(m.Paragraph(tr(
        'After a project is selected, button \'next\' will be enabled. '
        'Push \'next\' button and step 2 will be shown.')))

    message.add(m.ImportantText(tr('2. Download Progress Step.')))

    message.add(m.Paragraph(tr(
        'This step will automatically download project that selected in '
        'previous step, and show download progress. After it is done, '
        'project will be show on QGIS and wizard can be closed.')))
    return message
