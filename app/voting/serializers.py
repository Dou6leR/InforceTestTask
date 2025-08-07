from rest_framework import serializers
from .models import Vote

from menu_items.serializers import MenuItemSerializer
from menu_items.models import MenuItem


class VoteSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
    )

    class Meta:
        model = Vote
        fields = ["id", "employee", "menu_item", "vote_date"]
        read_only_fields = ["employee"]


class VoteResultSerializer(serializers.Serializer):
    menu_item = MenuItemSerializer(read_only=True)
    vote_count = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        menu_item_id = instance['menu_item']
        menu_item = MenuItem.objects.get(id=menu_item_id)
        representation = {
            'menu_item': MenuItemSerializer(menu_item, context=self.context).data,
            'vote_count': instance['vote_count']
        }
        return representation
