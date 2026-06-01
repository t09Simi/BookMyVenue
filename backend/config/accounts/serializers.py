from rest_framework import serializers 
from .models import Venue

class VenueSerializer(serializers.ModelSerializer):
    amenities = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Venue
        fields = ['id','name', 'description', 'location',
                  'amenities', 'capacity', 'price_per_hour']
        
class VenueRejectSerializer(serializers.Serializer):
    reason = serializers.CharField(
        max_length = 500,
        required = True,
        allow_blank = False,
        trim_whitespace = True,
    )