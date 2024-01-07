from urllib.parse import urlparse

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve, Resolver404, reverse, NoReverseMatch
from django.utils import translation
from django.views.generic import TemplateView

from root import settings


# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class AllFarmView(TemplateView):
    template_name = "allFirma.html"


class BlogView(TemplateView):
    template_name = "blog.html"


class BlogSingleView(TemplateView):
    template_name = "blog-single.html"


class ContactView(TemplateView):
    template_name = "contact.html"


def set_language(request, language):
    view = None

    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            pass
        else:
            break

    if view:
        translation.activate(language)
        try:
            next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
            response = HttpResponseRedirect(next_url)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        except (NoReverseMatch, ObjectDoesNotExist):
            response = HttpResponseRedirect("/")
    else:
        response = HttpResponseRedirect("/")

    return response
