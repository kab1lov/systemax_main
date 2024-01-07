import os
import uuid

from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
from django.db.models import Model, CharField, ImageField, ForeignKey, CASCADE, SlugField, DateTimeField, EmailField
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


class BlogModel(Model):
    title = CharField(max_length=255)
    image = ImageField(upload_to=image_filename)
    text = RichTextField()
    blog_inner = ForeignKey(BlogInnerTextModel, CASCADE, related_name='blogs')
    created_at = DateTimeField(auto_now_add=True)
    slug = SlugField(max_length=255, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # if not self.slug:
        self.slug = slugify(self.title)
        while BlogModel.objects.filter(slug=self.slug).exists():
            slug = BlogModel.objects.filter(slug=self.slug).first().slug
            if '-' in slug:
                try:
                    if slug.split('-')[-1] in self.title:
                        self.slug += '-1'
                    else:
                        self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                except:
                    self.slug = slug + '-1'
            else:
                self.slug += '-1'

        super().save(force_insert, force_update, using, update_fields)


class BlogChildModel(Model):
    text = CharField(max_length=255)
    blog = ForeignKey(BlogModel, CASCADE, related_name="children")


class IndexAboutModel(Model):
    title = CharField(max_length=255)
    text = RichTextField()


class StatisticsModel(Model):
    delivery = CharField(max_length=255)
    satisfied_client = CharField(max_length=255)
    settings = CharField(max_length=255)
    support = CharField(max_length=255)


class PartnersModel(Model):
    image = ImageField(upload_to=image_filename)


class Contact(Model):
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


class ServicesInnerTextModel(Model):
    title = CharField(max_length=255)


class ServiceModel(Model):
    main_image = ImageField(upload_to=image_filename)
    text = RichTextField()
    service_inner = ForeignKey(ServicesInnerTextModel, CASCADE, related_name="services")
    created_at = DateTimeField(auto_now_add=True)
    slug = SlugField(max_length=255, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # if not self.slug:
        self.slug = slugify(self.title)
        while BlogModel.objects.filter(slug=self.slug).exists():
            slug = BlogModel.objects.filter(slug=self.slug).first().slug
            if '-' in slug:
                try:
                    if slug.split('-')[-1] in self.title:
                        self.slug += '-1'
                    else:
                        self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                except:
                    self.slug = slug + '-1'
            else:
                self.slug += '-1'

        super().save(force_insert, force_update, using, update_fields)


class ServiceImageModel(ImageDeletionMixin,Model):
    image = ImageField(upload_to=image_filename)
    service = ForeignKey(ServiceModel, CASCADE, related_name="images")



