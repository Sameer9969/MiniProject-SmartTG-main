from .models import Place

def all_places(request):
    places = Place.objects.all()
    return {'all_places': places}
