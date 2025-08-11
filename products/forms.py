from django import forms
from django.core.exceptions import ValidationError  # noqa: F401

from .models import Comment

# class ProductCommentForm(forms.Form):
#     user_email = forms.EmailField(required=True , label="ایمیل:" , 
#      widget=forms.EmailInput(attrs={'class': 'form-control',
#       'placeholder': 'لطفا ایمیل خود را وارد کنید'})      
#     )

#     title = forms.CharField(max_length=150  , label="عنوان:",
#      widget=forms.TextInput(attrs={'class': 'form-control',
#       'placeholder': 'لطفا عنوان نظر خود را وارد کنید'})
#     )
#     text = forms.CharField(max_length=1000  , label="متن نظر:",
#      widget=forms.Textarea(attrs={'class': 'form-control',
#       'placeholder': 'لطفا متن نظر خود را وارد کنید'})
#     )
#     rate = forms.IntegerField(max_value=5 , min_value=0  , label="امتیاز:",
#      widget=forms.NumberInput(attrs={'class': 'form-control',
#       'placeholder': 'لطفا امتیاز خود را وارد کنید'})
#     )
#     product_id = forms.IntegerField(widget=forms.HiddenInput())


    # password = forms.CharField(widget=forms.PasswordHiddenInput)
    # password2 = forms.CharField(widget=forms.passwordhiddeninput)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data['password']
    #     password2 = cleaned_data['password2']
    #     if password != password2:
    #         raise ValidationError({"password":"passwords do not match"})
        
        
        #return password

    # def clean_product_id(self):
    #     product_id = self.cleaned_data['product_id']
    #     query = Product.objects.filter(pk=product_id)
    #     if not query.exists():
    #         raise ValidationError("the product id is invalid") 
    #     return product_id

class ProductCommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = "__all__" #['user_email' , 'title' , 'text' , 'rate' , 'product_id']  all fields
       
        widgets = {
            'user_email': forms.EmailInput(attrs={'class': 'form-control',
            'placeholder': 'لطفا ایمیل خود را وارد کنید'
            ,  'style': 'background-color: lightyellow;'}),

            'title': forms.TextInput(attrs={'class': 'form-control',
            'placeholder': 'لطفا عنوان نظر خود را وارد کنید'
            ,  'style': 'background-color: lightyellow;'}),

            'text': forms.Textarea(attrs={'class': 'form-control',
            'placeholder': 'لطفا متن نظر خود را وارد کنید',
            'style': 'background-color: lightyellow;'}),

            'rate': forms.NumberInput(attrs={'class': 'form-control',
            'placeholder': 'لطفا امتیاز خود را وارد کنید',
            'style': 'background-color: lightyellow;'}),

            'product': forms.HiddenInput(),

        }
    def save(self , commit=True):

        return super().save(commit=commit)