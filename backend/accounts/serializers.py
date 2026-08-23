from rest_framework import serializers
from .models import Parent

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'username', 'email', 'phone', 'address', 'password']
        extra_kwargs = {'password': {'write_only': True}}
                       

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Parent(**validated_data)
        user.set_password(password)
        user.save()
        return user
