from django.shortcuts import render , get_object_or_404
from myapp.models import Catogory
from store.models import Product
from carts.models import CartItem 
from carts.views import _cart_id
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from django.db.models import Q

# Create your views here.
def store(request, category_slug=None):
    category = None
    products = None
    if category_slug is not None:
        category = get_object_or_404(Catogory, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        paginator=Paginator(products, 3)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator=Paginator(products, 3)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_product,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    # Use case-insensitive lookup and return a 404 if not found
    try:
        single_product =Product.objects.get(
            category__slug__iexact=category_slug,
            slug__iexact=product_slug,
            is_available=True,
            )
        in_cart =CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    
    except Exception as e:
        raise e
    context = {'single_product': single_product,
               'in_cart':in_cart
               }
    return render(request, 'store/product_detail.html', context)

def search(request) :
    if 'q' in request.GET:
        q=request.GET['q']
        if q :
            products=Product.objects.filter(Q(description__icontains=q)|Q(product_name__icontains=q))
    product_count = products.count()
    context={"products":products,
             "product_count":product_count}
    return render(request,'store/store.html', context)