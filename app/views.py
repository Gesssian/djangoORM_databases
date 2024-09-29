from django.shortcuts import render

climbers = [
    {
        "id": 1,
        "name": "Эдмунд Хилари",
        "description": "В 11:30 утра 29 мая 1953 г. Эдмунд Хиллари из Новой Зеландии и Тенцинг Норгей, шерпа из Непала, стали первыми известными исследователями, достигшими вершины горы Эверест, которая на высоте 29 035 футов над уровнем моря является самой высокой точкой на земле. Эти двое в составе британской экспедиции совершили свой последний штурм вершины, проведя беспокойную ночь на высоте 27 900 футов. Новость об их достижении облетела весь мир 2 июня, в день коронации королевы Елизаветы II, и британцы приветствовали это как хорошее предзнаменование для будущего их страны.",
        "peak": "Эверест",
        "image": "http://localhost:9000/images/1.png"
    },
    {
        "id": 2,
        "name": "Маттиас Цурбригген",
        "description": "В 1892 году английский барон и альпинист Мартин Конвей нанял Маттиаса для участия в своей экспедиции по Каракоруму. В рамках этой экспедиции, которая заняла 8 месяцев, они совершили первое восхождение на Пионер-Пик (6890 метров; второстепенный пик вершины Балторо-Кангри) с ледника Балторо, что являлось высочайшей покорённой вершиной в мире на тот момент.",
        "peak": "Аконкагуа",
        "image": "http://localhost:9000/images/2.png"
    },
    {
        "id": 3,
        "name": "Хадсон Стак",
        "description": "Первое подтвержденное восхождение — американская экспедиция под командой преподобного Хадсона Стака. Самый простой и популярный маршрут на Денали — по Западному контрфорсу. Кроме технической сложности (маршрут относительно простой), при восхождении на Денали существенным фактором является погода — при ее ухудшении температура может опускаться до -40°С при штормовом ветре",
        "peak": "Денали",
        "image": "http://localhost:9000/images/3.png"
    },
    {
        "id": 4,
        "name": "Ганс Мейер",
        "description": "Первое восхождение совершено в 1889 году немецким путешественником Гансом Мейером и австрийским альпинистом Людвигом Пуртшеллером. На вершину Ухуру ведут 6 простых маршрута — Марангу, Умбве, Шира, Немошо, Ронгаи и Машаме, не требующий альпинистской подготовки. Самый популярный, благодаря инфраструктуре — хижинам и пр. — Марангу, по нему заходит основная масса восходителей. Вершину Килиманджаро покрывает снежно-ледовая шапка, однако в последние годы она стремительно тает.",
        "peak": "Килиманджаро",
        "image": "http://localhost:9000/images/4.png"
    },
    {
        "id": 5,
        "name": "Фредерик Кук",
        "description": "Высшая точка Северной Америка, находится на Аляске. Первое восхождение было совершено в начале прошлого века: в 1906 году Фредериком Куком, однако есть сомнения что он достиг вершины. Первое подтвержденное восхождение — американская экспедиция под командой преподобного Хадсона Стака",
        "peak": "Мак-Кинли",
        "image": "http://localhost:9000/images/5.png"
    },
    {
        "id": 6,
        "name": "Килар Хаширов",
        "description": "Высшая точка Кавказа и Европы в особых представлениях не нуждается. Первое восхождение на Восточную вершину Эльбруса (5621) совершил 10 июля 1829 горный проводник Килар Хаширов, участвовавший в экспедиции под руководством генерала Г.А. Эммануэля.",
        "peak": "Эльбрус",
        "image": "http://localhost:9000/images/6.png"
    }
]

draft_expedition = {
    "id": 123,
    "status": "Черновик",
    "date_created": "12 сентября 2024г",
    "climbers": [
        {
            "id": 1,
            "count": 2
        },
        {
            "id": 2,
            "count": 1
        },
        {
            "id": 3,
            "count": 3
        }
    ]
}


def getClimberById(climber_id):
    for climber in climbers:
        if climber["id"] == climber_id:
            return climber


def getClimbers():
    return climbers


def searchClimbers(climber_name):
    res = []

    for climber in climbers:
        if climber_name.lower() in climber["name"].lower():
            res.append(climber)

    return res


def getDraftExpedition():
    return draft_expedition


def getExpeditionById(expedition_id):
    return draft_expedition


def index(request):
    climber_name = request.GET.get("climber_name", "")
    climbers = searchClimbers(climber_name) if climber_name else getClimbers()
    draft_expedition = getDraftExpedition()

    context = {
        "climbers": climbers,
        "climber_name": climber_name,
        "climbers_count": len(draft_expedition["climbers"]),
        "draft_expedition": draft_expedition
    }

    return render(request, "home_page.html", context)


def climber(request, climber_id):
    context = {
        "id": climber_id,
        "climber": getClimberById(climber_id),
    }

    return render(request, "climber_page.html", context)


def expedition(request, expedition_id):
    expedition = getExpeditionById(expedition_id)
    climbers = [
        {**getClimberById(climber["id"]), "count": climber["count"]}
        for climber in expedition["climbers"]
    ]

    context = {
        "expedition": expedition,
        "climbers": climbers
    }

    return render(request, "expedition_page.html", context)

