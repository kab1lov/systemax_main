from urllib.parse import urlparse

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve, Resolver404, reverse, NoReverseMatch
from django.utils import translation
from django.views import View
from django.views.generic import TemplateView, ListView

from apps.models import (
    ServiceModel,
    IndexAboutModel,
    StatisticsModel,
    PartnersModel,
    ContactModel,
    SocialsModel, About,
)
from root import settings


# Create your views here.


class IndexView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        service = ServiceModel.objects.all()
        index_about = IndexAboutModel.objects.first()
        statistics = StatisticsModel.objects.first()
        partners = PartnersModel.objects.all()
        contact = ContactModel.objects.first()
        socials = SocialsModel.objects.first()

        context = {
            "services": service,
            "index_about": index_about,
            "statistics": statistics,
            "partners": partners,
            "contact": contact,
            "socials": socials,
        }
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = "about.html"

    def get(self, request, *args, **kwargs):
        about = About.objects.first()
        partners = PartnersModel.objects.all()
        services = ServiceModel.objects.all()
        socials = SocialsModel.objects.first()

        context = {
            'about': about,
            "partners": partners,
            "services": services,
            "socials": socials,
        }
        return render(request, self.template_name, context)


class AllFarmView(TemplateView):
    template_name = "allFirma.html"


class BlogView(TemplateView):
    template_name = "blog.html"

    def get(self, request, *args, **kwargs):
        services = ServiceModel.objects.all()
        socials = SocialsModel.objects.first()

        context = {
            "services": services,
            "socials": socials,
        }
        return render(request, self.template_name, context)


class BlogSingleView(TemplateView):
    template_name = "blog-single.html"


class ContactView(View):
    template_name = "contact.html"

    def get(self, request, *args, **kwargs):
        contact = ContactModel.objects.first()
        services = ServiceModel.objects.all()
        socials = SocialsModel.objects.first()

        context = {
            'contact': contact,
            "services": services,
            "socials": socials,
        }
        return render(request, self.template_name, context)










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
