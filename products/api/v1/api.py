from .serializers import ProductSerializer , ProductListSerializer
from ...models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination  # noqa: F401
from rest_framework.permissions import IsAuthenticated , IsAdminUser ,IsAuthenticatedOrReadOnly  # noqa: F401
from .permissions import IsAdminOrReadOnly
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet #کاملترین نوع view ها که همیه حالات جنگو را دربر میگیرد
from rest_framework.decorators import action



class ProductList(APIView):
    ''' List all products , or create a new Product in classic APIView'''
    permission_classes = [IsAdminOrReadOnly]
    # 1. این خط کلید ماجراست! 🔑
    # با این خط به DRF می‌فهمونیم که این کلاس قراره صفحه‌بندی داشته باشه
    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        ''' یک تابع برای خواندن و گرفتن داده و نمایش آنها'''
        queryset = Product.objects.all().select_related('brand','category')

        # 2. ساختن نمونه از کلاسی که بالا تعریف کردیم
        self.paginator = self.pagination_class()
        
        # تنظیمات دلخواه (می‌تونی اینا رو توی settings.py هم ببری)
        self.paginator.page_size = 15

        # 3. نکته مهم: پاس دادن 'view=self' 🎯
        # این باعث میشه پجینیتور بفهمه صاحبش کیه و دکمه‌ها رو درست بسازه
        result_page = self.paginator.paginate_queryset(queryset, request, view=self)

        # اگر صفحه‌بندی انجام شد (یعنی result_page خالی نبود)
        if result_page is not None:
            serializer = ProductListSerializer(result_page, many=True)
            # 4. برگرداندن ریسپانس مخصوص (شامل دکمه‌ها و لینک‌ها)
            return self.paginator.get_paginated_response(serializer.data)

        # حالت fallback (اگر صفحه‌بندی کار نکرد، کل دیتا رو بده - که معمولاً پیش نمیاد)
        serializer = ProductListSerializer(queryset, many=True)
#TODO نکته: همیشه data را isvalid میکنیم  نه instance را: -->پس نتیجه مگیریم که instance نیازی به ولیدیشن ندارد

        return Response(serializer.data)



    def post(self,request, format=None):
        ''' یک تابع برای ایجاد و تولید داده آنها'''
        serializer = ProductListSerializer(data=request.data) #چون میخایم دیتا را ایجاد بکنیم فقط data را بعنوان آرگومان میدیم
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
         


class ProductDetail(APIView):
    '''Retrieve , Update or Delete a product instance '''
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self,pk):
        ''']جون در همهی توابع این کلاس به یک ID یا شماره ای تز نمونه های یک محصول نیازداریم
        پس یک تابع جداگانه ای برای تشخیص و گرفتن آیدی هر محصول  '''
         
        try:
            return Product.objects.select_related('brand','category').get(pk=pk)
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
    
        
# class ProductListGenericView(generics.ListAPIView):
#     '''میباشد GET ALL  فقط دارای متد generics در مد  ListAPIViewاستفاده از '''
         
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer

class ProductListGenericView(generics.ListCreateAPIView):
  '''میباشد GET ,POST   دارای هر دو متد generics در مد  ListCreateAPIView استفاده از '''
  queryset = Product.objects.all()
  serializer_class = ProductListSerializer
  
         

class ProductDetailGenericView(generics.RetrieveUpdateDestroyAPIView):

    '''همهی حالات متدهای مختلف برای گرفتن و ویرایش و حذف جزییات اطلاعات برای یک محصول خاص را دارد  RetrieveUpdateDestroyAPIView استفاده از '''

    serializer_class = ProductSerializer
    queryset = Product.objects.all().select_related(
        'brand','category').prefetch_related('sellers')

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            # 'links': {
            #     'next': self.get_next_link(),
            #     'previous': self.get_previous_link()
            # },
            'count': self.page.paginator.count,
            'results': data
        })

class ProductModelVS(ModelViewSet):
    '''(CRUD کامل) در بر گیرنده کامل همهی متدهای جنگو دریک کلاس میباشد ModelViewSet'''
    
    # serializer_class = ProductSerializer
    # queryset = Product.objects.all().select_related(
    #     'brand','category').prefetch_related('sellers')

    serializer_class = ProductListSerializer  #اتریبیوت serializer_class
    queryset = Product.objects.all()    #اتریبیوت queryset

    pagination_class = CustomPagination
    
    def get_serializer_class(self):
    # رو میخونه و پاس میده وقتیکه به فانکشنش برای  CBV مشابه هر اتریبیوتی در 
    # کردن نیاز هستش override یک فانکشنی وجود داره که این اتریبیوت 
        if self.action == 'List' or self.action == 'create':
            return self.serializer_class # = return ProductListSerializer
        else:
            return ProductSerializer

      #exstra action in viewset
    @action(detail=True , methods=['post'])
    def liked(self,request,pk): 
        prdct_obj:Product=self.get_object() # میسازد Product  نام متغریست که یک شیئ از جنس  prdct_obj
        # prdct_obj:Product ==> TYPE(prdct_obj) = Product
        prdct_obj.liked_users.add(request.user)
        serializer=self.get_serializer(instance=prdct_obj)
        return Response(data=serializer.data, status=201)

    # def get_queryset(self):
    #     query = Product.objects.filter(owner = self.request.user)
    #     return query #فقط محصولات مربوط به کاربر فعلی را نمایش بده
    
    
