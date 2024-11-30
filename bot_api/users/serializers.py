from rest_framework import serializers


class LinkTelegramSerializer(serializers.Serializer):
    """Сериализатор ссылки на Telegram."""

    token = serializers.CharField()
    telegram_id = serializers.IntegerField()
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    username = serializers.CharField(allow_blank=True, required=False)
