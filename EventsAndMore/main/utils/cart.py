from django.db.models import F

from .models import Carro, Elementos_Carro


class Cart(object):
    def __init__(self, cliente, evento, stand):
        self.cliente = cliente
        self.evento = evento
        self.stand = stand
        self.carro = Carro.objects.get_or_create(cliente=cliente, evento=evento, stand=stand)[0]

    def add(self, servicio, cantidad=1):
        if cantidad < 1:
            raise ValueError('La cantidad debe ser mayor a 0')
        print(self.carro)
        if Elementos_Carro.objects.filter(carro=self.carro, servicio=servicio).exists():
            Elementos_Carro.objects.filter(carro=self.carro, servicio=servicio).update(
                cantidad=F('cantidad') + cantidad)
        else:
            Elementos_Carro.objects.create(carro=self.carro, servicio=servicio, cantidad=cantidad)

    def remove(self, servicio):
        if Elementos_Carro.objects.filter(carro=self.carro, servicio=servicio).exists():
            Elementos_Carro.objects.filter(carro=self.carro, servicio=servicio).delete()
        else:
            raise ValueError('El servicio no existe en el carro')

    def clear(self):
        Elementos_Carro.objects.filter(carro=self.carro).delete()

    def remove_cart(self):
        self.clear()
        self.carro.delete()

    def set_quantity(self, servicio, cantidad):

        if int(cantidad) < 1:
            raise ValueError('La cantidad debe ser mayor a 0')
        if Elementos_Carro.objects.filter(carro=self.carro, servicio=servicio).exists():
            Elementos_Carro.objects.filter(carro=self.carro, servicio=servicio).update(
                cantidad=int(cantidad))

    def __iter__(self):
        for item in self.items:
            yield item

    def is_empty(self):
        return self.total == 0

    @property
    def items(self):
        return Elementos_Carro.objects.filter(carro=self.carro)

    @property
    def total(self):
        return sum(item.cantidad * item.servicio.precio for item in self.items)

