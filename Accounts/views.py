from django.shortcuts import render
from rest_framework import viewsets,status,mixins,generics
from .serializers import DocRegisterSerializer,Staff_registrationSerializer,ClnicloginSerializer,ClniupSerializer,DocterupSerializer,StaffupSerializer,doctordelSerializer,ClniViewsSerializer,doctorviewSerializer,StaffviewupSerializer
from .models import UserAccount,Clinic,Doctor,Staff
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class Doc_Registartion_API(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=DocRegisterSerializer
    def post(self, request,format=None):
        serializer = DocRegisterSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({'status': status.HTTP_200_OK,'message':'Registration Successful','data':{"Token":token}},status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST,'message':serializer.errors,'data':{"errors":serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
    

class Staff_Registartion_API(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=Staff_registrationSerializer
    def post(self, request,format=None):
        serializer = Staff_registrationSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({'status': status.HTTP_201_CREATED,'message':'Registration Successful','data':{"Token":token}},status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST,'message':serializer.errors,'data':{"errors":serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)



# login views

class ClinicLoginView(GenericAPIView):
   serializer_class=ClnicloginSerializer
   def post(self,request,format=None):
      serializer=ClnicloginSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         email=serializer.data.get('email')
         password=serializer.data.get('password')
         user=authenticate(email=email,password=password)
         if user is not None:
            token=get_tokens_for_user(user)
            return Response({'status': status.HTTP_200_OK,'message':'Login Success','data':{"Token":token}},status=status.HTTP_200_OK)
         else:
             return Response({'status': status.HTTP_404_NOT_FOUND,'message':'non_field_errors','data':{"errors":'Email or password is not Valid'}}, status=status.HTTP_404_NOT_FOUND)
            
         

# #Accounts update


class clinic_update(GenericAPIView,mixins.UpdateModelMixin):
   permission_classes=[IsAuthenticated]
   serializer_class =ClniupSerializer
   def put(self,request,*args,**kwargs):
      chk=request.user.Block
      if chk == True:
            return Response({'status': status.HTTP_403_FORBIDDEN,'message':'errors','data':{"errors":'Plez contect Wiz 91'}}, status=status.HTTP_403_FORBIDDEN)
      user = Clinic.objects.get(id=self.request.user.id)
      serializer = self.serializer_class(instance=user, data=request.data,context={'user':request.user})
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'status': status.HTTP_200_OK,'message':'updated','data':serializer.data}, status=status.HTTP_200_OK)
     
  
  


class Doctor_update(GenericAPIView,mixins.UpdateModelMixin):
   permission_classes=[IsAuthenticated]
   serializer_class =DocterupSerializer
   def put(self,request,*args,**kwargs):
      chk=request.user.is_doctor
      if chk != True:
          return Response({'status': status.HTTP_403_FORBIDDEN,'message':'non_field_errors','data':'Not a doctor profile'}, status=status.HTTP_403_FORBIDDEN)
      user = Doctor.objects.get(id=self.request.user.id)
      serializer = self.serializer_class(instance=user, data=request.data,context={'user':request.user})
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'status': status.HTTP_200_OK,'message':'updated','data':serializer.data}, status=status.HTTP_200_OK)
  

class Staff_update(GenericAPIView,mixins.UpdateModelMixin):
   permission_classes=[IsAuthenticated]
   serializer_class =StaffupSerializer
   def put(self,request,*args,**kwargs):
      chk=request.user.is_staff
      if chk != True:
          return Response({'status': status.HTTP_403_FORBIDDEN,'message':'non_field_errors','data':'Not a staff profile'}, status=status.HTTP_403_FORBIDDEN)
      user = Staff.objects.get(id=self.request.user.id)
      serializer = self.serializer_class(instance=user, data=request.data,context={'user':request.user})
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'status': status.HTTP_200_OK,'message':'staff_updated','data':serializer.data}, status=status.HTTP_200_OK)


#view
class Doctor_account_views(GenericAPIView,mixins.RetrieveModelMixin):
    queryset=Doctor.objects.all()
    serializer_class=doctorviewSerializer
    permission_classes=[IsAuthenticated]  
    def get(self,request,*args,**kwargs):
        chk_avilable=Doctor.objects.filter(id=kwargs['pk'])
        if chk_avilable.exists():
            staff_obj=Doctor.objects.select_related().get(id=kwargs['pk'])
            if staff_obj.clinic.id==request.user.id:
                if request.user.is_clinic != True or request.user.Block==True: 
                    return Response({'status': status.HTTP_403_FORBIDDEN,'message':'non_profile_errors or Block','data':'the profile is block or not a clnic profile'}, status=status.HTTP_403_FORBIDDEN)
                return Response({'status': status.HTTP_200_OK,'message':'ok','data':self.retrieve(self,request,*args,**kwargs)}, status=status.HTTP_200_OK)
                # return self.retrieve(self,request,*args,**kwargs)
            return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'non_field_errors','data':'doctor not belong you'}, status=status.HTTP_401_UNAUTHORIZED)
            
            
class Doctor_all_account_views(generics.ListAPIView):
    serializer_class=ClniViewsSerializer
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        if request.user.is_clinic != True or request.user.Block==True: 
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'non_profile_errors or Block','data':'the profile is block or not a clnic profile'}, status=status.HTTP_403_FORBIDDEN)
        doc_obj=Doctor.objects.filter(clinic=request.user.id).values()
        return Response({'status': status.HTTP_200_OK,'message':'ok','data':doc_obj}, status=status.HTTP_200_OK)
        


class Staff_account_views(GenericAPIView,mixins.RetrieveModelMixin):
    queryset=Staff.objects.all()
    serializer_class=StaffviewupSerializer
    permission_classes=[IsAuthenticated]  
    def get(self,request,*args,**kwargs):
        chk_avilable=Staff.objects.filter(id=kwargs['pk'])
        if chk_avilable.exists():
            staff_obj=Staff.objects.select_related().get(id=kwargs['pk'])
            if staff_obj.clinic.id==request.user.id:
                if request.user.is_clinic != True or request.user.Block==True: 
                    return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'non_profile_errors or Block','data':'the profile is block or not a clnic profile'}, status=status.HTTP_403_FORBIDDEN)
                return Response({'status': status.HTTP_200_OK,'message':'retrived','data':self.retrieve(self,request,*args,**kwargs)}, status=status.HTTP_200_OK)
                # return self.retrieve(self,request,*args,**kwargs)
            return Response({'status': status.HTTP_403_FORBIDDEN,'message':'non_field_errors','data':'staff not belong you'}, status=status.HTTP_403_FORBIDDEN)
    
class Staff_all_account_views(generics.ListAPIView):
    serializer_class=StaffviewupSerializer
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        if request.user.is_clinic != True or request.user.Block==True: 
            return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'non_profile_errors or Block','data':'the profile is block or not a clnic profile'}, status=status.HTTP_403_FORBIDDEN)
        doc_obj=Staff.objects.filter(clinic=request.user.id).values()
        return Response({'status': status.HTTP_200_OK,'message':'ok','data':doc_obj}, status=status.HTTP_200_OK)
    
    
#Delete

class doctor_delete(GenericAPIView,mixins.DestroyModelMixin):
    permission_classes=[IsAuthenticated]
    queryset=Doctor.objects.all()
    def delete(self,request,*args,**kwargs):
        chk_avilable=Doctor.objects.filter(id=kwargs['pk'])
        if chk_avilable.exists():
            doc_obj=Doctor.objects.select_related().get(id=kwargs['pk'])
            if doc_obj.clinic.id==request.user.id:
                if request.user.is_clinic != True or request.user.Block==True: 
                    return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'non_profile_errors or Block','data':'the profile is block or not a clnic profile'}, status=status.HTTP_403_FORBIDDEN)
                del_item=self.destroy(self,request,*args,**kwargs)
                return Response({'status': status.HTTP_204_NO_CONTENT,'message':'sucessfully_deleted','data':str(del_item)}, status=status.HTTP_204_NO_CONTENT)
            return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'non_field_errors','data':'doctor not belong you'}, status=status.HTTP_401_UNAUTHORIZED) 
        return Response({'status': status.HTTP_404_NOT_FOUND,'message':'non_field_errors','data':'Not Found'}, status=status.HTTP_404_NOT_FOUND)                       
       

class staff_delete(GenericAPIView,mixins.DestroyModelMixin):
    permission_classes=[IsAuthenticated]
    queryset=Staff.objects.all()
    def delete(self,request,*args,**kwargs):
        chk_avilable=Staff.objects.filter(id=kwargs['pk'])
        if chk_avilable.exists():
            doc_obj=Staff.objects.select_related().get(id=kwargs['pk'])
            if doc_obj.clinic.id==request.user.id:
                if request.user.is_clinic != True or request.user.Block==True: 
                    return Response ({'status': status.HTTP_403_FORBIDDEN,'message':'non_profile_errors or Block','data':'the profile is block or not a clnic profile'}, status=status.HTTP_403_FORBIDDEN)
                del_item=self.destroy(self,request,*args,**kwargs)
                return Response ({'status': status.HTTP_204_NO_CONTENT,'message':'sucessfully_deleted','data':str(del_item)}, status=status.HTTP_204_NO_CONTENT)
            return Response({'status': status.HTTP_401_UNAUTHORIZED,'message':'non_field_errors','data':'staff not belong you'}, status=status.HTTP_401_UNAUTHORIZED)                        
        return Response({'status': status.HTTP_404_NOT_FOUND,'message':'non_field_errors','data':'Not Found'}, status=status.HTTP_404_NOT_FOUND)