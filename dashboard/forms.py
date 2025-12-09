from django.forms import ModelForm , formset_factory , inlineformset_factory  # noqa: F401
from django import forms  # noqa: F401
from products.models import Product , ProductOptions , SellerProductPrice   

class ProductModelForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  


class ProductOptionsModelForm(ModelForm):
    class Meta:
        model = ProductOptions
        fields = ['name', 'value']

class SellerProductPriceForm(ModelForm):
    class Meta:
        model = SellerProductPrice
        fields = ['seller', 'price', 'discount']

    

ProductOptionsFormSet = inlineformset_factory(
    Product,ProductOptions, form=ProductOptionsModelForm )

SellerProductPriceFormSet = inlineformset_factory(
    Product, SellerProductPrice, form=SellerProductPriceForm)


