from django.shortcuts import render
from django.views.generic import TemplateView

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
