#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for the Fragment class.
"""

from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from web_fragments.fragment import Fragment

TEST_HTML = '<p>Hello, world!</p>'
TEST_CSS = 'body {background-color:red;}'
TEST_CSS_URL = '/css/test.css'
TEST_JS = 'window.alert("Hello");'
TEST_JS_URL = '/js/test.js'
TEST_JS_INIT_FN = 'mock_initialize'
TEST_JS_INIT_VERSION = 1


class TestFragment(TestCase):
    """
    Unit tests for fragments.
    """

    def setUp(self):
        super(TestFragment, self).setUp()

    def create_test_fragment(self):
        """
        Creates a fragment for use in unit tests.
        """
        fragment = Fragment()
        fragment.add_content(TEST_HTML)
        fragment.add_css(TEST_CSS)
        fragment.add_css_url(TEST_CSS_URL)
        fragment.add_javascript(TEST_JS)
        fragment.add_javascript_url(TEST_JS_URL)
        fragment.initialize_js(TEST_JS_INIT_FN)
        return fragment

    def test_resources_dict(self):
        """
        Returns the expected test resources.
        """
        return [
            {
                'kind': 'text',
                'data': TEST_CSS,
                'mimetype': 'text/css',
                'placement': 'head',
            },
            {
                'kind': 'url',
                'data': TEST_CSS_URL,
                'mimetype': 'text/css',
                'placement': 'head',
            },
            {
                'kind': 'text',
                'data': TEST_JS,
                'mimetype': 'application/javascript',
                'placement': 'foot',
            },
            {
                'kind': 'url',
                'data': TEST_JS_URL,
                'mimetype': 'application/javascript',
                'placement': 'foot',
            },
        ]

    def testToDict(self):
        """
        Tests the toDict method.
        """
        fragment = self.create_test_fragment()
        dict = fragment.to_dict()
        self.assertEqual(dict['content'], TEST_HTML)
        self.assertEqual(dict['js_init_fn'], TEST_JS_INIT_FN)
        self.assertEqual(dict['js_init_version'], TEST_JS_INIT_VERSION)
        self.assertEqual(dict['resources'], self.test_resources_dict())

    def testFromDict(self):
        """
        Tests the fromDict method.
        """
        test_dict = {
            'content': TEST_HTML,
            'resources': self.test_resources_dict(),
            'js_init_fn': TEST_JS_INIT_FN,
            'js_init_version': TEST_JS_INIT_VERSION
        }
        fragment = Fragment.from_dict(test_dict)
        result_dict = fragment.to_dict()
        self.assertEqual(result_dict['content'], TEST_HTML)
        self.assertEqual(result_dict['js_init_fn'], TEST_JS_INIT_FN)
        self.assertEqual(result_dict['js_init_version'], TEST_JS_INIT_VERSION)
        self.assertEqual(result_dict['resources'], self.test_resources_dict())

    def test_body_html(self):
        """
        Tests the body_html method.
        """
        fragment = self.create_test_fragment()
        html = fragment.body_html()
        self.assertEqual(html, TEST_HTML)

    def test_head_html(self):
        """
        Tests the head_html method.
        """
        fragment = self.create_test_fragment()
        html = fragment.head_html()
        self.assertEqual(
            html.replace('\n', ''),
            "<style type='text/css'>{css}</style><link rel='stylesheet' href='{css_url}' type='text/css'>".format(
                css=TEST_CSS,
                css_url=TEST_CSS_URL,
            )
        )

    def test_foot_html(self):
        """
        Tests the foot_html method.
        """
        fragment = self.create_test_fragment()
        html = fragment.foot_html()
        self.assertEqual(
            html.replace('\n', ''),
            "<script>{js}</script><script src='{js_url}' type='application/javascript'></script>".format(
                js=TEST_JS,
                js_url=TEST_JS_URL,
            )
        )
