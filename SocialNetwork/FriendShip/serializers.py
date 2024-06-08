from rest_framework import serializers
from .models import FriendShipRequest


class FriendShipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShipRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp', 'status']
        read_only_fields = ['timestamp', 'status']