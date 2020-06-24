from rest_framework import serializers
from company.models import Company

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
       fields = ('dev_name', 'email', 'city', 'country', 'description', 'password')
        # fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CompanySerializer_read(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('dev_name', 'email', 'city', 'country', 'description')
        # fields = '__all__'
