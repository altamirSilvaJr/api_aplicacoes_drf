# Generated by Django 2.2.9 on 2021-07-25 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0003_carteira'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentacao',
            name='carteira',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api_rest.Carteira'),
        ),
    ]
