# -*- coding: utf-8 -*-
"""
seed_db.py
Management command to seed the database with categories, products and prices.

این فایل دیتابیس را با دسته‌بندی‌ها، محصولات و قیمت‌ها پر می‌کند.
روش استفاده:
    python manage.py seed_db
"""

import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product, Category, SellerProductPrice
from sellers.models import Seller



class Command(BaseCommand):
    """
    Seeds the database with a tree of categories and some products for each category.
    همچنین پیام‌های پیشرفت را به stdout می‌نویسد.
    """
    help = 'Seeds the database with categories, products, and prices.'

    def handle(self, *args, **options):
    # اطمینان از وجود یک فروشنده‌ی پایه
        seller, created = Seller.objects.get_or_create(
            slug='digi-seller',
            defaults={'name': 'DiGi Seller'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✅ فروشنده‌ی پیش‌فرض ساخته شد: DiGi Seller"))
        else:
            self.stdout.write("ℹ️ فروشنده‌ی پیش‌فرض از قبل وجود داشت: DiGi Seller")

    # حالا از متغیر seller برای ساخت محصولات استفاده کن
    # example: Product.objects.create(name='...', seller=seller, ...)
        self.stdout.write("🔥 شروع عملیات پاکسازی دیتابیس محصولات و دسته‌بندی‌ها...")
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✅ پاکسازی با موفقیت انجام شد."))

        # دریافت اولین فروشنده؛ اگر نباشد عملیات متوقف می‌شود
        seller = Seller.objects.first()
        if not seller:
            self.stderr.write(self.style.ERROR(
                "❌ هیچ فروشنده‌ای در دیتابیس وجود ندارد! ابتدا یک Seller بسازید."
            ))
            return

        self.stdout.write(f"😎 فروشنده انتخاب شد: {seller.name}")

        # لیست ۱۰ دسته‌بندی اصلی (name, slug)
        root_cats_data = [
            ("کالای دیجیتال", "digital-goods"),
            ("مد و پوشاک", "fashion-clothing"),
            ("خانه و آشپزخانه", "home-kitchen"),
            ("زیبایی و سلامت", "beauty-health"),
            ("اسباب بازی", "toys-hobbies"),
            ("کتاب و لوازم تحریر", "books-stationery"),
            ("ورزش و سفر", "sports-travel"),
            ("ابزار و اداری", "tools-industrial"),
            ("خودرو و موتورسیکلت", "vehicles-parts"),
            ("محصولات بومی و محلی", "native-local-products"),
        ]

        self.stdout.write("🚀 شروع عملیات سنگین ساخت و ساز...")

        # ساخت درخت دسته‌ها و ایجاد محصولات برای هر کدام
        for name, slug in root_cats_data:
            # سطح 1
            root, _ = Category.objects.get_or_create(
                slug=slug, defaults={'name': name}
            )
            self.stdout.write(f"\n📂 دسته اصلی: {root.name}")
            self.create_products_for_cat(root, seller)

            # دو زیرمجموعه سطح 2
            for i in range(1, 3):
                sub1_name = f"{root.name} - زیرمجموعه {i}"
                sub1_slug = f"{root.slug}-sub-{i}"
                sub1, _ = Category.objects.get_or_create(
                    slug=sub1_slug,
                    defaults={'name': sub1_name, 'parent': root}
                )
                self.create_products_for_cat(sub1, seller)

                # دو زیر-زیرمجموعه سطح 3
                for j in range(1, 3):
                    sub2_name = f"{sub1.name} - بخش {j}"
                    sub2_slug = f"{sub1.slug}-part-{j}"
                    sub2, _ = Category.objects.get_or_create(
                        slug=sub2_slug,
                        defaults={'name': sub2_name, 'parent': sub1}
                    )
                    self.create_products_for_cat(sub2, seller)

        self.stdout.write(self.style.SUCCESS("\n🎉 تمام شد! دیتابیس با موفقیت پر شد!"))

    def create_products_for_cat(self, cat_obj, seller, count=4):
        """
        Create `count` products for a given category and attach a SellerProductPrice.
        برای هر محصول، قیمت و مقدار تخفیف به صورت رندوم تعیین می‌شود.
        """
        for i in range(1, count + 1):
            p_name = f"{cat_obj.name} - مدل حرفه‌ای {random.randint(100, 999)}"
            price = random.randint(100, 5000) * 10000  # قیمت به تومان یا واحد دلخواه
            disc = random.randint(0, 30)  # تخفیف 0 تا 30 درصد

            prod = Product.objects.create(
                name=p_name,
                en_name=f"Product-{slugify(cat_obj.slug)}-{random.randint(1000, 9999)}",
                description=f"این یک محصول تست برای دسته {cat_obj.name} است.",
                category=cat_obj,
                is_active=True
            )

            SellerProductPrice.objects.create(
                product=prod,
                seller=seller,
                price=price,
                discount=disc
            )

        self.stdout.write(f"   ➕ {count} محصول به '{cat_obj.name}' اضافه شد.")
