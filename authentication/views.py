from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import  UserSerializer
from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    def post(self, request):
        # Retrieve the user from the request
        user = request.user
        
        # Check if the user already has a profile
        if Profile.objects.filter(user=user).exists():
            return Response({'error': 'Profile already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile_data = request.data
        
        # Add the user information to the profile data
        profile_data['user'] = user.id  # 
        
        serializer = ProfileSerializer(data=profile_data)
        
        # Validate and save the profile
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)