"""
Django view implementation of web fragments.
"""
from abc import ABCMeta, abstractmethod

from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.views.generic import View

WEB_FRAGMENT_RESPONSE_TYPE = 'application/web-fragment'
STANDALONE_TEMPLATE_NAME = 'web_fragments/standalone_fragment.html'


class FragmentView(View, metaclass=ABCMeta):
    """
    Base class for Django web fragment views.
    """

    def get(self, request, *args, **kwargs):
        """
        Render a fragment to HTML or return JSON describing it, based on the request.
        """
        fragment = self.render_to_fragment(request, **kwargs)
        response_format = request.GET.get('format') or request.POST.get('format') or 'html'
        if response_format == 'json' or WEB_FRAGMENT_RESPONSE_TYPE in request.headers.get('accept', 'text/html'):
            return JsonResponse(fragment.to_dict())

        return self.render_standalone_response(request, fragment, **kwargs)

    def render_standalone_response(self, request, fragment, **kwargs):
        """
        Renders a standalone page as a response for the specified fragment.
        """
        if fragment is None:
            return HttpResponse(status=204)

        html = self.render_to_standalone_html(request, fragment, **kwargs)
        return HttpResponse(html)

    def render_to_standalone_html(self, request, fragment, **kwargs):
        """
        Render the specified fragment to HTML for a standalone page.
        """
        template = get_template(STANDALONE_TEMPLATE_NAME)
        context = {
            'head_html': fragment.head_html(),
            'body_html': fragment.body_html(),
            'foot_html': fragment.foot_html(),
        }
        return template.render(context)

    @abstractmethod
    def render_to_fragment(self, request, **kwargs):
        """
        Render this view to a fragment.
        """
        raise NotImplementedError()
