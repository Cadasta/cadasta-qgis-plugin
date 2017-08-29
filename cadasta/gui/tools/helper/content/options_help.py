# coding=utf-8
"""Help for options."""

from cadasta.utilities.i18n import tr
from extras import messaging as m
from extras.messaging import styles

INFO_STYLE = styles.INFO_STYLE

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '03/01/17'


def options_help():
    """Help message for Options.

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
    message = m.Heading(tr('Options Help'), **INFO_STYLE)
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
        'Options will help you redefine url of Cadasta that is used as '
        'source. And also it create a credential to be used on submit '
        'new or updated projects.')))

    message.add(m.Paragraph(tr(
        'There are 3 input that all of that are required.')))

    bullets = m.BulletedList()
    bullets.add(m.Text(
        m.ImportantText(tr('Cadasta URL')),

        tr('- overwrite current url as cadasta source.'
           'default is https://platform-staging-api.cadasta.org/')
    ))
    bullets.add(m.Text(
        m.ImportantText(tr('Cadasta Username')),
        tr('- username that will be used for other request, e.g: create '
           'project')
    ))
    bullets.add(m.Text(
        m.ImportantText(tr('Cadasta Password'))

    ))
    message.add(bullets)

    message.add(m.Paragraph(tr(
        'Fill out the form with your username and password. Click \'Connect\' '
        'button '
        'to login. If that is successful click the \'Save\' button to save '
        'the settings.')))
    message.add(m.ImportantText(tr('Note that your password is not saved.')))
    return message
