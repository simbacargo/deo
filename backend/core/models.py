from django.db import models
import uuid
from django.urls import reverse
import random,string

def get_uuid():
    return str(uuid.uuid4())


def get_token():
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    unique_id = ''.join(random.choice(allowed_chars) for _ in range(10))
    return unique_id


class TimeStampedModel(models.Model):
    """ Time Stamped Model"""
    uid = models.CharField(primary_key=True, default=get_token, editable=False, unique=True, max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def id(self):
        return self.uid


    def save(self, *args, **kwargs):
        self.uid = get_token()
        super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True



class Photo(TimeStampedModel):
    """Photo Model Definition"""
    caption = models.CharField(max_length=80,null=True,blank=True)
    product_id = models.CharField(max_length=80,null=True,blank=True)
    file = models.FileField(upload_to="images/%Y/%m/%d/")
    file_base64 = models.TextField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(Photo, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.file)

from django.db.models.signals import pre_save, post_save,pre_delete

def confirm_created(sender, instance, created, **kwargs):
    if created:
        print ("Created")
def picture_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)

pre_delete.connect(picture_delete, sender=Photo)
post_save.connect(confirm_created, sender=Photo)

class Video(models.Model):
    Video_Description= models.CharField(max_length=500,null=True,blank=True)
    slug = models.SlugField(unique=True)
    videofile= models.FileField(upload_to='deploy/videos/%Y/%m/%d/', null=True, verbose_name="")
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse ("deploy:detail", kwargs={"slug":self.slug})

    # def __str__(self):
    #     return self.Video_Description + ": " + str(self.id)

from rest_framework import serializers

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field   for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class PhotoSerializers(serializers.ModelSerializer):
    file = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Photo
        fields = "__all__"


from drf_extra_fields.fields import Base64ImageField

class PhotoSerializers(serializers.Serializer):
    file = Base64ImageField(required=False)
    # created = serializers.DateTimeField()
    class Meta:
        model = Photo
        fields = "__all__"

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers
from drf_extra_fields.fields import Base64FileField, Base64ImageField
import filetype

## defenition
class MyCustomBase64FileField(Base64FileField):
    """
    A custom serializer field to handle base64-encoded files.
    """
    ALLOWED_MIME_TYPES = {
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'application/pdf': 'pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    }

    ALLOWED_TYPES = ['pdf', 'docx', 'jpg', 'jpeg', 'png']

    def get_file_extension(self, filename, decoded_file):
        extension = filetype.guess_extension(decoded_file)
        return extension

    def to_internal_value(self, data):
        if isinstance(data, str):
            return super().to_internal_value(data)
        return data

## Usge
class PhotoSerializers(serializers.Serializer):
    file = MyCustomBase64FileField(required=False)
    class Meta:
        model = Photo
        fields = "__all__"


        

class ViewHistory(models.Model):
    user = models.CharField(max_length=150)
    product = models.CharField(max_length=150)
    date_joineds = models.DateTimeField(auto_now_add=True)

