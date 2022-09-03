from rest_framework import serializers
from app.models import slots, appointment


class SlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = slots
        fields = '__all__'
        depth = 1

class PostSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = slots
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = appointment
        fields = '__all__'
        depth = 1


class PostAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = appointment
        fields = '__all__'
