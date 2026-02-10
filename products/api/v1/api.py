from .serializers import PruductSerializer
from ...models import Product
from rest_framework.views import APIView
from rest_framework.response import Response


class ProductList(APIView):
    def get(self,request,format=None):
        ''' یک تابع برای خواندن و گرفتن داده و نمایش آنها'''
        query = Product.objects.all()
        serializer = PruductSerializer(instance=query, many=True)
#TODO نکته: همیشه data را isvalid میکنیم  نه instance را: -->پس نتیجه مگیریم که instance نیازی به ولیدیشن ندارد
        return Response(serializer.data)

    def post(self,request, format=None):
        serializer = PruductSerializer(data=request.data)
         
