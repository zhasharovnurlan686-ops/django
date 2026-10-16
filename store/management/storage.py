import mimetypes

from django.core.files.base import ContentFile
from django.core.files.storage import Storage

from .models import MediaBlob


class DatabaseStorage(Storage):
    def _open(self, name, mode="rb"):
        try:
            image = MediaBlob.objects.get(path=name)
        except MediaBlob.DoesNotExist:
            raise FileNotFoundError(name)

        return ContentFile(bytes(image.data), name=name)

    def _save(self, name, content):
        data = b"".join(content.chunks())

        content_type = (
            getattr(content, "content_type", None)
            or mimetypes.guess_type(name)[0]
            or "application/octet-stream"
        )

        MediaBlob.objects.update_or_create(
            path=name,
            defaults={
                "data": data,
                "content_type": content_type,
                "size": len(data),
            },
        )

        return name

    def exists(self, name):
        return MediaBlob.objects.filter(path=name).exists()

    def delete(self, name):
        MediaBlob.objects.filter(path=name).delete()

    def size(self, name):
        return MediaBlob.objects.get(path=name).size

    def url(self, name):
        from django.urls import reverse

        return reverse("database_image", kwargs={"path": name})