#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for web fragment views
"""

from __future__ import absolute_import, unicode_literals

from django.http import HttpResponse, JsonResponse
from django.test import TestCase
from django.test.client import RequestFactory

from web_fragments.views import FragmentView



class TestViews(TestCase):
    """
    Unit tests for views.
    """

    def setUp(self):
        super(TestViews, self).setUp()
        self.requests = RequestFactory()
        self.view = FragmentView()

    def test_get_with_GET(self):
        """
        Test fragment getter when sent an HTTP GET with format=json
        """
        self.view.get(self.requests.get("/?format=json"))

    def test_get_with_POST(self):
        """
        Test fragment getter when sent an HTTP POST with format=json
        """
        self.view.get(self.requests.post("/", {"format": "json"}))

    def test_get_with_meta(self):
        """
        Test fragment getter with an HTTP request with an Accept=application/web-fragment header
        """
        self.view.get(self.requests.get("/", {}, HTTP_ACCEPT='application/web-fragment'))

    def test_get_html_explicit(self):
        """
        Test fragment getter when html is requested
        """
        self.view.render_standalone_html = {}
        self.view.get(self.requests.get("/?format=hmtl"))

    def test_get_html_implicit(self):
        """
        Test fragment getter when no format is specified
        """
        self.view.render_standalone_html = {}
        self.view.get(self.requests.get("/"))

    def test_render_standalone_html(self):
        """
        Test the render_standalone_html method of the FragmentView class
        """
