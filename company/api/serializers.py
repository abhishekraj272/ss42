from rest_framework import serializers
from company.models import Company

class CompanySerializer(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Company
        # fields = ('company_name', 'dev_name', 'email', 'city', 'country', 'description', 'company_name', 'api_key')
        fields = '__all__'

class CompanySerializer_read(serializers.ModelSerializer):
    company_name = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Company
        fields = ('dev_name', 'email', 'city', 'country', 'description', 'company_name')
