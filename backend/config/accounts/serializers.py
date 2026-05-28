from rest_framework import serializers 
from .models import Venue

class VenueSerializer(serializers.ModelSerializer):
    amenities = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Venue
        fields = ['id','name', 'description', 'location',
                  'amenities', 'capacity', 'price_per_hour']