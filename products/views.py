from django.shortcuts import render,get_object_or_404 #,httpResponse
from.models import Product ,Comment,SellerProductPrice # ,Category
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

    if request.method == 'POST':
        # اینجا می‌توانید کامنت‌ها را در مدل Comment ذخیره کنید   
        Comment.objects.create(
            title=request.POST.get('title',''),
            text=request.POST.get('text',''),
            rate=int(request.POST.get('rate',0)),
            user_email=request.POST.get('user_email',''),
            product_id=p
        )

        

    """
    SELECT *: این بخش مشخص می‌کند که همه ستون‌های جدول products_sellerproductprice باید انتخاب شوند. یعنی تمام اطلاعات مربوط به رکوردهای انتخاب شده در نتیجه نهایی خواهد بود.

    FROM products_sellerproductprice: این قسمت به پایگاه داده می‌گوید که کدام جدول استفاده شود. در اینجا، جدول products_sellerproductprice به عنوان منبع داده‌ها تعیین شده است. این جدول معمولاً شامل اطلاعات مربوط به قیمت‌های محصولات از فروشندگان مختلف است.

    WHERE product_id = {p.id}: این شرط، رکوردهایی را که ارتباط با محصول خاصی (با شناسه p.id) دارند، فیلتر می‌کند. این شناسه باید با مقدار واقعی شناسه محصولی که می‌خواهیم اطلاعاتش را بگیریم جایگزین شود. به عبارت دیگر، این قسمت باعث می‌شود که فقط قیمت‌های فروشندگان مربوط به این محصول خاص در نتیجه آخر فیلتر شوند.

    GROUP BY seller_id: این بخش رکوردها را بر اساس شناسه فروشنده (seller_id) گروه‌بندی می‌کند. به این صورت، برای هر فروشنده، یک گروه جداگانه ایجاد می‌شود.

    HAVING MAX(update_at): این شرط به ما امکان می‌دهد که فقط جدیدترین رکوردها برای هر فروشنده را انتخاب کنیم. MAX(update_at) به یادداشت جدیدترین تاریخ به‌روزرسانی برای هر فروشنده اشاره دارد. در واقع، با این شرط، رکوردهای مربوط به قیمت‌های فروشندگان با جدیدترین تاریخ به‌روزرسانی نمایش داده می‌شوند.

    نتیجه‌گیری
    در نهایت، این کد اطلاعات مربوط به قیمت‌های فروشندگان برای محصول خاصی را که شناسه آن در {p.id} قرار داده شده، بازیابی می‌کند و تنها قیمت‌های مرتبط با جدیدترین تاریخ به‌روزرسانی که برای هر فروشنده وجود دارد را برمی‌گرداند. این کد به شما کمک می‌کند تا فقط اطلاعات قیمت‌های جدیدترین فروشندگان محصول خاص را دریافت نمایید، که در انجام تحلیل‌ها یا نمایش قیمت‌ها در سایت بسیار مفید است.
    """
    seller_prices =SellerProductPrice.objects.raw(
        f""" SELECT * FROM products_sellerproductprice
         WHERE product_id = {p.id}
         group by seller_id
         having Max(update_at) """)

    # همه‌ی seller_prices مربوط به این محصول
    seller_prices = p.seller_prices.all()

    # فروشنده‌ی پیش‌فرض (مثلاً اولین آیتم یا براساس منطق خودت)
    default_product_seller = seller_prices.first()

    # اضافه کردن کامنت‌ها
    prdct_comments = p.prdct_comments.all()

    context = {
        'product': p,
        'seller_prices': seller_prices,
        'default_product_seller': default_product_seller,
        'prdct_comments':prdct_comments,
        
        # اگر نیاز داری شمارش کامنت هم تو تمپلیت استفاده کنی:
        'comment_counts': prdct_comments.count() ,#if hasattr(p, 'comments') else 0,
    }

    return render(request, 'products/product-detail.html', context)

       
      