from rest_framework.views import APIView
from rest_framework.response import Response
from markdown.models import Document, Tags
from markdown.serializer import DocumentSerializer


class DocumentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        doc_id = kwargs.get("pk")
        if doc_id is None:
            sort_asc = request.query_params.get("sort_asc", False)
            tag = request.query_params.get("tag", None)
            all_docs = Document.objects.all()
            if tag:
                all_docs.filter(tags__name=tag)

            if sort_asc:
                all_docs.order_by('created_at')
            else:
                all_docs.order_by('-created_at')

            response = []
            for doc in all_docs:
                data = DocumentSerializer(doc).data
                all_tags = []
                for tag in doc.tags_set.all():
                    all_tags.append(tag.name)
                data["tags"] = ",".join(all_tags)
                response.append(data)

            return Response(data=response, status=200)
        else:
            doc = Document.objects.filter(id=doc_id).first()
            if doc is None:
                return Response(data={"details": "Document not found against id"}, status=404)

            all_tags = []
            tags = doc.tags_set.all()
            for tag in tags:
                all_tags.append(tag.name)

            response = DocumentSerializer(doc).data
            response["tags"] = ",".join(all_tags)
            return Response(data=response, status=200)


    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(request.data)
        if not serializer.is_valid():
            return Response(data={"details": "Invalid data"}, status=400)

        tags = serializer.validated_data.get("tags")
        serializer.save()

        for tag in tags.split(","):
            Tags.objects.create(name=tag, document=serializer.instance.id)

        response = serializer.data
        response["tags"] = tags
        return Response(data=response, status=200)

    def patch(self, request, *args, **kwargs):
        doc_id = kwargs.get("pk")
        if doc_id is None:
            return Response(data={"details": "id is required."}, status=400)

        doc = Document.objects.filter(id=doc_id).first()
        if doc is None:
            return Response(data={"details": "Document not found against id"}, status=404)

        serializer = DocumentSerializer(request.data, instance=doc)
        if not serializer.is_valid():
            return Response(data={"details": "Invalid data"}, status=400)

        tags = serializer.validated_data.get("tags")
        serializer.save()

        Tags.objects.filter(document=serializer.instance.id).delete()

        for tag in tags:
            Tags.objects.create(name=tag, document=serializer.instance.id)

        response = serializer.data
        response["tags"] = tags
        return Response(data=response, status=200)

    def delete(self, request, *args, **kwargs):
        doc_id = kwargs.get("pk")
        if doc_id is None:
            return Response(data={"details": "id is required."}, status=400)

        doc = Document.objects.filter(id=doc_id).first()
        if doc is None:
            return Response(data={"details": "Document not found against id"}, status=404)

        doc.delete()
        return Response(data={}, status=204)
