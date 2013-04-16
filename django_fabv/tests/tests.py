"""
Tests for fabv
"""
import os
from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from fabv.models import Hit, Experiment, Test


class ExtendedTestCase(TestCase):
    """
    Provides general functionality for the fabv tests
    """
    urls = "fabv.tests.urls"

    template_dirs = [
        os.path.join(os.path.dirname(__file__), 'templates'),
    ]

    def setUp(self):
        """
        Sets up the test
        """
        # Django related stuff
        self.settings_template_dir = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = self.template_dirs

        self.client1 = Client(REMOTE_ADDR="127.0.0.1")
        self.client2 = Client(REMOTE_ADDR="127.0.0.2")

    def tearDown(self):
        """
        Restores the settings
        """
        # According to the docs this could be cached
        settings.TEMPLATE_DIRS = self.settings_template_dir


class TestTemplates(ExtendedTestCase):
    """
    Tests that the templates are served correctly
    """
    def testTemplates(self):
        """
        Test the content of the templates
        """
        response = self.client1.get('')
        self.assertTrue("index" in response.content)

        response = self.client1.get('/test/')
        self.assertTrue("test" in response.content)
        self.assertTrue("foo" not in response.content)

        response = self.client1.get('/landing/')
        self.assertTrue("stats" not in response.content)

        response = self.client1.get('/signup/')
        self.assertTrue("signup" in response.content)

        response = self.client1.get('foobar')
        self.assertTrue("404" in response.content)


class TestHits(ExtendedTestCase):
    """
    Tests whether hits are registered
    """

    def testHits(self):
        """
        Test the recording of hits.
        """
        response = self.client1.get('')
        self.assertTrue("index" in response.content)

        start_pk = Hit.objects.all()[0].pk
        hit = Hit.objects.select_related().get(pk=start_pk)
        user1_key = hit.user.key
        self.assertTrue(hit.user.ip == "127.0.0.1")

        response = self.client1.get('')
        hit = Hit.objects.select_related().get(pk=start_pk + 1)
        self.assertTrue(user1_key == hit.user.key)

        response = self.client2.get('')
        hit = Hit.objects.select_related().get(pk=start_pk + 2)
        self.assertTrue(user1_key != hit.user.key)

        count_hits = Hit.objects.count()
        self.assertTrue(count_hits == 3)


class TestExperiments(ExtendedTestCase):
    """
    Tests the display of experiments
    """

    def testExperiments(self):
        """
        Tests a simple experiment with one and two variations
        """
        experiment = Experiment(name="Foo", short_name="foo")
        experiment.save()

        testOption1 = Test(experiment=experiment, name="Foo", content="foo")
        testOption1.save()

        response = self.client1.get('/test/')
        self.assertTrue("foo" in response.content)

        testOption2 = Test(experiment=experiment, name="Bar", content="bar")
        testOption2.save()

        i = 0
        found_bar = False
        while (not found_bar and i < 255):
            i += 1
            client = Client(REMOTE_ADDR="128.0.0." + str(i))
            response = client.get('/test/')
            if "bar" in response.content:
                found_bar = True  # Drinks for everyone!
        # This tests passes with p = 1 - (0.5^255)
        self.assertTrue(found_bar)


class TestPersistence(ExtendedTestCase):
    """
    Tests the display of experiments
    """

    def testPersistence(self):
        """
        Tests the persistence of the displayed variations
        """
        url = '/persistence/'

        experiment = Experiment(name="Persistence", short_name="persistence")
        experiment.save()

        testOption1 = Test(experiment=experiment, name="Foo", content="foo")
        testOption1.save()

        testOption2 = Test(experiment=experiment, name="Foo", content="bar")
        testOption2.save()


        content = self.client1.get(url).content

        found_deviation = False
        i = 0
        while (not found_deviation and i < 1000):
            i += 1
            response = self.client1.get(url)
            if content not in response.content:
                found_deviation = True
        # This tests passes with p = 1 - (0.5^1000)
        self.assertTrue(not found_deviation)


class TestStatistics(ExtendedTestCase):
    """
    Tests the display of experiments
    """

    def testStatistics(self):
        """
        Tests a simple experiment with one and two variations
        """
        experiment = Experiment(name="Statistics1", short_name="stats")
        experiment.save()

        testOption1 = Test(experiment=experiment, name="Foo", content="foo")
        testOption1.save()

        testOption2 = Test(experiment=experiment, name="Bar", content="bar")
        testOption2.save()

        clients = []
        n = 255
        # Create 255 clients and connect to the test page, our public
        # really likes content containing bar and is immediately
        # interested in signing up in this scenario.
        for i in xrange(1, n + 1):
            client = Client(REMOTE_ADDR="127.0.1." + str(i))
            clients.append(client)

            response = self.client.get('/landing/')
            if "bar" in response.content:
                response = self.client.get('/signup/')

        count_hits = Hit.objects.count()
        self.assertTrue(n <= count_hits and count_hits <= n * 2)
