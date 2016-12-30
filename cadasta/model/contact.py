# coding=utf-8
"""
Cadasta project - **Contact Model.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '28/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

from qgis.PyQt.QtSql import QSqlQuery
from cadasta.database.cadasta_database import CadastaDatabase


class Contact():
    """Contact model."""
    id = None
    name = None
    email = None
    phone = None
    _fields = ['id', 'name', 'email', 'phone']

    def __init__(self, id=None,
                 name=None, email=None, phone=None):
        """Constructor.

        :param id: id of contact.
        :type id: int

        :param name: name of contact.
        :type name: str

        :param email: email of contact.
        :type email: str

        :param phone: phone of contact.
        :type phone: str
        """
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        Contact.create_database()

    def save(self):
        """Save this object to database

        :return: id of row that is inserted
        :rtype: int
        """

        data = {}
        if self.id:
            data['id'] = self.id
        if self.name:
            data['name'] = u'\"%s\"' % self.name
        if self.email:
            data['email'] = u'\"%s\"' % self.email
        if self.phone:
            data['phone'] = u'\"%s\"' % self.phone

        # save to database
        row_id = CadastaDatabase.save_to_database(
            Contact.__name__, data)
        if row_id >= 1:
            self.id = row_id
        return self.id

    def delete(self):
        """Delete this object
        """
        CadastaDatabase.delete_rows_from_database(
            Contact.__name__, [self.id])
        del self

    # ------------------------------------------------------------------------
    # STATIC METHOD
    # ------------------------------------------------------------------------
    @staticmethod
    def create_database():
        """Create table function."""
        db = CadastaDatabase.open_database()
        query_fields = ('id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'name varchar(20) NOT NULL,'
                        'email varchar(20),'
                        'phone varchar(20)')
        query_string = 'create table %(TABLE)s (%(query_field)s)' % \
                       {
                           'TABLE': Contact.__name__,
                           'query_field': query_fields
                       }
        query = QSqlQuery()
        query.exec_(query_string)
        db.close()

    @staticmethod
    def get_rows(**kwargs):
        """Get filtered rows from kwargs

        :return: List of json of the rows
        :rtype: [dict]
        """
        query_filter = []
        filter_string = '%(FIELD)s=%(VALUE)s'
        for key, value in kwargs.iteritems():
            if key != 'id':
                value = '"%s"' % value

            # append it to query filter
            query_filter.append(filter_string % {
                'FIELD': key,
                'VALUE': value
            })
        query = CadastaDatabase.get_from_database(
            Contact.__name__, ','.join(query_filter))

        #  convert
        output = []
        while (query.next()):
            output.append(
                Contact(
                    id=query.value(0),
                    name=query.value(1),
                    email=query.value(2),
                    phone=query.value(3)
                )
            )
        return output

    @staticmethod
    def table_model():
        """Get Table Model for Contact

        :return: Table Model for contact
        :rtype: QSqlTableModel
        """
        Contact.create_database()
        return CadastaDatabase.get_table_model(Contact.__name__)
