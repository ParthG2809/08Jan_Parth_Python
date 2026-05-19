from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'specialization',
            'experience_years',
            'email',
            'phone_number',
            'clinic_address',
            'consultation_fee',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience years cannot be negative.")
        return value

    def validate_consultation_fee(self, value):
        if value < 0:
            raise serializers.ValidationError("Consultation fee cannot be negative.")
        return value

    def validate(self, data):
        """
        Object-level validation: Ensure active doctors have either a phone number or a clinic address
        so patients can actually contact/find them.
        """
        # When updating, we might receive partial data. Let's handle instances safely.
        is_active = data.get('is_active')
        phone = data.get('phone_number')
        address = data.get('clinic_address')

        # If this is an update and some fields are missing from data dictionary, we fall back to instance properties
        if self.instance:
            if is_active is None:
                is_active = self.instance.is_active
            if phone is None:
                phone = self.instance.phone_number
            if address is None:
                address = self.instance.clinic_address
        else:
            # For creation, default is_active is True if not provided
            if is_active is None:
                is_active = True

        if is_active and not phone and not address:
            raise serializers.ValidationError(
                "An active doctor profile must provide at least one contact method (phone number or clinic address)."
            )
        return data
