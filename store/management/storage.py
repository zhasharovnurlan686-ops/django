from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.urls import reverse

from .models import MediaBlob


class DatabaseStorage(Storage):
    """
    Хранит файлы в PostgreSQL вместо файловой системы Render.
    """

    def _open(self, name, mode="rb"):
        item = MediaBlob.objects.get(path=name)
        return ContentFile(bytes(item.data), name=name)

    def _save(self, name, content):
        if hasattr(content, "chunks"):
            data = b"".join(content.chunks())
        else:
            data = content.read()

        content_type = getattr(
            content, "content_type", "application/octet-stream"
        ) or "application/octet-stream"

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
        return MediaBlob.objects.only("size").get(path=name).size

    def url(self, name):
        return reverse("database_image", kwargs={"path": name})