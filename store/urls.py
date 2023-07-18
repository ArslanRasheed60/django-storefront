from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from pprint import pprint
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)


# URL Config

urlpatterns = router.urls


# urlpatterns = [
        #path('', include(router.urls)),
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail')
# ]
