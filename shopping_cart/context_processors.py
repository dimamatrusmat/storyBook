from .basket import Basket


# В каждой просматриваемой странице есть доступ к просмотру Корзины
def basket(request):
    return {'basket': Basket(request)}
