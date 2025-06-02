from django.shortcuts import render,get_object_or_404 #,httpResponse
from.models import Product # ,Category
#from django.template.loader import get_template 

# Create your views here.

def product_list_view(request):
    #categories = Category.objects.all()
    products = Product.objects.all()[:10]
    context = {'products':products}
    return render(request,
                  template_name='products/product-list.html'
                  ,context=context)
    
   
    
def  product_detail_view(request,pk):
       # try:
            #p = Product.objects.get(id=product_id)
            p=get_object_or_404(Product,id=pk)
          # template = get_template('products/product.html')
            context = {'product':p} 
            
            # با توجه به @property در مدل، product.default_image آماده استفاده است
            context = {
                'product':p,
                # اگر می‌خواهید جداگانه توی کانتکست داشته باشید:
                'default_img':p.default_image,
            }                      
          # return HttpResponse(template.render(context={'product':p}))
            return render(request,'products/product-detail.html',context)
        
        #except Product.DoesNotExist:
             #return HttpResponse('404! Product Not Found!!!')
       
      