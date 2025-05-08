from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tags(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)