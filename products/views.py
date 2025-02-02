from django.shortcuts import render,HttpResponse,get_object_or_404
from.models import Product, Category
#from django.template.loader import get_template 

# Create your views here.

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:10]
    category_response = ''
    
    for c in categories:
        category_response += f'<li>{c.name}</li><br>'
    category_response = f'<ul>{category_response}</ul>'
    
    products_response = ''
    for p in products:
        products_response += f'<li><a href="/products/{p.id}">{p.name}</a></li><br>'
        
    return HttpResponse(f"""
    <html>
    <head>
    <title>DigiKala</title></head>
    <body>
    <h1>The Best Shopping Site in Iran</h1>
    {category_response}
    <h1>Products</h1>
    {products_response}
    </body>
    </html>
    """)
    
def product_view(request,product_id):
       # try:
            #p = Product.objects.get(id=product_id)
            p=get_object_or_404(Product,id=product_id)
            #template = get_template('products/product.html')
            context = {'product':p}                       
           # return HttpResponse(template.render(context={'product':p}))
            return render(request,'products/product.html',context)
        
        #except Product.DoesNotExist:
             #return HttpResponse('404! Product Not Found!!!')
       
      