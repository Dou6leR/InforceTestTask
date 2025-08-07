from rest_framework import serializers
from django.db import transaction

from .models import Menu

from menu_items.models import MenuItem
from menu_items.serializers import MenuItemSerializer

from restaurants.models import Restaurant


class MenuSerializer(serializers.ModelSerializer):
    menu_items = serializers.SerializerMethodField()
    menu_items_input = MenuItemSerializer(many=True, write_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all()
    )

    class Meta:
        model = Menu
        fields = [
            "id", "restaurant", "menu_date", "menu_items", "menu_items_input"
        ]
        read_only_fields = ["id", "menu_date"]

    def create(self, validated_data):
        with transaction.atomic():
            menu_items_data = validated_data.pop("menu_items_input")
            menu = Menu.objects.create(**validated_data)
            menu_items = [
                MenuItem(menu=menu, **item_data) for item_data in menu_items_data
            ]
            MenuItem.objects.bulk_create(menu_items)
            return menu

    def get_menu_items(self, obj):
        menu_items = obj.menuitem_set.all()
        return MenuItemSerializer(menu_items, many=True).data

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if 'menu_items_input' not in data or not data['menu_items_input']:
                raise serializers.ValidationError(
                    {"menu_items_input": "At least one menu item is required."}
                )

            names = [item['name'] for item in data['menu_items_input']]

            if len(names) != len(set(names)):
                raise serializers.ValidationError(
                    {"menu_items_input": "Menu item names must be unique within a menu."}
                )
        return data
