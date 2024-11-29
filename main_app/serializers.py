from rest_framework import serializers
from .models import AgentApplication

class AgentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentApplication
        fields = [
            'id', 'user', 'company_name', 'company_address', 
            'company_email', 'company_contact', 'npwp', 
            'photo', 'status', 'created_at', 'updated_at'
        ]