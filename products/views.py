from django.shortcuts import render,get_object_or_404 , redirect#,httpResponse
 # Http404 رو import کن
from.models import Product ,Comment  # noqa: F401
from products.utils import get_product_last_price_list_orm
from products.forms import ProductCommentModelForm
# Create your views here.

def product_list_view(request):
    #categories = Category.objects.all()
    products = Product.objects.all()[:10]
    context = {'products':products}
    return render(request,
                  template_name='products/product-list.html'
                  ,context=context)
    
   
    
def product_detail_view(request, product_id):
    
    p = get_object_or_404(Product.objects.select_related(
        'category').prefetch_related('prdct_comments') , id=product_id)
        
    """نکته: select_related برای فارین کی ها (FK) و
    prefetch_related برای manytomany ها یا fkهای که reverse هستن 
    و روی table ما قرار دارند.
    """
    # با استفاده از دستورات ORM جنگو بدون SQL خام
    seller_prices = get_product_last_price_list_orm(product_id)

    # همه‌ی seller_prices مربوط به این محصول
    seller_prices = p.seller_prices.all()

    # فروشنده‌ی پیش‌فرض (مثلاً اولین آیتم یا براساس منطق خودت)
    default_product_seller = seller_prices.first()

    # اضافه کردن کامنت‌ها
    prdct_comments = p.prdct_comments.all()

    if request.method == "GET":
        comment_form = ProductCommentModelForm(initial={'product':p})
    elif request.method == "POST":
        comment_form = ProductCommentModelForm(request.POST)
        if comment_form.is_valid():
           comment_form.save(commit=True)
           
            # Comment.objects.create(**comment_form.cleaned_data,product=p)
           
        return redirect('products:product_single_view', product_id=product_id)       

    context = {
        'product': p,
        'seller_prices': seller_prices, # p.seller_last_prices
        'default_product_seller': default_product_seller,
        'prdct_comments':prdct_comments,
        
        # اگر نیاز داری شمارش کامنت هم تو تمپلیت استفاده کنی:
        'comment_counts': prdct_comments.count() ,#if hasattr(p, 'comments') else 0,
        'comment_form': comment_form
    }

    return render(request, 'products/product-detail.html', context)


#
def home(request):
    query = Product.objects.all()
    most_off_products = query
    most_sell = query
    most_recent = query
    context = {
        "most_off_products": most_off_products,
        "most_sell": most_sell,
        "most_recent": most_recent,
        "banners": [],
    }

    return render(
        template_name='products/index.html',
        request=request,
        context=context
    )

 
  
