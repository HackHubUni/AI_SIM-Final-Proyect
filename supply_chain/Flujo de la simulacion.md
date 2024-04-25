# Flujo de la simulación

## Inicio

Al inicio de la simulación como no hay eventos creados se tiene que pasar por cada empresa de la simulación (empresas matrices y del mapa) y llamar a un método común en todas las empresas `Start()`. Este método lo que hace es crear los eventos iniciales de cada una para su correcto funcionamiento.

### Descripción del `Start()` de cada empresa

#### Proveedores

- Crear un evento del momento en que se tiene que hacer `restock`. Recordar que los proveedores tienen en general un tiempo fijo $t$ con el que se separan todos los eventos de `restock`.
  - A la hora de procesar este evento se tiene que reabastecer cada producto del proveedor (con la calidad inicial que deben tener estos productos) y generar el próximo evento de `restock`

### Manufactores

Los manufactores tienen 2 servicios que ofrecen. Uno es la venta de productos que él mágicamente produce (pagando un costo por su `restock`) y otro es el servicio de creación de nuevos productos pidiendo ciertos ingredientes (productos necesarios junto con la cantidad de estos) (la calidad mínima de los productos puede ser útil pero por ahora se quita).
Entonces, el método `Start()` de esta empresa hace lo siguiente (lo mismo que el proveedor):
- Crear el primer evento de `restock` que rellena los productos necesarios para ofrecer el primer servicio descrito.
  - A la hora de procesar este evento se tiene que reabastecer cada producto que el manufactor ofrece (con la calidad inicial que deben tener estos productos) y generar el próximo evento de `restock`

### Almacenes

Los almacenes ofrecen el servicio de almacenar productos a empresas matrices. Para cada empresa matriz el almacén crea eventos de cuando toca cobrarle a la empresa matriz por sus servicios.
La lógica del cobro del servicio de almacén es el siguiente:
- En el momento en que una empresa matriz pide almacenar productos entonces el almacén crea un evento de `CobrarServicio` (ponerle otro nombre al evento, en ingles) para que se ejecute en el tiempo correspondiente.

Ahora, en la lógica del método `Start()` se crea el evento de `CobrarServicio` para cada una de las empresas que tienen productos almacenados al comienzo de la simulación (notar que los almacenes deben tener internamente una forma de saber que productos son de cada empresa).

### Tiendas

<!-- TODO: Agregar el punto de que las tiendas solo tienen un reabastecimiento mágico y este ocurre al inicio de la simulación -->
Las tiendas son las únicas empresas en la simulación que atienden clientes y son estas las que desencadenan el resto de las acciones a realizar en la simulación luego de la inicialización.

La lógica que se debe ejecutar en el método `Start()` de la tienda es la siguiente:
- Se debe crear el evento de `restock` que dice en que momento llegarán productos a la tienda.
  - A la hora de procesar este evento se hace lo mismo que con los proveedores y manufactores, es decir, se generan productos con una calidad inicial y se añaden a la tienda.
- Se debe crear el evento de `ClientArrival` que no es más que el evento que determina el momento en que un cliente llegará a la tienda (por ahora esto se hace por medio de la distribución Poisson). A la hora de procesar este evento se hace lo siguiente:
  - Se genera un nuevo cliente con sus características propias de sabor favorito y propiedades nutritivas que busca, así como también el hambre que tiene.
  - Se agrega el cliente a la cola de la tienda.
  - Se llama al cliente recién creado su método `Start()` que lo único que hace es generar un evento `LeaveStore` que remueve al cliente de la tienda si en el momento de su procesamiento el cliente sigue en la cola. De forma precisa se hace lo siguiente al procesar este evento:
    - El evento `LeaveStore` debe tener internamente el identificador *Único* del cliente (un GUID por ejemplo), digamos que se guarda en la variable `id`.
    - Luego se busca en la cola de la tienda por este cliente. Si el cliente se encuentra en la cola entonces se remueve y se le reporta a la tienda que se perdió un cliente (esto debe estar en los registros de la tienda, es simplemente anotar el tiempo en el que se fue el cliente de la tienda). Si el cliente no se encuentra en la cola esto quiere decir que se está atendiendo o que ya se fue de la tienda porque ya fue atendido, es decir, no es necesario hacer nada en este caso.
  - Se crea el evento `ProcessClient` que su semántica es simplemente decirle a la tienda que tiene que atender al próximo cliente. La forma precisa en que se realizará esto es la siguiente:
    - Se verifica si se está atendiendo algún cliente (las tiendas deben tener una forma de resolver esto, que en lo básico puede ser un booleano) en caso positivo simplemente no se hace nada. Pero en caso negativo, es decir, no se está atendiendo un cliente, entonces se saca de la cola de la tienda el próximo cliente y se le dice que decida que va a hacer.
    - Para el cliente decidir que hacer debe recibir información relacionada con los productos disponibles en la tienda y la cantidad que hay de estos productos. Luego, el cliente debe crear un evento `BuyItem` que su semántica es decirle a la tienda los productos que quiere comprar y cuantas unidades quería comprar de cada uno (porque puede ser que la tienda no tenga la cantidad suficiente para satisfacer su demanda). La lógica que se ejecuta al procesar este evento es la siguiente:
      - Se analiza cuantas unidades hay de cada producto.
      - Se trata de dar al cliente la cantidad de productos que pidieron (siempre es menor o igual, nunca es mayor, es decir, nunca se dan más unidades que las que piden).
      - El cliente analiza la calidad de cada producto recibido y genera un nuevo evento `GiveScore` que se debe ejecutar en el tiempo de la simulación en la que se espera que el cliente haya probado todos los productos (puede ser días después de la compra). Este evento se procesa de la siguiente forma:
        - El cliente calcula la calidad promedio que haya percibido de los alimentos y en dependencia de esto agrega a la tienda una nueva reseña, es decir, un valor entre 1 y 5 (las estrellas). Esto es útil para las estadísticas del final de la tienda (ver con que reseñas se quedaron, que no es más que el promedio de las reseñas).
      - El cliente se retira de la tienda y la tienda genera un nuevo evento que debe ocurrir inmediatamente, es decir, en el tiempo actual de la simulación, este evento es el de `ProcessClient`.
  - Se genera un evento `ReviewStock` que su semántica es decirle al agente de la tienda que debe revisar el stock y analizar si debe pedir a la empresa matriz más suministro. De forma precisa:
    - Se le dice al agente que revise el stock de la tienda (esto es un objetivo de los desires, planteando que se quiere tener el stock en un nivel optimo, donde optimo es algo que depende del agente... que puede ser que tener más de 34 unidades de cada producto).
    - Si el agente cree que es hora de pedir más suministros, entonces crea un evento `SupplyToShop` que su semántica al ejecutarse es decirle a la empresa matriz correspondiente que debe suministrarle cierta cantidad de unidades de un producto (se debe definir dentro del evento la tienda a la que se debe suministrar, así como la cantidad que está pidiendo del producto). De forma precisa:
      - La empresa matriz recibe la petición de la tienda y comienza a analizar cual es la serie de acciones que debe realizar para suplirle a la tienda sus necesidades.

### Descripción de la lógica de cada empresa

#### Empresa matriz

Su lógica es la siguiente:
- A la hora de la empresa matriz cumplir con el objetivo de suministrar cierta cantidad de unidades de un producto a una tienda ella tiene un conjunto de posibles acciones a realizar y con estas acciones debe crear una planificación, es decir, decidir la secuencia de pasos a realizar para cumplir el objetivo:
  <!-- TODO: Volver a analizar esto y analizar lo de la estimación de tiempo de envío y producción-->
  - **Preguntar** a los agentes transportistas cuanto cobran por el envío de cierta cantidades de un producto desde un punto de origen a un punto de destino.
  - **Preguntar** por los almacenes que tienen ese producto, la cantidad de unidades que de ese producto y la calidad promedio.
  - **Preguntar** por los manufactores que tienen a la venta ese producto, cuantos tienen a la venta y a cuanto venden la unidad.
  - **Preguntar** por los manufactores que pueden crear el producto, cuanto cobran por la creación de cierta cantidad de unidades del producto.
  - **Preguntar** por los proveedores que venden cierto producto, cuantas unidades venden y a que precio la unidad.
  - **Comprar** tantas unidad del producto al manufactor y enviarlas a cierto punto con un transportista especifico (Esta compra es para los productos que vende el manufactor).
  - **Comprarle** tantas unidades del producto al productor y enviarlas por medio de un agente transportista a un punto del mapa.
  - **Enviar** cierta cantidad de unidades del almacén a un punto del mapa por medio de un transportista.
  - **Mandar** al manufactor a crear cierta cantidad de productos y enviarla a cierto punto del mapa con un transportista. <!-- Analizar este punto pues es necesario que se hayan enviado los productos base al manufactor -->

#### Empresa proveedora

Las acciones de esta empresa son las siguientes:
1. Dar información a una empresa sobre un producto, esto es, mostrar de un producto la cantidad de unidades que tiene a la venta y el precio por unidad.
2. Realizar venta, esto es, definir la cantidad de unidades a vender de un producto especifico y enviarlo a cierto punto del mapa por un distribuidor.

#### Empresa transportista

Las acciones de esta empresa son las siguientes:
1. Decir cuanto cobra por enviar cierta cantidad de unidades de un producto de un punto de origen del mapa a un punto de destino.
2. Realizar el envío de cierta cantidad de unidades de un punto del mapa a otro. A la hora de realizar esta acción se le tiene que descontar un dinero a la empresa matriz.

#### Empresa manufacturera
<!-- TODO: Revisar esto completo -->
Las acciones de esta empresa
1. Dar información a una empresa sobre un producto, esto es, mostrar de un producto la cantidad de unidades que tiene a la venta y el precio por unidad.
2. Dar información sobre los productos que puede crear
3. Realizar venta, esto es, definir la cantidad de unidades a vender de un producto especifico y enviarlo a cierto punto del mapa por un distribuidor.
4. Producir cierta cantidad de unidades de un producto a una empresa, esto es, se descuenta a la empresa el costo de la producción de estas unidades, luego se envían los productos creados a un punto en el mapa (proporcionado por la empresa matriz) por medio de un distribuidor.

#### Empresa Almacén

Las acciones de 
