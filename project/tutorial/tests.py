import unittest

from pyramid import testing

class TutorialViewsTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
    
    def test_home(self):
        from .views import TutorialViews
        
        request = testing.DummyRequest()
        inst = TutorialViews(request)
        response = inst.home()
        self.assertEqual('Home View', response['name'])     # Grabing data from code
        
    def test_hello(self):
        from .views import TutorialViews
        
        request = testing.DummyRequest()
        inst = TutorialViews(request)
        response = inst.hello()
        self.assertEqual('Hello View', response['name'])    # Grabing it again
        

class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        app = main({})
        from webtest import TestApp
        
        self.testapp = TestApp(app)
    
    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hi, my name is Home View', res.body)

    def test_hello(self):
        res = self.testapp.get('/howdy', status=200)
        self.assertIn(b'<h1>Hi, my name is Hello View', res.body)