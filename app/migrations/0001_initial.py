# Generated by Django 4.2.7 on 2023-12-16 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField(max_length=256)),
                ('author', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(1, 'Available'), (0, 'Not available')])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookinstances', to='app.book')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('reader_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_taken', models.DateField()),
                ('bookinstance', models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.PROTECT, related_name='rents', to='app.bookinstance')),
                ('reader', models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.PROTECT, related_name='rents', to='app.reader')),
                ('user', models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.PROTECT, related_name='rents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='app.genre'),
        ),
    ]
