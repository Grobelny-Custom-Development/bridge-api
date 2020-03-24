from rest_framework import serializers
from activity.models import Cards


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = ('id', 'content',)
