from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from pprint import pprint
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
# pprint(router.urls)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product') 
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup="cart")
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

# URL Config

urlpatterns = router.urls + products_router.urls + cart_router.urls


# urlpatterns = [
        #path('', include(router.urls)),
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail')
# ]
