from rest_framework import serializers
from company.models import Company

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        # fields = ('dev_name', 'email', 'city', 'country', 'description')
        fields = '__all__'


class CompanySerializer_read(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('dev_name', 'email', 'city', 'country', 'description')
        # fields = '__all__'
