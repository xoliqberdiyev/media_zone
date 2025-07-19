import mimetypes
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    def get_object_parameters(self, name):
        content_type, _ = mimetypes.guess_type(name)
        return {
            "CacheControl": "max-age=86400",
            "ContentType": content_type or "application/octet-stream"
        }