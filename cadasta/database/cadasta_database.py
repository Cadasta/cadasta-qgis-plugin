# coding=utf-8
"""
Cadasta **Cadasta Database.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.


"""

import logging
from qgis.PyQt import QtSql
from qgis.PyQt.QtSql import QSqlTableModel
from cadasta.common.setting import get_path_database

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '27/12/16'
__copyright__ = 'Copyright 2016, Cadasta'

LOGGER = logging.getLogger('CadastaQGISPlugin')

database = 'QSQLITE'
database_name = get_path_database('cadasta.db')


class CadastaDatabase(object):
    """Cadasta class to handle database."""

    def __init__(self):
        """Constructor for the class."""

    @staticmethod
    def open_database():
        """Open Database.

        :return: Database that opened
        :rtype: QtSql.QSqlDatabase
        """
        db = QtSql.QSqlDatabase.addDatabase(database)
        if db:
            db.setDatabaseName(database_name)
            if db.open():
                LOGGER.debug("not opened")
                return db
        return None

    @staticmethod
    def save_to_database(table, data):
        """Save Into database.

        :param table: Table target be inserted
        :type table: str

        :param data: Data to be inserted
        :type data: dict

        :return: id of row that is inserted
        :rtype: int
        """
        db = CadastaDatabase.open_database()
        if 'id' in data:
            # updating existing data
            row_id = data['id']
            del data['id']

            query_filter = []
            filter_string = '%(FIELD)s=%(VALUE)s'
            for key, value in data.iteritems():
                value = value
                # append it to query filter
                query_filter.append(filter_string % {
                    'FIELD': key,
                    'VALUE': value
                })
            query_string = (
                               'UPDATE %(TABLE)s SET %(SET)s '
                               'WHERE id=%(ID)s'
                           ) % {
                               'TABLE': table,
                               'SET': ','.join(query_filter),
                               'ID': row_id
                           }
        else:
            # inserting new data
            fields = []
            values = []
            for key, value in data.iteritems():
                fields.append(key)
                values.append(value)
            query_string = (
                               'INSERT INTO %(TABLE)s (%(FIELDS)s) '
                               'VALUES (%(VALUES)s)'
                           ) % {
                               'TABLE': table,
                               'FIELDS': ','.join(fields),
                               'VALUES': ','.join(values)
                           }
        query = QtSql.QSqlQuery(db)
        query.exec_(query_string)
        db.close()
        if query.numRowsAffected() < 1:
            return -1
        else:
            return query.lastInsertId()

    @staticmethod
    def get_from_database(table, filter_string):
        """Get rows from database.

        :param table: Table target be inserted
        :type table: str

        :param filter_string: Filter_string that will be used as filter
        :type filter_string: str

        :return: Query that is received
        :rtype: QSqlQuery
        """
        db = CadastaDatabase.open_database()
        query_string = (
            'SELECT * FROM %(TABLE)s ' % {'TABLE': table}
        )
        if filter_string:
            query_string += 'WHERE %s' % filter_string
        query = QtSql.QSqlQuery(db)
        query.exec_(query_string)
        db.close()
        return query

    @staticmethod
    def delete_rows_from_database(table, row_ids):
        """Delete rows from database.

        :param table: Table target be inserted
        :type table: str

        :param row_ids: List id of row that will be deleted
        :type row_ids: [int]
        """
        db = CadastaDatabase.open_database()
        row_ids = ['%s' % row_id for row_id in row_ids]
        query_string = (
            'DELETE FROM %(TABLE)s WHERE ID IN (%(ID)s)' % {
                'TABLE': table, 'ID': ','.join(row_ids)
            }
        )
        query = QtSql.QSqlQuery(db)
        query.exec_(query_string)
        db.close()

    @staticmethod
    def get_table_model(table):
        """Get table model of table.

        :param table: Table target be inserted
        :type table: str

        :return: Table Model for contact
        :rtype: QSqlTableModel
        """
        CadastaDatabase.open_database()
        table_model = QSqlTableModel()
        table_model.setTable(table)
        table_model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        table_model.select()
        return table_model
