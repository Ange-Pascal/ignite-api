from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Video
        fields = [
            "id",
            "lesson",
            "video",
            "video_url",
            "duration",
            "provider",
            "created_at",
        ]
        read_only_fields = ["video_url", "provider", "created_at"]

    def validate_lesson(self, lesson):
        user = self.context["request"].user

        if user.roles.filter(name="admin").exists():
            return lesson

        if user.roles.filter(name="instructor").exists():
            if lesson.module.course.user != user:
                raise serializers.ValidationError(
                    "Vous ne pouvez pas ajouter une vidéo à ce cours."
                )

        return lesson

    def create(self, validated_data):
        request = self.context["request"]
        file = validated_data.pop("video", None)

        from .services.storage import handle_video_upload

        uploaded = handle_video_upload(file)

        video = Video.objects.create(
            uploaded_file=uploaded,
            provider="local",
            **validated_data
        )

        if uploaded:
            video.video_url = request.build_absolute_uri(
                video.uploaded_file.url
            )
            video.save()

        return video
