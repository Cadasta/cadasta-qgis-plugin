# coding=utf-8
"""Tests Pep8."""

import unittest
import os
from subprocess import Popen, PIPE


__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@inasafe.org"
__revision__ = '$Format:%H$'


class TestPep8(unittest.TestCase):
    """Test that the plugin is PEP8 compliant."""

    def test_pep8(self):
        """Test if the code is PEP8 compliant."""

        if os.environ.get('ON_TRAVIS', False):
            root = './'
        else:
            root = '../../'

        command = ['make', 'pep8']
        output = Popen(command, stdout=PIPE, cwd=root).communicate()[0]

        # make pep8 produces some extra lines by default.
        default_number_lines = 7
        lines = len(output.splitlines()) - default_number_lines

        message = 'Hey mate, go back to your keyboard :)'
        self.assertEquals(lines, 0, message)
