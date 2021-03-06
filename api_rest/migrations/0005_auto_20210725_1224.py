# Generated by Django 2.2.9 on 2021-07-25 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0004_movimentacao_carteira'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusDepositoRetirada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='movimentacao',
            name='carteira',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_rest.Carteira'),
        ),
        migrations.CreateModel(
            name='Saque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=50)),
                ('endereco_ip', models.CharField(max_length=39)),
                ('data_solicitacao', models.DateTimeField(auto_now_add=True)),
                ('carteira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_rest.Carteira')),
            ],
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=50)),
                ('endereco_ip', models.CharField(max_length=39)),
                ('data_solicitacao', models.DateTimeField(auto_now_add=True)),
                ('carteira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_rest.Carteira')),
            ],
        ),
    ]
