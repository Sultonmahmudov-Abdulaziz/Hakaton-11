import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView,DetailView
from .models import Cleaners,Category,Order,OrderItem
from django.http import HttpResponse,JsonResponse
from .cart import Cart
from django.views import View
from django.core.exceptions import ValidationError
from .sent_telegram import main
import asyncio
from .models import Comment
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User





#
# def index(request):
#     return render(request, 'product/index.html')


def cart_summary(request):

    cart = Cart(request)

    products = cart.get_products()
    quantity = cart.get_quantity()
    total = cart.get_total_price()

    all_orders = cart.get_all_info()

    data = {
        "products":products,
        "quantities":quantity,
        'total':total,
        "all_orders":all_orders
    }


    return render(request, 'cleaner/cart_summary.html',context=data)

def cart_add(request):

    cart = Cart(request)


    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = request.POST.get('product_quantity')

        product = get_object_or_404(Cleaners,id=product_id)

        cart.add(product=product,quantity=quantity)

        return JsonResponse({"product_id":product_id})
    return HttpResponse("Hello world")

def cart_update(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = request.POST.get('product_quantity')
        product = get_object_or_404(Cleaners, id=product_id)

        cart.product_update(product,quantity)

    return JsonResponse({"status":"Hello world"})

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        print(request.POST)
        product_id = request.POST.get('product_id')
        cart.delete_product(product_id)
        return JsonResponse({"status":"salom"})



class ProductListView(ListView):
    model = Cleaners
    template_name = 'cleaner/index.html'
    context_object_name = 'product'



class CategoryProductsList(DetailView):
    model = Category
    
    template_name = 'cleaner/categories.html'

    context_object_name = 'categories'

    def get_context_data(self,*args, **kwargs):
        context = super(CategoryProductsList,self).get_context_data(*args, **kwargs)
        category = context['categories']
        context['categories'] = category.categories.all()

        return context


class ProductDetailView(DetailView):
    model = Cleaners
    template_name = 'cleaner/detail.html'
    context_object_name = 'cleaner'
    comments=Comment.objects.all()



class OrderView(View):
    
    def post(self,request):
        cart = Cart(request)

        all_orders = cart.get_all_info()
        total = cart.get_total_price()

        
        
        order = Order()
        order.order_id = uuid.uuid4()
        order.total_price = total
        order.user = request.user
        
        order.save()
        user_manzil = request.user.manzil
        user_phone=request.user.phone_number
        try:
          
            for item_data in all_orders:
                order_item = OrderItem()
                order_item.order = order
                order_item.product_id = item_data['id']
                order_item.price = item_data['price']
                order_item.name = item_data['name']
                order_item.manzil = user_manzil
                order_item.phone = user_phone
                order_item.quantity = item_data['quantity']
                order_item.save()
                asyncio.run(main(f"""Siz {order_item.name} kasbiga oid {order_item.quantity} nafar 
hodim  uchun buyurtma qildingiz Hodimlarimiz {order_item.price}$ miqdordagi summani 50% ni
'986012345678910' hisob raqamimizga to'lov qilishingiz bilanoq hodimlariz {order_item.manzil} izga yetib borishadi 
                                   {order_item.phone} yo'lga chiqishadi"""))
                
               
        except:
            raise ValidationError("OrderItem modeliga saqlashdagi xatolik")

        cart.clear_cart()

        return redirect('cleaner:index')


class GetOrdersView(LoginRequiredMixin,View):

    def get(self, request):
        user = request.user

        orders = user.orders.all()

        data = {
            "orders":orders
        }

        return render(request, 'cleaner/orders.html', context=data)

class AddComment(LoginRequiredMixin, View):
    def post(self, request, id):
        form = CommentForm(request.POST)
        book = Cleaners.objects.get(id=id)
        data = {
            'form': form,
            'book': book
        }
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                book=book,
                comment_text=form.cleaned_data['comment_text'],
                stars_given=form.cleaned_data['stars_given']
            )
            return redirect(reverse('cleaner:index' ))
        return render(request, 'cleaner/detail.html', context=data)  