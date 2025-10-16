from . models import Catogory

def menu_links(request):
    links = Catogory.objects.all()
    return dict(links=links)
