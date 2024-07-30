from .models import Category


# К каждой просматриваемой странице есть доступ к просмотру категорий
def categories(request):
    return {'categories': Category.objects.all()}
