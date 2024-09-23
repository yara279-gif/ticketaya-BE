from .models import match_reservation
from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


# serializer
class bookmatchserializer(serializers.ModelSerializer):
    # price =  serializers.defaultdict(max_digits=7,decimal_places=2)

    class Meta:
        model = match_reservation
        fields = ["tickets_reserved"]
