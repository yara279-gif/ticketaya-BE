from . models import match_reservation,online_match_payment
from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#serializer
class bookmatchserializer (serializers.ModelSerializer):
    # price =  serializers.defaultdict(max_digits=7,decimal_places=2)


    class Meta:
        model = match_reservation
        fields = ['tickets_reserved','pay_method']
    
class matchpaymentserializer(serializers.ModelSerializer):

    class Meta:
        model = online_match_payment
        fields = ['visa_card', 'payment_status']

    def validate(self, attrs):
        visa_card = attrs.get("visa_card")
        payment_status = attrs.get("payment_status")

        # Check if visa_card is 16 digits
        if not (visa_card and len(visa_card) == 16 and visa_card.isdigit()):
            attrs['payment_status'] ="Failed"
            
            raise serializers.ValidationError({"visa_card": "Visa card must be exactly 16 digits."})
        return attrs

    def create(self, validated_data):
        # Create a new payment entry
        return online_match_payment.objects.create(**validated_data)



