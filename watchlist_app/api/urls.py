from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from.views import WatchListDetails, WatchListAV ,StreamPlatformAV ,StreamPlatformDetail,ReviewList,ReviewDetails,ReviewCreate




# router = DefaultRouter()
# router.register('stream' ,  StreamPlatformAV.as_view() , basename='streamplatform')

urlpatterns = [
    path('list', WatchListAV.as_view() , name='watchlistview'),
    path('<int:pk>', WatchListDetails.as_view() , name='watchlistdetail'),


    # path('',include(router.urls)),
    path('stream', StreamPlatformAV.as_view() , name='platformview'),
    path('stream/<int:pk>', StreamPlatformDetail.as_view() , name='platformdetail'),


    path('stream/<int:pk>/review-create', ReviewCreate.as_view() , name='review-create'),
    path('stream/<int:pk>/review', ReviewList.as_view() , name='platformdetail'),
    path('stream/review/<int:pk>', ReviewDetails.as_view() , name='platformdetail'),



    # path('review', ReviewList.as_view() , name='revewlist'),
    # path('review/<int:pk>', ReviewDetails.as_view() , name='revewdetail'),
]
