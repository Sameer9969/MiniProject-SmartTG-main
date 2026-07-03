from django.urls import path
from . import views

urlpatterns = [
    path('Home/', views.home, name='home'),
    
    path('wishlist/', views.wishlist, name='wishlist'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('place/<int:place_id>/', views.place_detail, name='place_detail'),
    path('add-to-wishlist/<int:place_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:place_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('search/', views.search_places, name='search_places'),
    path('profile/', views.user_profile, name='user_profile'),
    path('place/<int:place_id>/upload_review/', views.upload_review, name='upload_review'),
    path('place/<int:place_id>/view_reviews/', views.view_reviews, name='view_reviews'),
]
