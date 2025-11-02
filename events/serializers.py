from rest_framework import serializers
from .models import Event, RSVP, Review
from users.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    rsvp_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'organizer', 'location',
            'start_time', 'end_time', 'is_public', 'created_at',
            'updated_at', 'rsvp_count', 'average_rating'
        ]
        read_only_fields = ['organizer', 'created_at', 'updated_at']

    def get_rsvp_count(self, obj):
        return obj.rsvps.count()

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    def validate(self, data):
        if data.get('end_time') and data.get('start_time'):
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError("End time must be after start time")
        return data

class RSVPSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    
    class Meta:
        model = RSVP
        fields = ['id', 'event', 'user', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'event', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'event', 'user', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'event', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value