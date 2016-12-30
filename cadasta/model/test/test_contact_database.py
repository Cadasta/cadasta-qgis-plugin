# coding=utf-8

"""Tests for Contact Database.
"""

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '28/12/16'

import unittest

from cadasta.model.contact import Contact


class ContactDatabaseTest(unittest.TestCase):
    """Test Contact Database."""

    def setUp(self):
        """Runs before each test."""
        self.database_name = 'test'

    def test_insert_fail_database(self):
        """Test Insert Fail Database."""
        contact = Contact()
        contact.save()
        self.assertIsNone(contact.id)

    def test_insert_success_database(self):
        """Test Insert success Database."""
        test_contact = Contact(
            name='test1',
            email='test1@gmail.com',
            phone='000000'
        )
        test_contact.save()
        self.assertIsNotNone(test_contact.id)

        test_contact.delete()

    def test_get_rows_database(self):
        """Test Get Rows Contact Database."""
        # create first
        test_contact = Contact(
            name='test2',
            email='test2@gmail.com',
            phone='0000'
        )
        test_contact.save()
        self.assertIsNotNone(test_contact.id)

        # get the row
        contacts = Contact.get_rows(id=test_contact.id)
        self.assertEqual(len(contacts), 1)

        test_contact.delete()

    def test_update_database(self):
        """Test Insert success Database."""
        # save first if not saved
        test_contact = Contact(
            name='test1',
            email='test1@gmail.com',
            phone='000000'
        )
        test_contact.save()
        self.assertIsNotNone(test_contact.id)

        # update it
        id = test_contact.id
        updated_name = 'test1_updated'
        test_contact.name = updated_name
        test_contact.save()
        self.assertIsNotNone(test_contact.id)

        # check from database
        contacts = Contact.get_rows(id=test_contact.id)
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].id, id)
        self.assertEqual(contacts[0].name, updated_name)

        test_contact.delete()

    def test_delete_row(self):
        """Test Get Rows Contact Database."""
        # create first
        test_contact = Contact(
            name='test3',
            email='test3@gmail.com',
            phone='00000'
        )
        test_contact.save()
        self.assertIsNotNone(test_contact.id)

        # get it's id
        id = test_contact.id
        contacts = Contact.get_rows(id=id)
        self.assertEqual(len(contacts), 1)

        # delete object
        test_contact.delete()

        # check it again from database
        contacts = Contact.get_rows(id=id)
        self.assertEqual(len(contacts), 0)


if __name__ == "__main__":
    suite = unittest.makeSuite(ContactDatabaseTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
