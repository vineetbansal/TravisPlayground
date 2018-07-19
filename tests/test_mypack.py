from unittest import TestCase

from mypack import create_app
from mypack.blueprints.web import index, hello, n_actors

# Testing web endpoints/blueprint requires a working 'app'
app = create_app(debug=True)


class APITestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testWebEndpoint(self):
        """
        Test a web endpoint by emulating a web request
        """
        with app.test_request_context('/'):
            rv = app.preprocess_request()
            if rv is not None:
                response = app.make_response(rv)
            else:
                rv = app.dispatch_request()
                response = app.make_response(rv)

                response = app.process_response(response)

        self.assertEqual(response.mimetype, 'text/html')
        self.assertEqual(response.data.decode('utf-8'), 'Index page works!')

    def testBlueprintRoute1(self):
        """
        Test a blueprint route directly (fast!)
        """
        self.assertEqual(index(), 'Index page works!')

    def testBlueprintRoute2(self):
        """
        Test a blueprint route directly (fast!)
        """
        # If a blueprint renders a template, an app context needs to be pushed to the stack
        with app.app_context():
            self.assertEqual(hello(), 'Hello World')

    def testBlueprintRoute3(self):
        self.assertEqual(n_actors(), '200')