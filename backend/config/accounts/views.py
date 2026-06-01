from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Venue
from .serializers import VenueSerializer, VenueRejectSerializer
from .permissions import IsOwner, IsVenueOwner, IsAdmin

class VenueListView(ListCreateAPIView):
    serializer_class = VenueSerializer
    queryset = Venue.objects.filter(status ="accepted")

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOwner()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VenueSubmitView(APIView):
    permission_classes = [IsVenueOwner]

    def post(self, request, pk):
        venue = get_object_or_404(Venue, pk=pk)
        self.check_object_permissions(request, venue)
        try:
            venue.submit()
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Venue submitted", "status": venue.status}, status=status.HTTP_200_OK)
    

class VenueApproveView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        venue = get_object_or_404(Venue, pk=pk)

        try:
            venue.approve(request.user)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Venue approved", "status": venue.status},
            status=status.HTTP_200_OK)
    
    
class VenueRejectView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        venue = get_object_or_404(Venue, pk=pk)
        serializer = VenueRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            venue.reject(request.user, serializer.validated_data["reason"])
        except ValueError as e:
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Venue Rejected", "status":venue.status, "reason":venue.rejection_reason}, status=status.HTTP_200_OK)


