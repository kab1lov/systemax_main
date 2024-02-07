import os
import uuid

from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator, URLValidator
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    ImageField,
    Model,
    SlugField,
    URLField,
)
from django.utils.text import slugify


class ImageDeletionMixin(Model):
    @staticmethod
    def _delete_file(path):
        if os.path.isfile(path):
            os.remove(path)

    def delete_image(self, field_name):
        try:
            image_field = getattr(self, field_name)
            if image_field:
                self._delete_file(image_field.path)
        except AttributeError:
            pass

    def delete(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, ImageField):
                self.delete_image(field.name)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        is_new_instance = not self.pk
        orig = None
        if not is_new_instance:
            orig = self.__class__.objects.get(pk=self.pk)
        super().save(*args, **kwargs)
        if not is_new_instance and orig:
            for field in self._meta.get_fields():
                if isinstance(field, ImageField):
                    new_image_field = getattr(self, field.name)
                    old_image_field = getattr(orig, field.name)
                    if new_image_field != old_image_field:
                        self.delete_image(old_image_field.name)

    class Meta:
        abstract = True


def image_filename(instance, filename):
    extension = filename.split(".")[-1]
    unique_filename = uuid
    return f"images/{unique_filename}"


class BlogInnerTextModel(Model):
    title = CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Blog Inner"


class BlogModel(ImageDeletionMixin, Model):
    title = CharField(max_length=255)
    image = ImageField(upload_to=image_filename)
    text = RichTextField()
    blog_inner = ForeignKey(BlogInnerTextModel, CASCADE, related_name="blogs")
    created_at = DateTimeField(auto_now_add=True)
    slug = SlugField(max_length=255, unique=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.pk:  # noqa
            self.slug = slugify(self.title)
        else:
            old_instance = BlogModel.objects.get(pk=self.pk)
            if self.title != old_instance.title:
                self.slug = slugify(self.title)

        while BlogModel.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            if "-" in self.slug:
                parts = self.slug.split("-")
                if parts[-1].isdigit():
                    count = int(parts[-1])
                    self.slug = "-".join(parts[:-1]) + "-" + str(count + 1)
                else:
                    self.slug += "-1"
            else:
                self.slug += "-1"

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Blogs"


class BlogChildModel(Model):
    text = CharField(max_length=255)
    blog = ForeignKey(BlogModel, CASCADE, related_name="children")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Blog Children"


class IndexAboutModel(Model):
    title = CharField(max_length=255)
    text = RichTextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Index About"


class StatisticsModel(Model):
    delivery = CharField(max_length=255)
    satisfied_client = CharField(max_length=255)
    settings = CharField(max_length=255)
    support = CharField(max_length=255)

    def __str__(self):
        return self.delivery

    class Meta:
        verbose_name_plural = "Statistics"


class PartnersModel(ImageDeletionMixin, Model):
    image = ImageField(upload_to=image_filename)

    class Meta:
        verbose_name_plural = "Partners"


class ContactModel(Model):
    address = CharField(max_length=255)
    map = CharField(max_length=350)
    email = EmailField(max_length=255, unique=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number1 = CharField(
        validators=[phone_regex], max_length=17, blank=True, unique=True
    )
    phone_number2 = CharField(
        validators=[phone_regex], max_length=17, blank=True, unique=True
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = "Contact"


class ServiceModel(ImageDeletionMixin, Model):
    title = CharField(max_length=255)
    sub_title = CharField(max_length=255)
    main_image = ImageField(upload_to=image_filename)
    up_text = RichTextField()
    down_text = RichTextField()
    created_at = DateTimeField(auto_now_add=True)
    slug = SlugField(max_length=255, unique=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.pk:  # noqa
            self.slug = slugify(self.title)
        else:
            old_instance = ServiceModel.objects.get(pk=self.pk)
            if self.title != old_instance.title:
                self.slug = slugify(self.title)

        while ServiceModel.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            if "-" in self.slug:
                parts = self.slug.split("-")
                if parts[-1].isdigit():
                    count = int(parts[-1])
                    self.slug = "-".join(parts[:-1]) + "-" + str(count + 1)
                else:
                    self.slug += "-1"
            else:
                self.slug += "-1"

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Services"


class ServiceImageModel(ImageDeletionMixin, Model):
    image = ImageField(upload_to=image_filename)
    service = ForeignKey(ServiceModel, CASCADE, related_name="images")

    class Meta:
        verbose_name_plural = "Service Images"


class About(Model):
    title = CharField(max_length=255)
    text = RichTextField()
    link = URLField(validators=(URLValidator,), null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "About"


class SocialsModel(Model):
    facebook = URLField(validators=(URLValidator,), null=True, blank=True)
    instagram = URLField(validators=(URLValidator,), null=True, blank=True)
    telegram = URLField(validators=(URLValidator,), null=True, blank=True)

    def __str__(self):
        return self.facebook

    class Meta:
        verbose_name_plural = "Socials"
