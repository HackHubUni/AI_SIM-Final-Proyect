from supply_chain.agents.utils import *
def main():
    cliente_x = ClientWrapped('x')  # Cliente(x)
    valoracion_x_bien = Valoracion("x", ValoracionTag.Bien)  # Valoracion_(x,Bien)

    product_y = ProductWrapped('y')  # Product_(y)

    pedir_precio_hecho = PedirPrecio('x', 'y', NumberWrapped(1))  # Pedir_precio(x,y,1) persona # # producto factor=1

    left_part = AndLogicWrapped(
        [cliente_x, valoracion_x_bien, product_y, pedir_precio_hecho])
    implication_ = ImplicationLogicWrapped(
        [left_part], [pedir_precio_hecho]
    )
    print(implication_.show())

if __name__ =='__main__':
    main()