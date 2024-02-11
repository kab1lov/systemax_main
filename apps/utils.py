from django.contrib.admin import ModelAdmin
from django.forms import FileInput, TextInput
from django.utils.html import format_html


class TitleSplitter:
    @staticmethod
    def split_colorful_title(colorful_title, title):
        start_part = ""
        middle_part = ""
        end_part = ""

        if colorful_title and title and colorful_title in title:
            start_index = title.find(colorful_title)
            if start_index == 0:
                start_part = colorful_title
                end_part = title[len(colorful_title):].strip()
            else:
                start_part = title[:start_index].strip()
                end_part = title[start_index + len(colorful_title):].strip()
            middle_part = colorful_title

        return start_part, middle_part, end_part


class BaseAdmin(ModelAdmin):
    def has_add_permission(self, request):
        existing_count = self.model.objects.count()
        return existing_count < 1


class ImagePreviewAdminWidget(FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            image_html = format_html(
                '<img src="{}" style="max-width:300px; max-height:300px;" />', value.url
            )
            output.append(image_html)
        output.append(super().render(name, value, attrs, renderer))
        return format_html("".join(output))


class VideoPreviewAdminWidget(FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            video_html = format_html(
                '<video width="320" height="240" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>',
                value.url,
            )
            output.append(video_html)
        output.append(super().render(name, value, attrs, renderer))
        return format_html("".join(output))


class YouTubeVideoAdminWidget(TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value:
            output.append(
                format_html(
                    '<iframe width="320" height="240" src="{}" frameborder="0" allowfullscreen></iframe>',
                    value,
                )
            )
        output.append(super().render(name, value, attrs, renderer))
        return format_html("".join(output))
