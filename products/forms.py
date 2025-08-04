from django import forms
from django.core.exceptions import ValidationError

from products.models import Product

class ProductCommentForm(forms.Form):
    user_email = forms.EmailField(required=True , label="ایمیل:")
    title = forms.CharField(max_length=150  , label="عنوان:")
    text = forms.CharField(widget=forms.Textarea , label="متن نظر:")
    rate = forms.IntegerField(max_value=5 , min_value=0  , label="امتیاز:")
    product_id = forms.IntegerField()

    def clean_product_id(self):
        product_id = self.cleaned_data['product_id']
        query = Product.objects.filter(pk=product_id)
        if not query.exists():
            raise ValidationError("the product id is invalid") 
        return product_id

