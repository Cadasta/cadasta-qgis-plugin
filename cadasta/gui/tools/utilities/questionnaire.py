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
    'integer64': 'IN',
    'double': 'DE',
    'real': 'DE',
    'date': 'DA',
    'datetime': 'DT'
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

    def generate_new_questionnaire(
            self, current_layer, mapped_fields, current_questionnaire):
        """Generate new questionnaire.

        This will get current questionnaire or create from default
        questionnaire. Updating it by looking of fields from current layer.

        Questionnaire is based on current layer field.
        All of new field that not in questionnaire will be append to
        question group -> 'location_attributes'

        :param current_layer: layer that using for generate questionnaire
        :type current_layer: QgsVectorLayer

        :param mapped_fields: Mapping fields of layer to key on questionnaire
        :type mapped_fields: dict

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

        # get all question name in questionnaire
        attributes_in_questionnaire = []
        for question in questionnaire["questions"]:
            attributes_in_questionnaire.append(question["name"])

        # get question group in questionnaire question group
        if 'question_groups' not in questionnaire:
            questionnaire['question_groups'] = []

        # Get current fields
        # Current field of layer for attribute
        # insert into 'location_attributes'
        location_attributes = {
            "name": "location_attributes",
            "label": "Location Attributes",
            "type": 'group',
            "questions": []
        }
        index = 1
        for field in current_layer.fields():
            field_name = field.name()
            if field_name != 'id':
                if field_name not in mapped_fields:
                    try:
                        # check location attributes in question group
                        location_attributes["questions"].append(
                            {
                                "name": field_name,
                                "label": field_name,
                                "type": mapping_type[
                                    field.typeName().lower()
                                ],
                                "required": False,
                                "default": 'null',
                                "hint": 'null',
                                "relevant": 'null',
                            }
                        )
                    except KeyError:
                        pass
                    index += 1

        # insert into questionnaire
        index = -1
        for question_group in questionnaire['question_groups']:
            index += 1
            if question_group['name'] == 'location_attributes':
                break

        if index == -1:
            questionnaire['question_groups'].append(
                location_attributes)
        else:
            questionnaire['question_groups'][index] = location_attributes

        return json.dumps(questionnaire, indent=4)

    def add_index(self, question_object, index):
        """Add index to question.

        :param question_object: object to be added index
        :type question_object: dict

        :param index: current index
        :type index: int

        :return: latest index
        :rtype: int
        """
        if 'index' not in question_object:
            question_object['index'] = index
        else:
            if question_object['index'] - index != 1:
                question_object['index'] = index + 1
        index += 1
        return index

    def validate_questionnaire(self, questionnaire):
        """Validate and fix questionnaire file.

        :param questionnaire: questionnaire string
        :type questionnaire: str

        :return: validated questionnaire
        :rtype: str
        """
        questionnaire_obj = json.loads(questionnaire)
        index = 1
        for question in questionnaire_obj['questions']:
            index = self.add_index(question, index)

            if 'options' in question:
                option_index = 1
                for option in question['options']:
                    option_index = self.add_index(option, option_index)

        index = 1
        for question_group in questionnaire_obj['question_groups']:
            index = self.add_index(question_group, index)

            if 'questions' in question_group:
                question_index = 1
                for question in question_group['questions']:
                    question_index = self.add_index(question, question_index)

        return json.dumps(questionnaire_obj)

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
