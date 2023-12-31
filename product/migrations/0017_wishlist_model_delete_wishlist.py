# Generated by Django 4.2.5 on 2023-11-06 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import parler.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0016_remove_wishlist_product_alter_wishlist_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist_model',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'wishlists',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
