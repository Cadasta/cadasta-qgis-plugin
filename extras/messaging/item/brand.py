"""
InaSAFE Disaster risk assessment tool developed by AusAid - **Paragraph.**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.
"""

__author__ = 'tim@kartoza.com'
__revision__ = '$Format:%H$'
__date__ = '28/05/2013'
__copyright__ = ('Copyright 2015, Australia Indonesia Facility for '
                 'Disaster Reduction')

from text import Text
# TODO: I don't really like importing this here as it breaks the modularity of
# TODO: messaging. TS
from cadasta.utilities.resources import (
    resources_path,
    resource_url)


class Brand(Text):
    """A class to model the cadasta brand.
    """

    def __init__(self, **kwargs):
        """Creates a brand element.

        For HTML, it will insert a div with class 'branding' - use css to
        set the style of that div as you want it.

        We pass the kwargs on to the base class so an exception is raised
        if invalid keywords were passed. See:

        http://stackoverflow.com/questions/13124961/
        how-to-pass-arguments-efficiently-kwargs-in-python
        """
        super(Brand, self).__init__(**kwargs)

    def to_html(self):
        """Render as html.
        """
        uri = resource_url(
            resources_path('images', 'logo_white.png'))
        snippet = (
                      '<div class="branding">'
                      '<img src="%s" title="%s" alt="%s" %s/></div>') % (
                      uri,
                      'Cadasta',
                      'Cadasta',
                      self.html_attributes())
        return snippet

    def to_text(self):
        """Render as plain text.
        """
        return ''

    def to_markdown(self):
        return '# **** Cadasta ****'

    def to_json(self):
        pass
