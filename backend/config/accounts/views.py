from rest_framework.generics import ListAPIView
from .models import Venue
from .serializers import VenueSerializer

class VenueListView(ListAPIView):
    serializer_class = VenueSerializer
    queryset = Venue.objects.filter(status ="accepted")
