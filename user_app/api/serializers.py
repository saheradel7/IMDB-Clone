from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type' : 'password'},write_only = True)

    class Meta:
        model = User
        fields =['username', 'email' , 'password' , 'password2']

        extra_kwargs =  {
            'password' : {'write_only':True} 
        }

    def save(self):
        p1 = self.validated_data['password']
        p2 = self.validated_data['password2']

        if p1 != p2:
            raise ValidationError("paswords doesnot match") 
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise ValidationError("this email aready exits")


        acount = User(email = self.validated_data['email'] , username=self.validated_data['username'])
        acount.set_password(self.validated_data['password'])
        acount.save()
        return acount
