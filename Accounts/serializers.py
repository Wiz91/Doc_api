from rest_framework import serializers,status
from rest_framework.validators import UniqueValidator
from .models import UserAccount,Clinic,Staff,Doctor
from django.contrib.auth.hashers import make_password


# Doc serializers registration



class DocRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = Doctor
        fields = ['email','contact','first_Name','last_Name','designation','experience','qualification','specialist','password','password2']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user=self.context.get('user')
        if user.Block == True:
            raise serializers.ValidationError("plzz contect wiz91")
        if user.is_clinic != True:
            raise serializers.ValidationError("You are not clinic profile")
        if password != password2:
            raise serializers.ValidationError("password and confirm password dosen't match")
        return attrs
    
    def create(self, validated_data):
        user=self.context.get('user')
        if user.Block != True:
            return Doctor.objects.create(email=self.validated_data['email'],contact=self.validated_data['contact'],first_Name=self.validated_data['first_Name'],last_Name=self.validated_data['last_Name'],designation=self.validated_data['designation'],experience=self.validated_data['experience'],qualification=self.validated_data['qualification'],specialist=self.validated_data['specialist'],password=make_password(self.validated_data['password']),clinic=user)
        raise serializers.ValidationError("Please contect to Wiz 91")


# staff serializers registration

class Staff_registrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = Staff
        fields = ['email','contact','first_Name','last_Name','password','password2']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user=self.context.get('user')
        if user.Block == True:
            raise serializers.ValidationError("plzz contect wiz91")
        if user.is_clinic != True:
            raise serializers.ValidationError("You are not clinic profile")
        if password != password2:
            raise serializers.ValidationError("password and confirm password dosen't match")
        return attrs
    
    def create(self, validated_data):
        user=self.context.get('user')
        if user.Block != True:
            return Staff.objects.create(email=self.validated_data['email'],contact=self.validated_data['contact'],first_Name=self.validated_data['first_Name'],last_Name=self.validated_data['last_Name'],password=make_password(self.validated_data['password']),clinic=user)
        raise serializers.ValidationError("Please contect to Wiz 91")

# logins

class ClnicloginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=UserAccount
        fields=['email','password']

#  Account update serializer


class ClniupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Clinic
        fields=['email','contact','clinic_Name','Owner_First_Name','Owner_Last_Name','Address','map']

    def validate(self, attrs):
        return attrs


class DocterupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields=['email','contact','first_Name','last_Name','designation','experience','qualification','specialist','contact']

    def validate(self, attrs):
        return attrs
    

class StaffupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Staff
        fields=['email','contact','first_Name','last_Name']

    def validate(self, attrs):
        return attrs
    
#views
 
class StaffupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Staff
        fields=['email','contact','first_Name','last_Name']

    def validate(self, attrs):
        return attrs
 
 
class ClniViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Clinic
        fields=['id','email','contact','clinic_Name','Owner_First_Name','Owner_Last_Name','Address','map']

    def validate(self, attrs):
        return attrs
 
class doctorviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields=['id','password','email','contact','first_Name','last_Name','designation','experience','qualification','specialist','contact']

    def validate(self, attrs):
        return attrs 
 
class StaffviewupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Staff
        fields=['id','password','email','contact','first_Name','last_Name']

    def validate(self, attrs):
        return attrs
 
 #delete   
class doctordelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields=['email','contact','first_Name','last_Name','designation','experience','qualification','specialist','contact']

    def validate(self, attrs):
        return attrs
    
    
    def delete(self, validated_data):
        print('h')
        raise serializers.ValidationError("password and confirm password dosen't match")