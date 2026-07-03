from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Place, Wishlist
from .forms import ContactForm,UserProfileForm
from django.db.models import Q  #Q allows flexible search across multiple fields.
from .models import UserProfile,Review
from .forms import ReviewForm



# -------------------------------
# Home Page – Show All Places
# -------------------------------
def home(request):
    places = Place.objects.all()
    if request.user.is_authenticated:
        wishlist_places = Wishlist.objects.filter(user=request.user).values_list('place_id', flat=True)
    else:
        wishlist_places = []
    return render(request, 'home/homePage.html', {
        'places': places,
        'wishlist_places': wishlist_places
    })



# -------------------------------
# Wishlist Page
# -------------------------------
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'home/wishlist.html', {'wishlist_items': wishlist_items})


# -------------------------------
# About Page
# -------------------------------
def about(request):
    return render(request, 'home/about.html')


# -------------------------------
# Contact Page
# -------------------------------
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Your message has been sent successfully! We'll reply soon.")
            return redirect('contact')
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})


# -------------------------------
# Place Detail Page
# -------------------------------
def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    is_wishlisted = False

    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, place=place).exists()

    context = {
        'place': place,
        'is_wishlisted': is_wishlisted,
    }
    return render(request, 'home/place_detail.html', context)


# -------------------------------
# Add to Wishlist
# -------------------------------
@login_required
def add_to_wishlist(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, place=place)
    if created:
        messages.success(request, f"❤️ Added {place.name} to your wishlist!")
    else:
        messages.info(request, f"{place.name} is already in your wishlist.")
    return redirect('wishlist')


# -------------------------------
# Remove from Wishlist
# -------------------------------
@login_required
def remove_from_wishlist(request, place_id):
    Wishlist.objects.filter(user=request.user, place_id=place_id).delete()
    messages.info(request, "❌ Removed from wishlist.")
    return redirect('wishlist')




# -------------------------------
# Search Place
# -------------------------------

def search_places(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        # Split query into individual words
        keywords = query.split()

        # Start with an empty Q object
        search_filter = Q()

        # Match *any* of the words in name or description
        for word in keywords:
            search_filter |= Q(name__icontains=word) | Q(description__icontains=word)

        results = Place.objects.filter(search_filter).distinct()

    return render(request, 'home/search_results.html', {
        'query': query,
        'results': results
    })


@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect('user_profile')
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    return render(request, 'home/edit_profile.html', {'form': form})



# -------------------------------
# Review Place
# -------------------------------


@login_required
def upload_review(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.place = place
            review.save()
            messages.success(request, "✅ Review added successfully!")
            return redirect('place_detail', place_id=place.id)
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = ReviewForm()
    return render(request, 'home/upload_review.html', {'form': form, 'place': place})


def view_reviews(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    reviews = place.reviews.all().order_by('-created_at')
    return render(request, 'home/view_reviews.html', {'place': place, 'reviews': reviews})

