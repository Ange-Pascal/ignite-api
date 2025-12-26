from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"
        read_only_fields = ["video_url"]

    def create(self, validated_data):
        provider = validated_data.get("provider", "local")
        uploaded_file = validated_data.pop("uploaded_file", None)

        video = Video.objects.create(**validated_data)

        if provider == "local" and uploaded_file:
            video.uploaded_file = uploaded_file
            video.video_url = video.uploaded_file.url
            video.save()
        elif provider == "s3" and uploaded_file:
            # Si S3 configuré via django-storages, la même logique s'applique
            video.uploaded_file = uploaded_file
            video.video_url = video.uploaded_file.url
            video.save()

        return video
