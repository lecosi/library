from django.db import models

from utils.models import BaseModel


class Author(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(BaseModel):
    title = models.CharField(max_length=100)
    external_id = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, null=True)
    editor = models.CharField(max_length=100)
    category = models.ManyToManyField(Category, null=True)
    description = models.TextField(null=True)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ManyToManyField(Author, null=True)

    def __str__(self):
        return self.title
