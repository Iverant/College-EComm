from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def products(request):
    page_obj = products = Product.objects.all() 

    product_name = request.GET.get('product_name')
    if product_name != '' and product_name is not None:
        page_obj = products.filter(name__icontains=product_name)
    
    paginator = Paginator(page_obj, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'myapp/index.html', context)

#class based view for above products view [ListView]
class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'products'
    paginate_by = 3

def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'myapp/detail.html', context)

#class based view for above product_detail view [DetailView]
class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/detail.html'
    context_object_name = 'product'

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES['upload']
        quantity = request.POST.get('quantity')  
        seller_name = request.user
        product = Product(name=name, price=price, desc=desc, image= image,quantity=quantity, seller_name=seller_name)
        product.save()
    return render(request, 'myapp/addproduct.html')

#class based view for above add_product view [CreateView]
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'desc', 'image','quantity', 'seller_name']
    

def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.desc = request.POST.get('desc')
        product.image = request.FILES['upload']
        product.quantity = request.POST.get('quantity') 
        product.save()
        return redirect('/myapp/products/')
    context = {'product': product}
    return render(request, 'myapp/updateproduct.html', context)

#class based view for above update_product view [UpdateView]
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'desc', 'image', 'quantity' ,'seller_name']
    template_name_suffix = '_update_form'

def delete_product(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    if request.method == 'POST':
        product.delete()
        return redirect('/myapp/products/')
    return render(request, 'myapp/delete.html', context)

#class based view for above delete_product view [DeleteView]
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('myapp:products')

def my_listings(request):
    products = Product.objects.filter(seller_name=request.user)
    context = {'products': products}
    return render(request, 'myapp/mylistings.html', context)

@login_required

@login_required
@login_required
@login_required
def buy_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    # Check if the current user is the seller of the product
    if product.seller_name == request.user:
        return render(request, 'myapp/buy_product.html', {'product': product, 'error': 'You cannot buy your own product.'})
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity > product.quantity:
            # Handle the case where the requested quantity is more than available
            return render(request, 'myapp/buy_product.html', {'product': product, 'error': 'Requested quantity exceeds available stock.'})
        
        
        product.quantity -= quantity
        if product.quantity == 0:
            product.delete()
        else:
            product.save()
        return redirect('/myapp/products/')
    
    client = razorpay.Client(auth=('rzp_test_iAXoYqImBUMKhy', 'FFkOH7CYDIUs7rqIPwGyF8Fn'))
    payment = client.order.create({'amount': product.price * 100, 'currency': 'INR', 'payment_capture': '1'})
    
    print("**************************")
    print(payment)
    print("**************************")
    
    return render(request, 'myapp/buy_product.html', {'product': product, 'payment': payment})



def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'myapp/product_detail.html', {'product': product, })
