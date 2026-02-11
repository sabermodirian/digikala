from .serializers import ProductSerializer
from ...models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status





class ProductList(APIView):
    ''' List all products , or craete a new Product '''
    def get(self,request,format=None):
        ''' یک تابع برای خواندن و گرفتن داده و نمایش آنها'''
        query = Product.objects.all()
        serializer = ProductSerializer(instance=query, many=True)
#TODO نکته: همیشه data را isvalid میکنیم  نه instance را: -->پس نتیجه مگیریم که instance نیازی به ولیدیشن ندارد
        return Response(serializer.data)

    def post(self,request, format=None):
        ''' یک تابع برای ایجاد و تولید داده آنها'''
        serializer = ProductSerializer(data=request.data) #چون میخایم دیتا را ایجاد بکنیم فقط data را بعنوان آرگومان میدیم
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
         
class ProductDetail(APIView):
    '''Retrieve , Update or Delete a product instance '''
    def get_object(self,pk):
        ''']جون در همهی توابع این کلاس به یک ID یا شماره ای تز نمونه های یک محصول نیازداریم
        پس یک تابع جداگانه ای برای تشخیص و گرفتن آیدی هر محصول  '''
         
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        ''' یک تابع برای خواندن و گرفتن داده هر محصول و نمایش  جزییات آن محصول ا'''
        prdct_obj = self.get_object(pk)
        serializer = ProductSerializer(instance=prdct_obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        ''' تابعی برای بروزرسانی  یا ویرایش و آپدیت هر محصول'''
        prdct_obj = self.get_object(pk)
        serializer = ProductSerializer(instance=prdct_obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """   تابعی برای حذف هر محصول که به سریالایزر هم نیازی ندارد چون
        هیچ کانتنتی و محصولی را برنمیگرداند"""
        prdct_obj = self.get_object(pk)
        prdct_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        
     
         



