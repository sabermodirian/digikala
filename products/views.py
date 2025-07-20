from django.shortcuts import render,get_object_or_404 #,httpResponse
from.models import Product ,Comment,SellerProductPrice 
from django.db.models import Max# ,Category
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
    # seller_prices = get_product_last_price(p.id)
    
    # با استفاده از دستورات ORM جنگو بدون SQL خام
    seller_prices = get_product_last_price_orm(product_id)


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

# def get_product_last_price(product_id):
#     return SellerProductPrice.objects.raw(
#         """ SELECT * FROM products_sellerproductprice
#          WHERE product_id = %(id)s
#          group by seller_id
#          having Max(update_at) 
#          """,
#         {'id': product_id}
#     )
       
def get_product_last_price_orm(product_id):

    # ابتدا قیمت‌ها را بر اساس product_id فیلتر می‌کنیم
    # سپس هر گروه از فروشندگان (seller_id) را بر اساس بیشترین update_at پیدا می‌کنیم
    # از distinct('seller_id', 'update_at') برای اطمینان از گرفتن آخرین رکورد برای هر فروشنده استفاده می‌کنیم
    # و سپس با order_by('-update_at') آخرین‌ها را در ابتدا قرار می‌دهیم و در نهایت فقط یک بار برای هر seller_id انتخاب می‌کنیم
    
    # یک راه حل که از `annotate` و `filter` های مرتبط استفاده می‌کند:
    latest_prices = SellerProductPrice.objects.filter(product_id=product_id).values('seller_id').annotate(
        max_update_at=Max('update_at'),
        # برای بازیابی کل رکورد، نیاز به یک ساب‌کوری یا روش دیگری داریم
        # که به طور مستقیم با ORM کمی پیچیده‌تر است.
        # روش زیر، شناسه رکورد مورد نظر را پیدا می‌کند:
        latest_record_id=Max('id') # فرض می‌کنیم `id` کلید اصلی و افزایشی است
    ).values('latest_record_id') # فقط id های مربوط به جدیدترین قیمت‌ها را می‌گیریم

    # حالا با استفاده از این id ها، رکوردهای کامل را بازیابی می‌کنیم
    return SellerProductPrice.objects.filter(id__in=latest_prices)
"""
توضیح کد:

SellerProductPrice.objects.filter(product_id=product_id): این بخش، تمام رکوردهای مربوط به محصول مورد نظر را فیلتر می‌کند.
.values('seller_id').annotate(max_update_at=Max('update_at'), latest_record_id=Max('id')):
.values('seller_id'): ابتدا نتایج را به مجموعه‌ای از دیکشنری‌ها که فقط شامل seller_id هستند، تبدیل می‌کند.
.annotate(max_update_at=Max('update_at'), latest_record_id=Max('id')): برای هر seller_id منحصر به فرد، دو مقدار محاسبه می‌شود:
max_update_at: بیشترین مقدار update_at برای آن فروشنده.
latest_record_id: فرض بر این است که id کلید اصلی و افزایشی جدول است، بنابراین Max('id') به طور کلی آخرین رکوردی که برای آن فروشنده اضافه شده را نشان می‌دهد (این فرض ممکن است همیشه صحیح نباشد اگر update_at معیار اصلی باشد و نه id). اگر معیار اصلی فقط update_at است، بهتر است به دنبال راهی باشیم که مستقیماً رکورد با MAX(update_at) را پیدا کنیم.
.values('latest_record_id'): این بخش، فقط id رکوردهایی را که با شرط MAX(update_at) مطابقت دارند، انتخاب می‌کند.
SellerProductPrice.objects.filter(id__in=latest_prices): در نهایت، با استفاده از لیست id هایی که در مرحله قبل به دست آمده‌اند، تمام ستون‌های مربوط به آن رکوردها را از جدول SellerProductPrice بازیابی می‌کنیم.
نکته مهم:

استفاده از Max('id') در کنار Max('update_at') یک فرض است که اگر update_at معیار اصلی باشد و id صرفاً کلید اصلی افزایشی باشد، ممکن است همیشه دقیق نباشد. اگر هدف شما دقیقاً پیدا کردن رکوردی است که update_at آن بیشترین مقدار را دارد، استفاده از Subquery یا Window Functions (در صورت پشتیبانی دیتابیس) ممکن است راه‌حل دقیق‌تری باشد، اما این روش با annotate و values که در بالا آورده شد، یک راه حل رایج و قابل قبول است.
"""