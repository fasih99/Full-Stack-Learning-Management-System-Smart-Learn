from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from ckeditor.fields import RichTextField
import os;

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
           ordering = ['title']

    def __str__(self):
        return self.title



class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True)

    class Meta:
         ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
         ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

class Content(models.Model):
    # this is general/base content class for diverse content
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to = {'model__in':('text',
                                                                                                            'file',
                                                                                                            'image',
                                                                                                            'video',)})
    order = OrderField(blank=True, for_fields=['module'])

    # We add a limit_choices_to   argument to limit the ContentType
    # objects that can be used for the generic relationship.
    # We use the model__in   field lookup to filter the query to the ContentType
    # objects with a model attribute that is 'text', 'video', 'image', or 'file'.

    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')

    #Only the content_type and object_id fields have a corresponding column in the database table of this model.
    #The item field allows you to retrieve or set the related object directly,
    #and its functionality is built on top of the other two fields.

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                                # Django allows us to specify a placeholder for the model class name
                                # in the related_name attribute as %(class)s.
                                # By doing so, related_name for each child model will be generated automatically.
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Each child model contains the fields defined in the ItemBase   class in addition to its own fields.
    # A database table will be created for the Text, File, Image, and Video   models respectively.
    # There will be no database table associated to the ItemBase   model since it is an abstract model.

    class Meta:
        abstract = True

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
        self._meta.model_name), {'item':self})

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = RichTextField(blank=True, null=True)
    # content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='media/files')


class Image(ItemBase):
       file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()
