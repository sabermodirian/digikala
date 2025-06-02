from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse  # noqa: F401


# Create your models here.

class Brand(models.Model):
    name = models.CharField(_("Name"),max_length=150)
    en_name = models.CharField(_("En Name"),max_length=150)
    verbose_name = _("Brand")
    verbose_name_plural = _("Brands")
    def __str__(self):
        return f'{self.id}:{self.name }'

class Product(models.Model):   
    
    #Product details
    name = models.CharField(_("Persian Name"),max_length=200)
    en_name = models.CharField(_("English Name"),max_length=200)#Enhlish Name of products
    description = models.TextField(_("Description"))
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
    
    parent = models.ForeignKey("self",verbose_name=_("Parent Category")
                               ,on_delete=models.SET_NULL
                               ,blank=True,null=True 
                               )
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    def __str__(self):
        return f'{self.slug} ::: of Category ::: {self.name }'
    
class Comment(models.Model):
    #Product Comment
    title = models.CharField(_("Title"),max_length=150)
    text = models.TextField(_("Text"))
    product_id = models.ForeignKey("Product"
                                ,verbose_name=_("Product")
                                ,on_delete=models.CASCADE       
                                )
    
    rate = models.PositiveSmallIntegerField(_("Rate"))
    user_email = models.EmailField(_("Email"), max_length=254)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
    
    def __str__(self):
        return f'comment on {self.product.name}'
    
    
class Image(models.Model): 
    
    #Product Image
    name = models.CharField(_("Name"), max_length=50)
    alt = models.CharField(_("Altenative Text"), max_length=100)
    product_id = models.ForeignKey("Product"
                                ,verbose_name=_("Product")
                                ,on_delete=models.CASCADE       
                                ,related_name="prdct_images" ) # اضافه کردن related_name)
    
    image = models.ImageField(_("Image"),upload_to='product_images')    
    is_default = models.BooleanField(_("is default image"),default=False)
    
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        
    def __str__(self):
        return f'Image of {self.product_id.name}'
    
    
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
    
    product_id = models.ForeignKey("Product"
                                ,verbose_name=_("Product"),
                                related_name="product_sellers"    
                                ,on_delete=models.CASCADE
                                )
    
    seller = models.ForeignKey(
        "sellers.Seller",
        verbose_name=_("Seller"),
        on_delete=models.CASCADE)


    price = models.PositiveIntegerField(_("Price"))    #PositiveIntegerField(_("Price")) 
    create_at = models.DateTimeField(_("First Creation")
                                     ,auto_now=False 
                                     ,auto_now_add=True) 
    update_at = models.DateTimeField(_("Last Update"), auto_now=True)
    
    class Meta:
        verbose_name = _("SellerProductPrice")
        verbose_name_plural = _("SellerProductPrices")
        
    def __str__(self):
        return f'{self.product_id.name}:{self.price}'
    

 
    
    