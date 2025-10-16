from django.shortcuts import render , get_object_or_404
from myapp.models import Catogory
from .models import Product
# Create your views here.
def store(request, category_slug=None):
    category = None
    products = None
    if category_slug is not None:
        category = get_object_or_404(Catogory, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    # Use case-insensitive lookup and return a 404 if not found
    single_product = get_object_or_404(
        Product,
        category__slug__iexact=category_slug,
        slug__iexact=product_slug,
        is_available=True,
    )
    context = {'single_product': single_product}
    return render(request, 'store/product_detail.html', context)
  