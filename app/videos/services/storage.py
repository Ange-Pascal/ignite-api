from django.conf import settings

def handle_video_upload(file):
    if settings.USE_CLOUD_STORAGE:
        return upload_to_cloud(file)
    return upload_to_local(file)

def upload_to_local(file):
    return file


def upload_to_cloud(file):
    # GCS Implementation plus tard

    raise NotImplementedError("Cloud storage not configured yet")

