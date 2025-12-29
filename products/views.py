from django.shortcuts import render,get_object_or_404 , redirect,HttpResponseRedirect, HttpResponse
from django.db.models import Max, Min, Q, Prefetch  # Prefetch را اضافه کنید
from.models import Product ,Comment, Category  # noqa: F401

from products.utils import get_product_last_price_list_orm , to_dict  # noqa: F401
from products.forms import ProductCommentModelForm
from django.views import View
from django.views.generic import ListView , DetailView , CreateView,\
    UpdateView , DeleteView  # noqa: F401
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import JsonResponse # یا Response اگه DRF داریfrom .models import Comment  # noqa: F401

import json  # noqa: F401
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view  
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommentSerializer , CommentModelSerializer  # noqa: F401

# Create your views here.



def product_list_view(request):
    #categories = Category.objects.all()
    products = Product.objects.all()[:10]
    context = {'products':products}
    return render(request,
                  template_name='products/product-list.html'
                  ,context=context)

class ProductDetailView(DetailView): #CBV for product detail view
    model = Product
    queryset = Product.objects.exclude(is_active=False)
    template_name = 'products/product-detail.html'


    def get(self, request, product_id, *args, **kwargs):
        return render(request, 'products/product-detail.html')

class ProductClassBaseView(View): #CBV ضعیف تقریبا شبیه فانکشن بیس ویو عمل میکند و خیلی امکانات جدید و خاصی به ما نمی دهد
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
   
    
def product_detail_view(request, product_id): #FBV for product detail view
    
    # p = get_object_or_404(Product.objects.select_related(
    #     'category').prefetch_related('prdct_comments') , id=product_id)
    p = get_object_or_404(Product.objects.select_related(
        'category'), id=product_id) # بدون prefetch    
        
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
    # prdct_comments = p.prdct_comments.all()  # با استفاده از دستورات ORM

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
        # 'prdct_comments':prdct_comments,
        
        # اگر نیاز داری شمارش کامنت هم تو تمپلیت استفاده کنی:
        # 'comment_counts': prdct_comments.count() ,#if hasattr(p, 'comments') else 0,
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



# products/views.py
'''class ProductListView(ListView):
 یادت باشه  نام قبلی این کلاس در پروژه ی کمیجانی
 '''

"""
🧠 کش کردن (Caching) ویوی دسته‌بندی محصولات به مدت ۱۵ دقیقه
---------------------------------------------------------
این دکوراتور باعث می‌شود کل خروجی View (CategoryListView) به‌صورت خودکار 
در حافظه‌ی کش ذخیره شود. تا ۱۵ دقیقه بعد از اولین درخواست، بدون اجرای دوباره‌ی
کوئری‌های دیتابیس، پاسخ مستقیماً از Cache برگردانده می‌شود.

Benefits:
- Reduces database load significantly.
- Increases response speed for search/sort pages.

Note:
Every unique URL parameter combination (e.g., ?search=x&sort=y) 
creates a separate cache entry.
"""
@method_decorator(cache_page(60 * 15), name="dispatch")
class CategoryListView(ListView):
    """
    نمایش لیست محصولات با قابلیت فیلتر دسته‌بندی، جستجو و مرتب‌سازی.
    Product list view with category filtering, search, and sorting capabilities.
    """
    model = Product
    template_name = "products/category_list.html"
    context_object_name = "product_list"
    paginate_by = 6

    def get_category(self):
        """
        🔍 بازیابی دسته‌بندی بر اساس اسلاگ (از URL یا Query Parameter).
        Retrives the category object based on the slug, handling trimming and cleaning.
        """
        # استفاده از کش داخلی برای جلوگیری از کوئری تکراری در یک درخواست
        if hasattr(self, "_category_cache"):
            return self._category_cache

        # دریافت اسلاگ از مسیر URL یا پارامتر GET
        slug_from_path = self.kwargs.get("category_slug")
        slug_from_query = self.request.GET.get("category_slug")
        resolved_slug = slug_from_path or slug_from_query

        if not resolved_slug:
            self._category_cache = None
            return None

        # 🛠️ مهم: حذف فاصله‌های اضافی که باعث خطای 404 می‌شدند
        cleaned_slug = resolved_slug.strip()

        self._category_cache = get_object_or_404(Category, slug=cleaned_slug)
        return self._category_cache

    def get_queryset(self):  # override _queryset=qs
        """
        ⚙️ ساخت کوئری نهایی محصولات (فیلتر فعال بودن، دسته، جستجو و مرتب‌سازی).
        Constructs the final queryset with filters and annotations.
        """
        qs = Product.objects.filter(is_active=True)
        
        # 1. فیلتر بر اساس دسته (اگر وجود داشته باشد)
        category = self.get_category()
        if category:
            qs = qs.filter(category=category)

        # 2. جستجو (Search)
        # .strip() اینجا هم اضافه شد تا جستجوهای " متن " درست کار کنند
        search_query = self.request.GET.get("search", "").strip()
        if search_query:
            qs = qs.filter(
                Q(name__icontains=search_query) |
                # Q(english_name__icontains=search_query) |  # ❌ این خط غلط است
                Q(en_name__icontains=search_query) |  # ✅ این خط اصلاح شدQ(english_name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(brand__name__icontains=search_query)
            )

        # 3. مرتب‌سازی (Sorting)
        sort_option = self.request.GET.get("sort", "newest")
        
        # محاسبه کمترین و بیشترین قیمت برای استفاده در مرتب‌سازی
        qs = qs.annotate(
            min_price=Min("seller_prices__price"),
            max_price=Max("seller_prices__price")
        )

        if sort_option == "min_price":
            qs = qs.order_by("min_price")
        elif sort_option == "max_price":
            qs = qs.order_by("-max_price")
        else:
            # پیش‌فرض: جدیدترین‌ها (بر اساس تاریخ ایجاد قیمت فروشنده یا محصول)
            qs = qs.order_by("-id") # یا -created_at اگر دارید

        return qs

    def get_context_data(self, **kwargs):
        """
        📦 ارسال داده‌های کمکی به قالب (برای حفظ وضعیت فرم‌ها و سایدبار).
        Adds extra context like categories list, current search query, and sort option.
        """
        """
        🚀 بازنویسی شده: ارسال داده‌های بهینه برای ساختار درختی و حفظ وضعیت فرم‌ها.
        
        تغییرات کلیدی:
        - `categories_tree`: به جای ارسال لیست خطی دسته‌بندی‌ها، یک ساختار درختی بهینه
          با `prefetch_related` ارسال می‌شود. این کار تمام فرزندان و نوه‌ها را در
          یک کوئری بهینه فراخوانی کرده و از مشکل N+1 جلوگیری می‌کند.
        """
        context = super().get_context_data(**kwargs)
        
        # فراخوانی بهینه دسته‌بندی‌های سطح بالا (والد ندارند) به همراه تمام فرزندانشان
        top_level_categories = Category.objects.filter(
            parent__isnull=True).prefetch_related(
            Prefetch(
                'children',
                queryset=Category.objects.prefetch_related('children') # برای لود کردن نوه‌ها
            )
        )
        
        context.update({
            "categories_tree": top_level_categories, # <--- جایگزین "categories" شد
            "category": self.get_category(),
            "search_query": self.request.GET.get("search", "").strip(),
            "current_sort": self.request.GET.get("sort", "newest")
        })
        return context

        '''
        🚀 بازنویسی شده:
         ارسال داده‌های بهینه برای ساختار درختی و حفظ وضعیت فرم‌ها:    
                                                    . نکته مهم:
        در فایل context_processors.py شما همچنان کار می‌کند، 
        اما در این صفحه ما از آن استفاده نمیکنیم بلکه از
         categories_tree که در ویو ساختیم استفاده می‌کنیم 
        چون بهینه است.
        '''
@csrf_exempt
def comment_api_response(request,product_id): # ''' این ویو برای تست API است '''
    cmmnts=Comment.objects.filter(product=product_id)
    cmnt_lst=list(cmmnts.values('product','product_id','rate','text','title','user','user_email','user_id'))    
    
    rspns = json.dumps({"message" : "Hello from API response for my digikala testing",
                        "result":cmnt_lst,
                        "count":cmmnts.count(),
                        
                        }, ensure_ascii=False)
    # return JsonResponse({"message" :"Hello from API"}) 
    return HttpResponse(content=rspns, content_type="application/json")



# @csrf_exempt
@api_view(['POST','GET'])
def comment_api_response_drf(request, product_id):
    '''  این ویو برای تست API است   '''
     # اول محصول رو پیدا کنیم که اگه نبود، 404 بدیم
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "محصولی با این شناسه یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        cmmnts_qs = Comment.objects.filter(product_id=product_id).select_related(
            'user'
        )
        
        # # 2. پاس دادن تک‌تک دیکشنری‌ها به تابع utils
        # # formatted_data = [comment_dict_formatter(cmnt) for cmnt in cmmnts_qs]
        # cmnt_lst = [to_dict(cmnt) for cmnt in cmmnts_qs]    
        # context = {
        #     "message" : "Hello from API in DRF for my digikala DRF(APIView) testing",
        #     "result":cmnt_lst,
        #     "count":cmmnts_qs.count(),
        # }
        # # return JsonResponse(formatted_data, safe=False, json_dumps_params={"ensure_ascii": False})

        # return Response(data=context, status=status.HTTP_200_OK)
        comment = CommentModelSerializer(instance=cmmnts_qs, many=True)
        return Response(data=comment.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # 1. داده‌های ورودی رو بده به سریالایزر
        serializer = CommentModelSerializer(data=request.data)
        
        # 2. اعتبارسنجی کن (اگه داده‌ها اشتباه باشن، خودش 400 برمی‌گردونه!)
        serializer.is_valid(raise_exception=True)
        
        # 3. کامنت جدید رو ذخیره کن (خودش همه کارا رو میکنه)
        #    یوزر و محصول رو هم خودمون بهش اضافه می‌کنیم
        serializer.save(user=request.user, product=product)
        
        # 4. یه جواب خوشگل به کاربر برگردون
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        # form = ProductCommentModelForm(request.POST)
        # if form.is_valid():
        #     cmnt_obj = form.save(commit=False)
        #     cmnt_obj.product = get_object_or_404(Product, id=product_id)
        #     cmnt_obj.user = request.user
        #     cmnt_obj.save()
        #     return Response(data=context, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(data=form.errors, status=status.HTTP_400_BAD_REQUEST)   



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

