from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from apps.models import (
    BlogInnerTextModel,
    BlogModel,
    BlogChildModel,
    IndexAboutModel,
    StatisticsModel,
    PartnersModel,
    ContactModel,
    ServiceImageModel,
    ServiceModel,
    About,
    SocialsModel,
)


@admin.register(BlogInnerTextModel)
class BlogInnerTextAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    list_display_links = (
        "id",
        "title",
    )


class BlogChildrenAdmin(StackedInline):
    model = BlogChildModel


@admin.register(BlogModel)
class BlogAdmin(ModelAdmin):
    list_display = ("id", "title", "image", "text")
    list_display_links = (
        "id",
        "title",
    )
    exclude = ("slug",)
    inlines = (BlogChildrenAdmin,)


@admin.register(IndexAboutModel)
class IndexAboutAdmin(ModelAdmin):
    list_display = ("id", "title", "text")
    list_display_links = (
        "id",
        "title",
    )


@admin.register(StatisticsModel)
class StatisticsAdmin(ModelAdmin):
    list_display = ("id", "delivery")
    list_display_links = (
        "id",
        "delivery",
    )


@admin.register(PartnersModel)
class PartnersAdmin(ModelAdmin):
    list_display = ("id", "image")
    list_display_links = (
        "id",
        "image",
    )


@admin.register(ContactModel)
class ContactAdmin(ModelAdmin):
    list_display = ("id", "address")
    list_display_links = (
        "id",
        "address",
    )


class ServiceImageAdmin(StackedInline):
    model = ServiceImageModel


@admin.register(ServiceModel)
class ServiceAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
        "main_image",
    )
    list_display_links = (
        "id",
        "title",
    )
    exclude = ("slug",)
    inlines = (ServiceImageAdmin,)


@admin.register(About)
class AboutAdmin(ModelAdmin):
    list_display = ("id", "title", "text")
    list_display_links = (
        "id",
        "title",
    )


@admin.register(SocialsModel)
class SocialAdmin(ModelAdmin):
    list_display = ("id", "facebook")
    list_display_links = (
        "id",
        "facebook",
    )
