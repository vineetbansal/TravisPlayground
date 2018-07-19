from unittest import TestCase
from flask import json

from mypack import create_app
from ffmeta.blueprints.web import hel
from ffmeta.models.db import session
from ffmeta.utils import AppException

app = create_app(debug=True)


class APITestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSelectAPI(self):
        """
        Test a 'select' api endpoint by emulating a web request
        """
        with app.test_request_context('/variable/ce3datey', subdomain='api'):
            rv = app.preprocess_request()
            if rv is not None:
                response = app.make_response(rv)
            else:
                rv = app.dispatch_request()
                response = app.make_response(rv)

                response = app.process_response(response)

        self.assertEqual(response.mimetype, 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'ce3datey')

    def testSelect1(self):
        """
        Test selection of a variable by name
        """
        data = select('ce3datey')
        self.assertEqual(data['name'], 'ce3datey')

    def testSelect1(self):
        """
        Test selection of a variable by name, and a given list of attributes we're interested in
        """
        data = select('ce3datey', ['data_source', 'name'])
        self.assertEqual(data['data_source'], 'constructed')

    def testSelect3(self):
        """
        Test selection of a variable that doesn't exist
        """
        self.assertRaises(AppException, select, 'unrecognized_variable_name')

    def testSearch1(self):
        """
        Test searching a variable given it's name
        """
        results = search({'name': 'name', 'op': 'eq', 'val': 'ce3datey'})
        self.assertEqual(len(results), 1)
        self.assertIn('ce3datey', results)

    def testSearchEq(self):
        """
        Test searching a variable given a value for one of it's attributes (wave)
        """
        results = search({'name': 'wave', 'op': 'eq', 'val': 3})
        expected_n_results = next(session.execute('SELECT COUNT(*) FROM variable WHERE wave=3'))[0]
        self.assertEqual(len(results), expected_n_results)

    def testSearchGt(self):
        """
        Test searching a variable given a comparison for one of it's attributes (wave)
        """
        results = search({'name': 'wave', 'op': 'gt', 'val': 3})
        expected_n_results = next(session.execute('SELECT COUNT(*) FROM variable WHERE wave>3'))[0]
        self.assertEqual(len(results), expected_n_results)

    def testSearchMultiple(self):
        """
        Test searching a variable given a multiple search criteria (implicitly combined by AND)
        """
        results = search(
            [
                {'name': 'wave', 'op': 'gt', 'val': 3},
                {'name': 'name', 'op': 'like', 'val': '%z%'}
            ]
        )
        expected_n_results = next(session.execute('SELECT COUNT(*) FROM variable WHERE wave>3 AND name LIKE "%z%"'))[0]
        self.assertEqual(len(results), expected_n_results)

    def testSearchNested(self):
        """
        Test searching a variable given nested search criteria
        """
        results = search(
            [
                {'or': [
                    {'name': 'wave', 'op': 'lte', 'val': 3},
                    {'name': 'name', 'op': 'like', 'val': '%z%'}
                ]},
                {'name': 'data_source', 'op': 'eq', 'val': 'constructed'}
            ]
        )
        expected_n_results = next(session.execute('SELECT COUNT(*) FROM variable WHERE (wave<=3 OR name LIKE "%z%") AND data_source="constructed"'))[0]
        self.assertEqual(len(results), expected_n_results)