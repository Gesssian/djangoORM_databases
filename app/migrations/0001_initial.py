# Generated by Django 4.2.7 on 2024-10-14 19:41

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
            name='Climber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='Описание')),
                ('status', models.IntegerField(choices=[(1, 'Действует'), (2, 'Удалена')], default=1, verbose_name='Статус')),
                ('image', models.ImageField(default='images/default.png', upload_to='', verbose_name='Фото')),
                ('peak', models.CharField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Альпинист',
                'verbose_name_plural': 'Альпинисты',
                'db_table': 'climbers',
            },
        ),
        migrations.CreateModel(
            name='Expedition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Введён'), (2, 'В работе'), (3, 'Завершен'), (4, 'Отклонен'), (5, 'Удален')], default=1, verbose_name='Статус')),
                ('date_created', models.DateTimeField(blank=True, null=True, verbose_name='Дата создания')),
                ('date_formation', models.DateTimeField(blank=True, null=True, verbose_name='Дата формирования')),
                ('date_complete', models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')),
                ('moderator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='moderator', to=settings.AUTH_USER_MODEL, verbose_name='Модератор')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Экспедиция',
                'verbose_name_plural': 'Экспедиции',
                'db_table': 'expeditions',
                'ordering': ('-date_formation',),
            },
        ),
        migrations.CreateModel(
            name='ClimberExpedition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(blank=True, null=True, verbose_name='Поле м-м')),
                ('climber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.climber')),
                ('expedition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.expedition')),
            ],
            options={
                'verbose_name': 'м-м',
                'verbose_name_plural': 'м-м',
                'db_table': 'climber_expedition',
                'unique_together': {('climber', 'expedition')},
            },
        ),
    ]
