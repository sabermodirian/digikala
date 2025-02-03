from django.db import models
from django.utils.translation import gettext as _

class Product(models.Model):   
    
    #Product details
    name = models.CharField(_("Persian Name"),max_length=200)
    en_name = models.CharField(_("English Name"),max_length=200)#Enhlish Name of products
    description = models.TextField(_("Description"))
    category = models.ForeignKey("Category"
                                 ,verbose_name=_("Category")
                                 ,on_delete=models.RESTRICT       # RESTRICT = PROTECT
                                 )
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
                                )
    
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
    
    
class Product_Price(models.Model):
    #Product Price
    
    product_id = models.ForeignKey("Product"
                                ,verbose_name=_("Product")    
                                ,on_delete=models.CASCADE
                                )
    price = models.PositiveIntegerField(_("Price"))    #PositiveIntegerField(_("Price")) 
    create_at = models.DateTimeField(_("First Creation")
                                     ,auto_now=False 
                                     ,auto_now_add=True) 
    update_at = models.DateTimeField(_("Last Update"), auto_now=True)
    
    class Meta:
        verbose_name = _("Product Price")
        verbose_name_plural = _("Product Prices")
        
    def __str__(self):
        return f'{self.product_id.name}:{self.price}'
    

 
    
    