from django.shortcuts import render,get_object_or_404 , redirect,HttpResponseRedirect, HttpResponse
 # Http404 رو import کن
from.models import Product ,Comment  # noqa: F401
from products.utils import get_product_last_price_list_orm
from products.forms import ProductCommentModelForm
from django.views import View

from django.contrib import messages
# Create your views here.

###

def product_list_view(request):
    #categories = Category.objects.all()
    products = Product.objects.all()[:10]
    context = {'products':products}
    return render(request,
                  template_name='products/product-list.html'
                  ,context=context)


class ProductClassBaseView(View):
    """نمایش جزئیات محصول و مدیریت کامنت‌ها"""
    
    form_class = ProductCommentModelForm
    template_name = 'products/product-detail.html'

    def get(self, request, product_id, *args, **kwargs):
        """نمایش صفحه محصول - متد GET"""
        
        # دریافت محصول با relations برای بهینه‌سازی کوئری‌ها
        product = get_object_or_404(
            Product.objects.select_related('category')
                          .prefetch_related('prdct_comments'),
            id=product_id
        )
        
        # دریافت قیمت‌های فروشندگان
        seller_prices = get_product_last_price_list_orm(product_id)
        default_seller = seller_prices.first() if seller_prices.exists() else None
        
        # دریافت کامنت‌های محصول
        comments = product.prdct_comments.all()
        
        # ایجاد فرم خالی برای ثبت کامنت جدید
        comment_form = self.form_class(initial={'product': product})
        
        # آماده‌سازی context برای ارسال به template
        context = {
            'product': product,
            'seller_prices': seller_prices,
            'default_product_seller': default_seller,
            'prdct_comments': comments,
            'comment_counts': comments.count(),
            'comment_form': comment_form
        }
        
        return render(request, self.template_name, context)

    def post(self, request, product_id, *args, **kwargs):
        """ثبت کامنت جدید - متد POST"""
        
        # چک کردن لاگین بودن کاربر
        if not request.user.is_authenticated:
            messages.warning(
                request, 
                "برای ثبت نظر باید وارد حساب کاربری خود شوید."
            )
            return redirect('accounts:login')
        
        # دریافت اطلاعات فرم از request
        comment_form = self.form_class(request.POST)
        
        # اعتبارسنجی فرم
        if comment_form.is_valid():
            try:
                # ذخیره کامنت بدون commit کردن در دیتابیس
                comment = comment_form.save(commit=False)
                
                # تنظیم کاربر و محصول
                comment.user = request.user
                comment.product_id = product_id
                
                # ذخیره نهایی در دیتابیس
                comment.save()
                
                # نمایش پیغام موفقیت
                messages.success(request, "نظر شما با موفقیت ثبت شد!")
                
                # ریدایرکت به صفحه همین محصول
                return redirect('products:product_single_view', product_id=product_id)
                
            except Exception as e:
                # مدیریت خطاهای احتمالی
                messages.error(request, f"خطا در ثبت نظر: {str(e)}")
        else:
            # نمایش پیغام خطا اگر فرم معتبر نبود
            messages.error(request, "لطفاً فرم را به درستی پر کنید.")
        
        # اگر فرم معتبر نبود یا خطا رخ داد، دوباره صفحه رو نمایش بده
        product = get_object_or_404(Product, id=product_id)
        seller_prices = get_product_last_price_list_orm(product_id)
        comments = product.prdct_comments.all()
        
        context = {
            'product': product,
            'seller_prices': seller_prices,
            'default_product_seller': seller_prices.first() if seller_prices.exists() else None,
            'prdct_comments': comments,
            'comment_counts': comments.count(),
            'comment_form': comment_form  # فرم با خطاها
        }
        
        return render(request, self.template_name, context)
   
    
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



def category_view(request, category_slug):#ناقص است
    return render(request, 'products/category.html')
    

def brand_view(request, brand_slug):#ناقص است
    
    return render(request, 'products/brand.html')

def delete_comment(request, comment_id):#ناقص است ,urls , هم ندارد
    cmmnt_obj = get_object_or_404(Comment, id=comment_id)
    if cmmnt_obj.user != request.user:
        return HttpResponseRedirect('products:product_single_view', HttpResponse._403_FORBIDDEN)
    else:
        if request.method == "POST":
            cmmnt_obj.delete()
        return HttpResponseRedirect('products:product_single_view', HttpResponse._200_OK)

 
def product_search_view(request):#ناقص است

    return render(request, 'products/search.html')  

