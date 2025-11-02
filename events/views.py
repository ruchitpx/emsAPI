from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsOrganizerOrReadOnly, IsPrivateEventAccessible, IsOwnerOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_public', 'organizer']
    search_fields = ['title', 'description', 'location', 'organizer__username']
    ordering_fields = ['start_time', 'created_at', 'title']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Event.objects.all()
        
        # For non-authenticated users, only show public events
        if not self.request.user.is_authenticated:
            return queryset.filter(is_public=True)
        
        # For authenticated users, show public events and private events they have access to
        if self.action == 'list':
            return queryset.filter(
                models.Q(is_public=True) | 
                models.Q(organizer=self.request.user) |
                models.Q(rsvps__user=self.request.user)
            ).distinct()
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rsvp(self, request, pk=None):
        event = self.get_object()
        rsvp_status = request.data.get('status', 'Going')  # Renamed variable
        
        # Check if RSVP already exists
        rsvp, created = RSVP.objects.get_or_create(
            event=event,
            user=request.user,
            defaults={'status': rsvp_status}
        )
        
        if not created:
            rsvp.status = rsvp_status
            rsvp.save()
        
        serializer = RSVPSerializer(rsvp)
        return Response(serializer.data, status=status.HTTP_200_OK)  # Now using the imported status module

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def reviews(self, request, pk=None):
        event = self.get_object()
        reviews = event.reviews.all()
        page = self.paginate_queryset(reviews)
        
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class RSVPViewSet(viewsets.ModelViewSet):
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return RSVP.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event')
        rsvp_status = request.data.get('status', 'Going')
        
        # Validate required fields
        if not event_id:
            return Response(
                {'error': 'Event ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate status
        valid_statuses = ['Going', 'Maybe', 'Not Going']
        if rsvp_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {'error': 'Event not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if RSVP already exists
        try:
            # Try to get existing RSVP
            rsvp = RSVP.objects.get(event=event, user=request.user)
            # Update existing RSVP
            rsvp.status = rsvp_status
            rsvp.save()
            serializer = self.get_serializer(rsvp)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except RSVP.DoesNotExist:
            # Create new RSVP
            rsvp = RSVP.objects.create(
                event=event,
                user=request.user,
                status=rsvp_status
            )
            serializer = self.get_serializer(rsvp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        rsvp_status = request.data.get('status')
        
        # Validate status
        valid_statuses = ['Going', 'Maybe', 'Not Going']
        if rsvp_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.status = rsvp_status
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        event_id = self.request.data.get('event')
        event = get_object_or_404(Event, id=event_id)
        serializer.save(user=self.request.user, event=event)