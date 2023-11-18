# from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
# from .views import Registration_view,logout_view

# urlpatterns = [
#    path('login/', obtain_auth_token , name= 'login'),
#    path('register/', Registration_view  , name= 'register'),
#    path('logout/', logout_view  , name= 'register')

# ]



from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # ... your other URL patterns ...
]
