from django.shortcuts import render  
from .forms import ProductFormSet , ProductModelForm

# Create your views here.


def create_product(request):
    inlines = (ProductFormSet(),)
    form = ProductModelForm(request.POST or None)
    form.inlines = inlines
    return render(request,
     'dashboard/create_product.html',
      {'form': form}
      )