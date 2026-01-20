from django.db import models
from django.db.models import Min, Max
from django.db.models.functions import Coalesce
from django.utils.translation import gettext as _
from django.urls import reverse  # noqa: F401
from django.conf import settings
from .validators import validate_rate
# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your models here.

class Brand(models.Model):
    name = models.CharField(_("Name"),max_length=150)
    en_name = models.CharField(_("En Name"),max_length=150)
    slug = models.SlugField(_("slug"),blank=True,null=True )
    verbose_name = _("Brand")
    verbose_name_plural = _("Brands")
    def __str__(self):
        return f'{self.id}:{self.name } {self.en_name} {self.slug}'


class MyQuerySet(models.QuerySet):
    def deleted(self):
        return self.update(is_active=False)

class NoDeleteManager(models.Manager):
    def get_queryset(self):
        return MyQuerySet(self.model, using=self._db)


class ProductQuerySet(models.QuerySet):
    def with_price_bounds(self):
        """Annotate each product with min_price/max_price taken from SellerProductPrice.
        این متد برای هر محصول، قیمت های حداقل/حداکثر را از SellerProductPrice برمیگرداند."""
        return self.annotate(
            min_price=Coalesce(Min("seller_prices__price"), 0),
            max_price=Coalesce(Max("seller_prices__price"), 0),
        )

# class ProductQuerySet(models.QuerySet):
#     def active(self):
#         return self.filter(is_active=True)

        objects = ProductQuerySet.as_manager()  # noqa: F841
        """Custom manager for Product model.
        این یک مدیر کوستوم است که برای مدل Product استفاده می‌شود.
        """

class Product(models.Model):   
    
    #Product details
    name = models.CharField(_("Persian Name"),max_length=200)
    en_name = models.CharField(_("English Name"),max_length=200)#Enhlish Name of products
    description = models.TextField(_("Description"))
    is_active = models.BooleanField(_("Is Active"),default=True)
    category = models.ForeignKey("Category"
                                 ,verbose_name=_("Category")
                                 ,on_delete=models.RESTRICT       # RESTRICT = PROTECT
                                 )
    brand = models.ForeignKey("Brand"
                              ,verbose_name=_("Brand")
                              ,on_delete=models.SET_NULL    # RESTRICT = PROTECT
                              ,blank=True,null=True       
                              )
    sellers = models.ManyToManyField("sellers.Seller"
                                     ,verbose_name=_("Sellers")
                                     ,through="SellerProductPrice"
                                     )
    """

    (حتماً! این بخش through="SellerProductPrice" در تعریف فیلد ManyToMany به این معنیه که 
    برای رابطهٔ چند به چند بین مدل‌ها، به جای جدول واسطِ پیش‌فرض Django، خودت یک مدل سفارشی واسط
    تعریف کردی که اطلاعات بیشتری (مثلاً قیمت هر فروشنده برای هر محصول) داخلش ذخیره کنی.)


    پارامتر `through="SellerProductPrice"` به Django می‌گوید که برای مدیریت رابطه‌ی چند-به-چند میان محصول و فروشنده
    به جای جدول واسط پیش‌فرض، از مدل سفارشی SellerProductPrice استفاده کند.
    با این کار می‌توان اطلاعات بیشتری مثل قیمت هر محصول برای هر فروشنده
    یا ویژگی‌های دیگر را در رابطه ذخیره کرد (در مدل SellerProductPrice تعریف شود).

    مثال: اگر چند فروشنده برای یک محصول قیمت‌ها و ویژگی‌های متفاوت داشته باشند،
    این مدل واسط می‌تواند آن داده‌ها را نگه‌داری کند.
    """


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    @property
    def sellers_last_price(self):
        return SellerProductPrice.objects.raw(
            """
             SELECT * FROM products_sellerproductprice
             WHERE product_id = %(id)s
             group by seller_id
             having Max(update_at) 
            """,
            {'id': self.id}
        )
    
    @property
    def default_product_seller(self):
        if self.sellers_last_price:
            return self.sellers_last_price[0]
        return None                                    
    
    @property
    def default_image(self):
        """
        اگر چندتا تصویر با is_default=True داشتیم،
        اولی را برمی‌گرداند. اگر هیچ‌کدام نبود،
        می‌توانید یک تصویر پیش‌فرض (placeholder) هم برگردانید.
        """
        img = self.prdct_images.filter(is_default=True).first()
        if img:
            return img
        # اگر می‌خواهید وقتی هیچ پیش‌فرضی نبود اولین تصویر را هم برگردانید:
        return self.prdct_images.first()


    @property
    def categories_list(self): 
        current_category = self.category
        categories_lst = [current_category]  
        while current_category.parent is not None:
            current_category = current_category.parent
            categories_lst.append(current_category)
            categories_lst.reverse()
        return categories_lst
        """
        ما در حال بررسی تابع categories_list هستیم که در یک کلاس تعریف شده است. این تابع برای بدست آوردن لیستی از دسته‌ها از دسته فعلی تا ریشه (بالاترین والد) استفاده می‌شود. در ادامه به تفصیل و با جزئیات بیشتر این تابع را بررسی می‌کنیم و مثال فارسی ارائه می‌دهیم.

شرح کامل و دقیق الگوریتم
تابع categories_list به صورت زیر عمل می‌کند:

مقداردهی اولیه:

current_category را برابر با self.category قرار می‌دهیم. این متغیر نشان‌دهنده‌ی دسته‌ی فعلی شیء است.
یک لیست خالی به نام categories_lst ایجاد می‌کنیم و دسته‌ی فعلی (current_category) را به عنوان اولین عضو به آن اضافه می‌کنیم. بنابراین لیست در این مرحله شامل تنها یک عنصر است: دسته‌ی فعلی.
حلقه‌ی while:

شرط حلقه این است که آیا current_category والد دارد یا خیر. به عبارت دیگر، آیا current_category.parent برابر با None است یا خیر.
تا زمانی که current_category.parent مقدار None نباشد (یعنی والد وجود دارد)، حلقه ادامه می‌یابد.
در هر تکرار حلقه:
current_category را به والد آن به‌روزرسانی می‌کنیم. یعنی current_category = current_category.parent.
سپس این current_category جدید (که والد دسته‌ی قبلی است) را به انتهای لیست categories_lst اضافه می‌کنیم.
این فرآیند تا جایی ادامه می‌یابد که به دسته‌ای برسیم که والد نداشته باشد (یعنی ریشه باشد). در این نقطه، current_category.parent برابر با None خواهد بود و حلقه پایان می‌یابد.
بازگشت نتیجه:

پس از اتمام حلقه، لیست categories_lst شامل تمام دسته‌ها از دسته‌ی فعلی تا ریشه (به ترتیب از فرزند به پدر) است. این لیست را بازمی‌گردانیم.
نکات مهم:
ترتیب عناصر در لیست خروجی: اولین عنصر لیست، دسته‌ی فعلی (self.category) و آخرین عنصر، ریشه (دسته‌ای بدون والد) است. این ترتیب از پایین به بالا (از برگ به ریشه) است.
ساختار داده: این الگوریتم فرض می‌کند که دسته‌ها به صورت یک ساختار درختی (Tree) سازماندهی شده‌اند و هر گره (دسته) یک اشاره‌گر به والد خود دارد.
کاربرد: این تابع معمولاً برای نمایش سلسله‌مراتب دسته‌ها استفاده می‌شود، مثلاً در سیستم‌های دسته‌بندی محصولات در فروشگاه‌های اینترنتی.
        """    
            
    def __str__(self):
        return f'{self.id}:{self.name }' 

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})

# class ProductQuerySet(models.QuerySet):
#     def active(self):
#         return self.filter(is_active=True)

    # objects = ProductQuerySet.as_manager()
    # """Custom manager for Product model.
    # این یک مدیر کوستوم است که برای مدل Product استفاده می‌شود.
    # """


    @property
    def cheapest_price(self):
        data = self.seller_prices.aggregate(value=Min("price"))
        return data["value"] or 0
        """این متد دسته‌بندی محصولات را براساس قیمت کمترین برمی‌گرداند."""

    @property
    def most_expensive_price(self):
        data = self.seller_prices.aggregate(value=Max("price"))
        return data["value"] or 0
    """ این هم متد قیمت بیشترین محصول را برمی‌گرداند."""

    
    
class Category(models.Model):
    #Product Category
    name = models.CharField(_("Name"), max_length=50)
    description = models.TextField(_("Description"),
                                   null=True, blank=True)
    
    slug = models.SlugField(_("Slug_Cat"),
                            unique=True ,db_index=True)
    
    icon = models.ImageField(_("Icon"),upload_to='category_images',
                             null=True, blank=True)
    
    image = models.ImageField(_("Image"),upload_to='category_images',
                              null=True, blank=True)
    
   
    # ⭐️ کلیدی‌ترین فیلد برای ساختار درختی
    # related_name='children' به ما اجازه می‌دهد تا به راحتی از یک والد به فرزندانش دسترسی پیدا کنیم.
  
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Parent Category"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children'  # <-- این نام برای دسترسی آسان به فرزندان است
    )
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return f'{self.slug} ::: of Category ::: {self.name }'

    def get_absolute_url(self):
        """
        یک URL استاندارد برای هر نمونه از دسته‌بندی برمی‌گرداند.
        این متد برای لینک‌دهی تمیز در تمپلیت‌ها استفاده می‌شود.
        """
        return reverse('products:category_list_slug', args=[self.slug])

    
class Comment(models.Model):
    #Product Comment
    title = models.CharField(_("Title"),max_length=150)
    text = models.TextField(_("Text"))
    product = models.ForeignKey("products.Product"
                                ,verbose_name=_("Product")
                                ,on_delete=models.CASCADE   
                                ,related_name="prdct_comments",
                                null=False,
                                blank=False
                                )
    
    rate = models.PositiveSmallIntegerField(
        _("Rate"), validators=[validate_rate]
        )
    user_email = models.EmailField(_("Email"), max_length=254)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
    
    def __str__(self):
        # این خط رو تغییر بده:
        if self.product: # بررسی میکنیم که آیا product وجود داره یا None نیست
            return f'comment on {self.product.name}'
        else:
            return f'Comment (Product not found) - ID: {self.pk}' # اگر product نبود، یک پیام دیگه نشون بده
    
    
class Image(models.Model): 
    
    #Product Image
    name = models.CharField(_("Name"), max_length=50)
    alt = models.CharField(_("Altenative Text"), max_length=100)
    product = models.ForeignKey("Product"
                                ,verbose_name=_("Product")
                                ,on_delete=models.CASCADE       
                                ,related_name="prdct_images" ) # اضافه کردن related_name)
    
    image = models.ImageField(_("Image"),upload_to='product_images')    
    is_default = models.BooleanField(_("is default image"),default=False)
    
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        
    def __str__(self):
        return f'Image of {self.product.name}'
    
    
class Question(models.Model):
    #Product Question
    
    text = models.TextField(_("Question"))
    user_email = models.EmailField(_("Email"), max_length=254)    
    Product_id = models.ForeignKey("Product"
                                ,verbose_name=_("Product")
                                ,on_delete=models.CASCADE       
                                )
    
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        
    def __str__(self):
        return f'Question about  {self.product.name}'
    
    
class Answer(models.Model):
    #Product Answer
    
    text = models.TextField(_("Answer"))
    user_email = models.EmailField(_("Email"), max_length=254)    
    Question_id = models.ForeignKey("Question"
                                ,verbose_name=_("Question")
                                ,on_delete=models.CASCADE       
                                )
    
    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        
    def __str__(self):
        return f'Answer to  {self.text}'   
    
  
class ProductOptions(models.Model):
    #Product Option
    
    product = models.ForeignKey("Product"
                                ,verbose_name=_("Product")    
                                ,on_delete=models.CASCADE
                                ,related_name="prdct_options"  # اضافه کردن related_name
                                )
    
    name = models.CharField(_("Attribute"), max_length=200)         
    value = models.CharField(_("Value"), max_length=200)
    
    class Meta:
        verbose_name = _("Product Option")
        verbose_name_plural = _("Product Options")
        
    def __str__(self):
        return f'{self.product.name}:{self.name}:{self.value}'
    
    
class SellerProductPrice(models.Model):
    #Product Price
    
    product = models.ForeignKey("Product"
                                ,verbose_name=_("Product"),
                                related_name="seller_prices"    
                                ,on_delete=models.CASCADE
                                )
    
    seller = models.ForeignKey(
        "sellers.Seller",
        verbose_name=_("Seller"),
        on_delete=models.CASCADE)


    price = models.PositiveIntegerField(_("Price")) 
    discount = models.PositiveIntegerField(_("Discount"),default=100)   #PositiveIntegerField(_("Price")) 
    create_at = models.DateTimeField(_("First Creation")
                                     ,auto_now=False 
                                     ,auto_now_add=True) 
    update_at = models.DateTimeField(_("Last Update"), auto_now=True)
    
    class Meta:
        verbose_name = _("SellerProductPrice")
        verbose_name_plural = _("SellerProductPrices")
        
    def __str__(self):
        return f'{self.product.name}:{self.price}'
    

 
    
    