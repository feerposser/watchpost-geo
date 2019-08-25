# Generated by Django 2.2.3 on 2019-07-01 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cidades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelBairro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('bounds_northeast_lat', models.FloatField(blank=True, null=True)),
                ('bounds_northeast_lng', models.FloatField(blank=True, null=True)),
                ('bounds_southwest_lat', models.FloatField(blank=True, null=True)),
                ('bounds_southwest_lng', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('endereco', models.CharField(blank=True, max_length=150, null=True)),
                ('distancia_maxima_km', models.IntegerField()),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('alteracao', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('A', 'ATIVO'), ('D', 'DESATIVADO'), ('I', 'INDEFINIDO')], default='A', max_length=1)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cidades.ModelCidade')),
            ],
            options={
                'verbose_name': 'Informação do bairro',
                'verbose_name_plural': 'Informações dos bairros',
                'db_table': 'bairros',
            },
        ),
        migrations.CreateModel(
            name='ModelBairroAuxiliar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_errado', models.CharField(max_length=100)),
                ('cidade', models.CharField(default='Passo Fundo', max_length=100)),
                ('fk_bairro', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bairros.ModelBairro')),
            ],
            options={
                'verbose_name': 'Informação errada de bairro',
                'verbose_name_plural': 'Informações erradas de bairros',
                'db_table': 'informacao_bairros_auxiliar',
            },
        ),
    ]