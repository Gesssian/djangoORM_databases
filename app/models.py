from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from app.utils import STATUS_CHOICES


class Climber(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    peak = models.CharField(verbose_name="Покорил", blank=True, null=True)
    image = models.ImageField(default="images/default.png")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Альпинист"
        verbose_name_plural = "Альпинисты"
        db_table = "climbers"


class Expedition(models.Model):
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')

    def __str__(self):
        return "Экспедиция №" + str(self.pk)

    def get_climbers(self):
        res = []

        for item in ClimberExpedition.objects.filter(expedition=self):
            tmp = item.climber
            tmp.value = item.value
            res.append(tmp)

        return res

    def get_status(self):
        return dict(STATUS_CHOICES).get(self.status)

    class Meta:
        verbose_name = "Экспедиция"
        verbose_name_plural = "Экспедиции"
        ordering = ('-date_formation', )
        db_table = "expeditions"


class ClimberExpedition(models.Model):
    climber = models.ForeignKey(Climber, models.CASCADE)
    expedition = models.ForeignKey(Expedition, models.CASCADE)
    value = models.IntegerField(verbose_name="Поле м-м", blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "climber_expedition"
