# Generated by Django 4.2.7 on 2023-12-17 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_rent_bookinstance_alter_bookinstance_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='status',
        ),
        migrations.AddField(
            model_name='rent',
            name='bookinstance',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='rent', to='app.bookinstance'),
            preserve_default=False,
        ),
    ]