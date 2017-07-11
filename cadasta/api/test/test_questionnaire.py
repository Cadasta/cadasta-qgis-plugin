# coding=utf-8

"""Tests for questionnare api.
"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/12/16'

import unittest

from mock.mock import MagicMock
from mock import patch
from cadasta.api.questionnaire import GetQuestionnaire


class QuestionnaireTest(unittest.TestCase):
    """Test questionnaire api works."""

    test_questionnare = {
        "id": "vqd89i65ed2u7yng5jbexhhr",
        "filename": "jmbibndu9khbsybnnrq8eyjr",
        "title": "StandardCadastaQuestionnaire",
        "id_string": "StandardCadastaQuestionnaire",
        "version": 2016102523562545,
        "questions": [],
        "question_groups": [],
        "md5_hash": "9022d5df877e743a6afc44e1da28e624"
    }

    def setUp(self):
        """Runs before each test."""

    def tearDown(self):
        """Runs after each test."""

    @patch("cadasta.api.questionnaire.GetQuestionnaire.__init__")
    def test_get_questionnaire(self, mock_init):
        """Test get questionnaire."""
        mock_init.return_value = None
        self.questionnaire_api = GetQuestionnaire()
        self.questionnaire_api.get_json_results = MagicMock(
            return_value=(True, self.test_questionnare)
        )
        results = self.questionnaire_api.get_json_results()
        self.assertTrue(results[0])
        self.assertIsInstance(results[1], dict)


if __name__ == "__main__":
    suite = unittest.makeSuite(QuestionnaireTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
