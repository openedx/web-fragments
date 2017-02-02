"""
Django view implementation of web fragments.
"""

from abc import ABCMeta, abstractmethod

from django.http import HttpResponse, JsonResponse
from django.template.context import Context
from django.template.loader import get_template
from django.views.generic import View

WEB_FRAGMENT_RESPONSE_TYPE = 'application/web-fragment'
STANDALONE_TEMPLATE_NAME = 'web_fragments/standalone_fragment.html'


class FragmentView(View):
    """
    Base class for Django web fragment views.
    """
    __metaclass__ = ABCMeta

    def get(self, request, *args, **kwargs):
        """
        Render a fragment to html or return json describing it, based on the request.
        """
        fragment = self.render_fragment(request, *args, **kwargs)
        response_format = request.GET.get('format') or request.POST.get('format') or 'html'
        if response_format == 'json' or WEB_FRAGMENT_RESPONSE_TYPE in request.META.get('HTTP_ACCEPT'):
            json = fragment.to_dict()
            return JsonResponse(json)
        else:
            html = self.render_standalone_html(fragment)
            return HttpResponse(html)

    def render_standalone_html(self, fragment):
        """
        Render html needed in the head, body and footer of the page needed by this fragment
        """
        template = get_template(STANDALONE_TEMPLATE_NAME)
        context = Context({
            'head_html': fragment.head_html(),
            'body_html': fragment.body_html(),
            'foot_html': fragment.foot_html(),
        })
        return template.render(context)

    @abstractmethod
    def render_fragment(self, request, **kwargs):
        """
        Not implemented yet.
        """
        raise NotImplementedError()
