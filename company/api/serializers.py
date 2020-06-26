from rest_framework import serializers
from company.models import Company

class CompanySerializer(serializers.ModelSerializer):
    # password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = Company
        # fields = ('dev_name', 'email', 'city', 'country', 'description')
        fields = '__all__'
        # extra_kwargs={
        #     'password':{'write_only'=True}
        # }

class CompanySerializer_read(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('dev_name', 'email', 'city', 'country', 'description')
        # fields = '__all__'
