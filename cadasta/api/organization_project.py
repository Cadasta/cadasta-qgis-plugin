# coding=utf-8
"""
Cadasta project - **Organization Project api.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import logging
from cadasta.mixin.network_mixin import NetworkMixin
from cadasta.common.setting import get_url_instance

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '21/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

LOGGER = logging.getLogger('CadastaQGISPlugin')


class OrganizationProject(NetworkMixin):
    """Class to fetch available organization project data."""

    api_url = 'api/v1/organizations/%s/projects/'

    def __init__(self, organization_slug, on_finished=None):
        """Constructor.

        :param organization_slug: Organization slug for getting projects
        :type organization_slug: str

        :param on_finished: (optional) function that catch result request
        :type on_finished: Function
        """
        self.request_url = get_url_instance() + (
            self.api_url % organization_slug)

        super(OrganizationProject, self).__init__()
        self.connect_get()
        self.on_finished = on_finished

    def connection_finished(self):
        """On finished function when tools request is finished."""
        # extract result
        if self.error:
            self.on_finished((False, self.error))
        else:
            result = self.get_json_results()
            if self.on_finished and callable(self.on_finished):
                self.on_finished((True, result))


class OrganizationProjectSpatial(NetworkMixin):
    """Class to fetch available organization project spatial data."""

    api_url = 'api/v1/organizations/%s/projects/%s/spatial/'

    def __init__(self, organization_slug, project_slug, on_finished=None):
        """Constructor.

        :param organization_slug: Organization slug for getting spatial
        :type organization_slug: str

        :param project_slug: Project slug for getting spatial
        :type project_slug: str

        :param on_finished: (optional) function that catch result request
        :type on_finished: Function
        """
        self.request_url = get_url_instance() + (
            self.api_url % (organization_slug, project_slug))

        self.organization_slug = organization_slug
        self.project_slug = project_slug

        super(OrganizationProjectSpatial, self).__init__()
        self.connect_get()
        self.on_finished = on_finished

    def connection_finished(self):
        """On finished function when tools request is finished.

        It will passing status of request, result,
        organization slug and project_slug
        to on_finished method
        """
        # extract result
        if self.error:
            self.on_finished(
                (False, self.error, self.organization_slug, self.project_slug)
            )
        else:
            result = self.get_json_results()
            if self.on_finished and callable(self.on_finished):
                self.on_finished(
                    (True, result, self.organization_slug, self.project_slug)
                )
