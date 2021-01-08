from rest_framework import serializers
from .models import Corona

class CoronaSerializer(serializers.ModelSerializer):
	class Meta:
		model=Corona
		fields='__all__'