from rest_framework import serializers
from markdown.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(max_length=500, write_only=True)
    class Meta:
        model = Document
        fields = "__all__"
