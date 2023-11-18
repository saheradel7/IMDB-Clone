from rest_framework.decorators import api_view
from  .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
@api_view(['POST'])
def Registration_view(request):
    data = request.data
    serializer = RegistrationSerializer(data= data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data ,status= status.HTTP_201_CREATED)
    

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)