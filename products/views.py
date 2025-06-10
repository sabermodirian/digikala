from django.shortcuts import render,get_object_or_404 #,httpResponse
from.models import Product  # ,Category
#from django.template.loader import get_template 

# Create your views here.

def product_list_view(request):
    #categories = Category.objects.all()
    products = Product.objects.all()[:10]
    context = {'products':products}
    return render(request,
                  template_name='products/product-list.html'
                  ,context=context)
    
   
    
def product_detail_view(request, product_id):
    p = get_object_or_404(Product, id=product_id)

    # همه‌ی seller_prices مربوط به این محصول
    seller_prices = p.seller_prices.all()

    # فروشنده‌ی پیش‌فرض (مثلاً اولین آیتم یا براساس منطق خودت)
    default_product_seller = seller_prices.first()

    context = {
        'product': p,
        'seller_prices': seller_prices,
        'default_product_seller': default_product_seller,
        # اگر نیاز داری شمارش کامنت هم تو تمپلیت استفاده کنی:
        #'comment_counts': p.comments.count() if hasattr(p, 'comments') else 0,
    }

    return render(request, 'products/product-detail.html', context)

       
      