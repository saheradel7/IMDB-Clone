from rest_framework.response import Response
from watchlist_app.models import WatchList,StreamPlatform,Review
from .serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from watchlist_app.api.permissions import AdminOrReadOnly,ReviwUserOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination


#region FUNCTIO BASE VIEW
# @api_view(['GET' , 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         data = Movie.objects.all()
#         serializer = MovieSerializer(data, many = True)
#         return Response(serializer.data , status=status.HTTP_200_OK)
    
#     if request.method == 'POST':
#         data = request.data
#         serializer = MovieSerializer(data = data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data , status=status.HTTP_200_OK)
#         return Response(serializer.errors)




# @api_view(['GET' , 'PUT' , 'DELETE'])
# def movie_detail(request , pk):
#     if request.method == 'GET':
#         data = Movie.objects.filter(id =pk)
#         serializer = MovieSerializer(data, many = True)
#         return Response(serializer.data ,status= status.HTTP_200_OK)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(id =pk)
#         data = request.data
#         serializer = MovieSerializer(movie , data =data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data , status= status.HTTP_200_OK)
#         return Response({'details':'error while PUT method'} , status= status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         Movie.objects.filter(id = pk ).delete()
#         return Response({'detals' : 'movie deleted'} ,status= status.HTTP_204_NO_CONTENT)
#endregion



class StreamPlatformAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        spf = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(spf , many = True ,context={'request': request})
        return Response(serializer.data , status= status.HTTP_200_OK)
    
    
    def post(self ,request):
        data = request.data
        serializer = StreamPlatformSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= status.HTTP_201_CREATED)
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetail(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request , pk):
        spf = StreamPlatform.objects.get(id = pk)
        serializer = StreamPlatformSerializer(spf,context={'request': request})
        return Response(serializer.data , status= status.HTTP_200_OK)
    
    def put(self , request, pk):
        data = request.data
        spf = StreamPlatform.objects.get(id= pk)
        serializer = StreamPlatformSerializer(spf , data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response (serializer.errors)
    
    def delete(self , request ,pk):
        StreamPlatform.objects.get(id= pk).delete()
        return Response({'detalis': 'deleted'}, status= status.HTTP_204_NO_CONTENT)





class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]

    def get(self,request):
        data = WatchList.objects.all()
        serializer = WatchListSerializer(data , many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self , request):
        data = request.data
        serializer = WatchListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= status.HTTP_201_CREATED)
        return Response(serializer.errors  , status= status.HTTP_400_BAD_REQUEST)

class WatchListDetails(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request, pk):
        movie = WatchList.objects.get(id = pk)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data , status= status.HTTP_200_OK)
    
    def put(self ,request , pk):
        movie = WatchList.objects.get(id = pk)
        data = request.data
        serializer = WatchListSerializer(movie , data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self , request , pk):
        WatchList.objects.get(id= pk).delete()
        return Response({'details': 'movie deleted'},  status=status.HTTP_204_NO_CONTENT)



class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    filterset_fields = ['review_user__username', 'active']
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist_id = pk)
    


class ReviewCreate(generics.CreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated] 
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(id = pk)
        review_user =  self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")


        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else :
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)
         


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviwUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = 'review-detail'

#region Review with MIXINS
# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    

# class ReviewDetails(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#endregion