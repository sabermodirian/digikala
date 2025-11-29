from django.forms import ModelForm , formset_factory , inlineformset_factory  # noqa: F401
from django import forms  # noqa: F401
from products.models import Product , ProductOptions

class ProductModelForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  


class ProductOptionModelForm(ModelForm):
    class Meta:
        model = ProductOptions
        fields = '__all__' 

    

ProductFormSet = inlineformset_factory(Product, 
ProductOptions, fields=['name', 'value'])
