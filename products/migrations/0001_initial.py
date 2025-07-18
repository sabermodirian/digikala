# Generated by Django 4.2.1 on 2025-06-08 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sellers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('en_name', models.CharField(max_length=150, verbose_name='En Name')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug_Cat')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='category_images', verbose_name='Icon')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images', verbose_name='Image')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category', verbose_name='Parent Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Persian Name')),
                ('en_name', models.CharField(max_length=200, verbose_name='English Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.brand', verbose_name='Brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='products.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='SellerProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(verbose_name='Price')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='First Creation')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Last Update')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_sellers', to='products.product', verbose_name='Product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.seller', verbose_name='Seller')),
            ],
            options={
                'verbose_name': 'SellerProductPrice',
                'verbose_name_plural': 'SellerProductPrices',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Question')),
                ('user_email', models.EmailField(max_length=254, verbose_name='Email')),
                ('Product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='ProductOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Attribute')),
                ('value', models.CharField(max_length=200, verbose_name='Value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prdct_options', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Option',
                'verbose_name_plural': 'Product Options',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='sellers',
            field=models.ManyToManyField(through='products.SellerProductPrice', to='sellers.seller', verbose_name='Sellers'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('alt', models.CharField(max_length=100, verbose_name='Altenative Text')),
                ('image', models.ImageField(upload_to='product_images', verbose_name='Image')),
                ('is_default', models.BooleanField(default=False, verbose_name='is default image')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prdct_images', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('text', models.TextField(verbose_name='Text')),
                ('rate', models.PositiveSmallIntegerField(verbose_name='Rate')),
                ('user_email', models.EmailField(max_length=254, verbose_name='Email')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Answer')),
                ('user_email', models.EmailField(max_length=254, verbose_name='Email')),
                ('Question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
    ]
