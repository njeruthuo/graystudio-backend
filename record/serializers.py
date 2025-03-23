from rest_framework import serializers
from .models import Record,Redemption,Client

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['amount_paid']

    def create(self, validated_data):
        # Return the created instance
        return Record.objects.create(**validated_data)


class RedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redemption
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    # Handle multiple records
    records = RecordSerializer(many=True, required=False)
    redemptions = RedemptionSerializer(many=True, required=False)

    class Meta:
        model = Client
        fields = ['name', 'number', 'date_joined',
                  'total_points', 'records', 'redemptions']

    def to_representation(self, instance):
        """Customize how the records field is represented in the output."""
        representation = super().to_representation(instance)
        representation['records'] = RecordSerializer(
            instance.records.all(), many=True).data
        return representation

    def create(self, validated_data):
        record_data = validated_data.pop("records", None)
        redemption_data = validated_data.pop("redemptions", None)

        # Create the client
        client, _ = Client.objects.get_or_create(**validated_data)

        # Create a single record if record_data is provided
        if record_data:
            for record in record_data:  # Handle multiple records
                record['client'] = client  # Add the client to the record data
                Record.objects.create(**record)
            client.update_total_points()  # Update total_points after creating the record

        # Create multiple redemptions if redemption_data is provided
        if redemption_data:
            for redemption in redemption_data:
                Redemption.objects.create(client=client, **redemption)
            client.update_total_points()  # Update total_points after creating redemptions

        return client  # Return the created client instance
