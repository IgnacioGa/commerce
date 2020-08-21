from .models import Category

def foos(request):
    return {'categorys': Category.objects.all()}