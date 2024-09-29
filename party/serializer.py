from rest_framework import serializers


from .models import Party, Party_user, Party_reservation, online_party_payment


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = [
            "id",
            "name",
            "performer",
            "location",
            "datetime",
            "number_of_tickets",
            "price",
            "description",
            "image",
            "avilable",
        ]


class User_partySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party_user
        fields = ["party", "user", "total"]


class show(serializers.Serializer):
    username = serializers.CharField()
    name = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


# -----------------------------(party reservation)-----------------------------
# serializer
class bookpartyserializer(serializers.ModelSerializer):
    class Meta:
        model = Party_reservation
        fields = ["pk", "tickets_reserved", "pay_method", "price"]


class partypaymentserializer(serializers.ModelSerializer):
    class Meta:
        model = online_party_payment
        fields = ["visa_card", "payment_status"]

    def validate(self, attrs):
        visa_card = attrs.get("visa_card")
        payment_status = attrs.get("payment_status")
        # Check if visa_card is 16 digits
        if not (visa_card and len(visa_card) == 16 and visa_card.isdigit()):
            attrs["payment_status"] = "Failed"

            raise serializers.ValidationError(
                {"visa_card": "Visa card must be exactly 16 digits."}
            )
        else:
            attrs["payment_status"] = "Complete"
        return attrs

    def create(self, validated_data):
        # Create a new payment entry
        return online_party_payment.objects.create(**validated_data)
