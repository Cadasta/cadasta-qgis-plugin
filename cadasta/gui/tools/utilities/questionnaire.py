# coding=utf-8
"""
Cadasta Utilities -**Questionnaire**

This module provides: Login : Login for cadasta and save authnetication

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import json
import logging
import re
from qgis.gui import QgsMessageBar
from cadasta.api.questionnaire import GetQuestionnaire, UpdateQuestionnaire
from cadasta.utilities.i18n import tr
from cadasta.utilities.resources import resources_path

__copyright__ = "Copyright 2016, Cadasta"
__license__ = "GPL version 3"
__email__ = "info@kartoza.org"
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('CadastaQGISPlugin')

mapping_type = {
    'string': 'TX',
    'integer': 'IN',
    'double': 'DE',
    'date': 'DA',
    'dateTime': 'DT'
}


class QuestionnaireUtility(object):
    def get_questionnaire_project(
            self, organization_slug, project_slug):
        """Get questionnaire for project.

        :param organization_slug: Organization slug for Questionnaire
        :type organization_slug: Str

        :param project_slug: Project slug for Questionnaire
        :type project_slug: Str

        """
        self.get_questionnaire_api = GetQuestionnaire(
            organization_slug=organization_slug,
            project_slug=project_slug,
            on_finished=self.get_questionnaire_project_finished
        )

    def get_questionnaire_project_finished(self, result):
        """Function when Questionnaire Api finished.

        :param result: result of request
        :type result: (bool, list/dict/str, str, str)
        """
        pass

    def generate_new_questionnaire(self, current_layer, current_questionnaire):
        """Generate new questionnaire.

        Thiw will get current questionnaire of create from default
        questionnaire. Updating it by looking of attributes.

        :param current_layer:layer that for generate questionnaire
        :type current_layer: QgsVectorLayer

        :param current_questionnaire: Questionnaire that found
        :type current_questionnaire: Str

        :return: generated questionnaire
        :rtype: str
        """

        questionnaire_path = resources_path('questionnaire.json')
        # get default questionnaire
        with open(questionnaire_path) as data_file:
            default_questionnaire = json.load(data_file)

        try:
            current_questionnaire = json.dumps(
                json.loads(current_questionnaire)
            )
            current_questionnaire = re.sub(
                r'"id":[ ]?"(.*?)"', "",
                current_questionnaire
            )
            current_questionnaire = re.sub(
                r',[ ]?}', '}',
                current_questionnaire
            )
            current_questionnaire = re.sub(
                r',[ ]?,', ',',
                current_questionnaire
            )
            questionnaire = json.loads(current_questionnaire)
            questionnaire.pop('version', None)
            questionnaire.pop('id_string', None)
            questionnaire.pop('md5_hash', None)
            questionnaire.pop('xls_form', None)
        except ValueError as e:
            default_questionnaire['filename'] = current_layer.name()
            default_questionnaire['title'] = current_layer.name()
            default_questionnaire['id_string'] = current_layer.name()
            questionnaire = default_questionnaire

        # Get current fields
        for field in current_layer.fields():
            found = False
            for question in questionnaire["questions"]:
                if question["name"] == field.name():
                    found = True
            if not found:
                questionnaire["questions"].append(
                    {
                        "name": field.name(),
                        "label": field.name(),
                        "type": mapping_type[field.typeName().lower()],
                        "required": False,
                        "constraint": 'null',
                        "default": 'null',
                        "hint": 'null',
                        "relevant": 'null'
                    }
                )
        return json.dumps(questionnaire, indent=4)

    def update_questionnaire(
            self, organization_slug, project_slug, questionnaire):
        """Update questionnaire of selected project.

        :param organization_slug: Organization slug for Questionnaire
        :type organization_slug: Str

        :param project_slug: Project slug for Questionnaire
        :type project_slug: Str

        :param questionnaire: Questionnaire that will be updated
        :type questionnaire: Str
        """
        self.update_questionnaire_api = UpdateQuestionnaire(
            organization_slug=organization_slug,
            project_slug=project_slug,
            new_questionnaire=questionnaire,
            on_finished=self.update_questionnaire_finished
        )

    def update_questionnaire_finished(self, result):
        """Update questionnaire of selected project is finished.

        :param result: result of request
        :type result: (bool, list/dict/str, str, str)
        """
        pass
