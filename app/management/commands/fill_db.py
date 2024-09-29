import random

from django.core.management.base import BaseCommand
from minio import Minio

from ...models import *
from .utils import random_date, random_timedelta


def add_users():
    User.objects.create_user("user", "user@user.com", "1234")
    User.objects.create_superuser("root", "root@root.com", "1234")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234")

    print("Пользователи созданы")


def add_climbers():
    Climber.objects.create(
        name="Эдмунд Хилари",
        description="В 11:30 утра 29 мая 1953 г. Эдмунд Хиллари из Новой Зеландии и Тенцинг Норгей, шерпа из Непала, стали первыми известными исследователями, достигшими вершины горы Эверест, которая на высоте 29 035 футов над уровнем моря является самой высокой точкой на земле. Эти двое в составе британской экспедиции совершили свой последний штурм вершины, проведя беспокойную ночь на высоте 27 900 футов. Новость об их достижении облетела весь мир 2 июня, в день коронации королевы Елизаветы II, и британцы приветствовали это как хорошее предзнаменование для будущего их страны.",
        peak="Эверест",
        image="images/1.png"
    )

    Climber.objects.create(
        name="Маттиас Цурбригген",
        description="В 1892 году английский барон и альпинист Мартин Конвей нанял Маттиаса для участия в своей экспедиции по Каракоруму. В рамках этой экспедиции, которая заняла 8 месяцев, они совершили первое восхождение на Пионер-Пик (6890 метров; второстепенный пик вершины Балторо-Кангри) с ледника Балторо, что являлось высочайшей покорённой вершиной в мире на тот момент.",
        peak="Аконкагуа",
        image="images/2.png"
    )

    Climber.objects.create(
        name="Хадсон Стак",
        description="Первое подтвержденное восхождение — американская экспедиция под командой преподобного Хадсона Стака. Самый простой и популярный маршрут на Денали — по Западному контрфорсу. Кроме технической сложности (маршрут относительно простой), при восхождении на Денали существенным фактором является погода — при ее ухудшении температура может опускаться до -40°С при штормовом ветре",
        peak="Денали",
        image="images/3.png"
    )

    Climber.objects.create(
        name="Ганс Мейер",
        description="Первое восхождение совершено в 1889 году немецким путешественником Гансом Мейером и австрийским альпинистом Людвигом Пуртшеллером. На вершину Ухуру ведут 6 простых маршрута — Марангу, Умбве, Шира, Немошо, Ронгаи и Машаме, не требующий альпинистской подготовки. Самый популярный, благодаря инфраструктуре — хижинам и пр. — Марангу, по нему заходит основная масса восходителей. Вершину Килиманджаро покрывает снежно-ледовая шапка, однако в последние годы она стремительно тает.",
        peak="Килиманджаро",
        image="images/4.png"
    )

    Climber.objects.create(
        name="Фредерик Кук",
        description="Высшая точка Северной Америка, находится на Аляске. Первое восхождение было совершено в начале прошлого века: в 1906 году Фредериком Куком, однако есть сомнения что он достиг вершины. Первое подтвержденное восхождение — американская экспедиция под командой преподобного Хадсона Стака.",
        peak="Мак-Кинли",
        image="images/5.png"
    )

    Climber.objects.create(
        name="Килар Хаширов",
        description="Высшая точка Кавказа и Европы в особых представлениях не нуждается. Первое восхождение на Восточную вершину Эльбруса (5621) совершил 10 июля 1829 горный проводник Килар Хаширов, участвовавший в экспедиции под руководством генерала Г.А. Эммануэля.",
        peak="Эльбрус",
        image="images/6.png"
    )

    client = Minio("minio:9000", "minio", "minio123", secure=False)
    client.fput_object('images', '1.png', "app/static/images/1.png")
    client.fput_object('images', '2.png', "app/static/images/2.png")
    client.fput_object('images', '3.png', "app/static/images/3.png")
    client.fput_object('images', '4.png', "app/static/images/4.png")
    client.fput_object('images', '5.png', "app/static/images/5.png")
    client.fput_object('images', '6.png', "app/static/images/6.png")
    client.fput_object('images', 'default.png', "app/static/images/default.png")

    print("Услуги добавлены")


def add_expeditions():
    users = User.objects.filter(is_superuser=False)
    moderators = User.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    climbers = Climber.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        add_expedition(status, climbers, users, moderators)

    add_expedition(1, climbers, users, moderators)

    print("Заявки добавлены")


def add_expedition(status, climbers, users, moderators):
    expedition = Expedition.objects.create()
    expedition.status = status

    if expedition.status in [3, 4]:
        expedition.date_complete = random_date()
        expedition.date_formation = expedition.date_complete - random_timedelta()
        expedition.date_created = expedition.date_formation - random_timedelta()
    else:
        expedition.date_formation = random_date()
        expedition.date_created = expedition.date_formation - random_timedelta()

    expedition.owner = random.choice(users)
    expedition.moderator = random.choice(moderators)

    for climber in random.sample(list(climbers), 3):
        item = ClimberExpedition(
            expedition=expedition,
            climber=climber,
            value=random.randint(1, 10)
        )
        item.save()

    expedition.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_climbers()
        add_expeditions()



















