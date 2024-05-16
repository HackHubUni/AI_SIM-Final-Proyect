Problema:
Las grandes empresas de comida rápida McDonals, BurgerKing establecen cadenas de suministro, pero se quiere 
evaluar cuales serían las mejores situaciones de estas mediante eventos aleatorios como puede ser un evento cultura
que aumente la cantidad de posibles clientes durante un determinado momento
- Se conoce cual es la probabilidad de cada tienda de que entre en cada momento una persona
- la cant de suministro en stock al momento de iniciar la simulación
- los proveedores a los cuales puede acudir a negociar la empresa matriz 
- el dinero que tiene en el balance inicialmente esta empresa matriz analizar
- Se conoce como se comportan las empresas ante diferentes eventos 

Durante cada ejecución de cada experimento de simulación existirá un cjt de elementos fijos:
- La probabilidad y densidad de personas que habrá en una tienda en un momento x y sus comportamientos,
- Las empresas no matriz y sus comportamientos
- Las empresas matrices competidoras de la empresa matriz a analizar y sus comportamientos



Con el objetivo de analizar cuales son el conjunto de comportamientos (hiperparámetros) de la empresa matriz
a analizar deben ser los que debe optar, como el comportamiento de abastecer una tienda x en un momento x
sus habilidaddes de negociacion con una empresa x osea cual debe ser su estrategia para poder aumentar sus ingresos
y disminuir la cant de clientes no satisfechos, tomaremos como óptimo los hiperparámetros
cuando la varianza de los dos indicadores a analizar están bajo un umbral definido por el cliente o por defecto 0.7 mas 100 iteraciones mas para asegurar que no se esta en un minimo local

Se brindarán las sgts respuestas en lenguaje natural:
- Cuáles son las empresas con las que debe de priorizar hacer negocios y compras.  y en que rango de tiempo
- Cuáles son las empresas que pueden traer más complicaciones hacer negocios con ellas.
- Que tiendas se deben de priorizar dado que van a tener más demanda  y en que rango de tiempo
- Qué productos va a tener más demanda por tienda y en cómputo global   y en que rango de tiempo
- Qué escenario es el de su competencia en su mejor escenario  y en que rango de tiempo
- Cuáles son la cant de incidentes promedio, la mediana (dado que queremos conocer donde se concentra estos), max y min esperados 
- Cuáles son los rangos de precios que debe estar dispuesto a pagar por productos a cada proveedor   y en que rango de tiempo
- Cuáles son los productos x que deben estar en los almacenes y en el rango de tiempo (t1,t2)


Respecto a los datos a introducir:


  


- El cjto de tiendas los cuales atenderá la empresa matriz en ese momento sobre estas:
    - La cant de cajas que tiene esta, osea la cant de clientes atender simultaneamente (Esto porfa decirme si lo podemos modelar 
     como que todas tienen una caja y una tienda con dos cajas con la misma tienda con almacenes compartidos)
    - La personas que habran en la tienda en cada momento en cada tienda:
        - Sobre ellas se debe conocer (lo que puso leismael)
    - Las mercancias iniciales estimadas que debe tener la tienda en ese momento (dado que la empresas
   generalmente tienen una cadena de suministro osea es establece que cant de productos a que coste y cuando entran a cada tienda )
    - Los precios iniciales de los productos
- Empresas suministradoras (agricultores, manufacturas, distribuidores y almacenes):
  - Nombre
  - Se debe introducir un balance estimado de esta
  - Los productos que oferta 
  - Los comportamientos de esta:
    - Los precios a ofrecer a cierta empresa matriz
    - La lealtad a cierta a cierta empresa matriz
    - La posibilidad de rechazar una oferta de una empresa matriz
    - La posibilidad de satisfacer un pedido de una empresa matriz sobre los anteriores pedidos
    - Las peculiaridades de cada una como su funcion de reabastecimiento respecto al costo y tiempo a demorar
  
    

- Mapa(Leismael)


Sobre la empresa matriz:
- Se tiene que tener el nombre:
    -Las tiendas a las que abastece,
    - los almacenes donde tiene guardada los productos iniciales asi como cuanto tiempo llevan en ellas (para despues calcualar el precio post tiempo)
    - Balance Money
    - Se variara(Leismael):
  - las valoraciones (1-10) sobre las empresas del mapa 1 mala 10 excelente, en base a un producto u servicio y cant a comprar(esto es por rango de 100 en 100)
  - El precio (min, max) a pagar por producto o servicio,unidad,empresa
  - Cant de producto rango (max y min) x en el almacen y a querer en el rango  tiempo (t1,t2) 
  - Cant de producto rango (max,min) x a abastecer en la tienda y en el rango tiempo (t1,t2)








    