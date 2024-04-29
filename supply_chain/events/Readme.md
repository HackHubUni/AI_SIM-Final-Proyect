# Events

> Esta carpeta contiene la implementación de todos los eventos de la simulación

En este documento se explicará cada evento implementado pero antes se dará una breve explicación de como funciona nuestra simulación con estos eventos

## Breve información sobre los eventos de algunas entidades de la simulación

Es sabido que nuestra simulación contiene 2 entidades fundamentales, las empresas y los agentes.
Las empresas son parte del entorno y tienen una serie de funcionalidades y comportamientos fijos (como reabastecerse cada cierto tiempo, pagar costos, etc.).
Los agentes por su parte, se dividen en los agentes que controlan las empresas y en los agentes que realizan la función de consumidores en las tiendas. Los agentes que controlan las empresas deben crear planes de acciones a ejecutar en sus empresas (como mandar a los almacenes a enviar cierta cantidad de productos hacia una tienda o conjunto de tiendas, planificar como enviar productos de los proveedores a los manufactores y de estos a los almacenes o tiendas, etc.) mientras que los consumidores al entrar a una tienda y ser agregados a la cola deben decidir cuanto tiempo están dispuestos a esperar para cuando ese tiempo pase irse si no los han atendido (un evento que al procesarse quita al consumidor de la cola y le dice a la tienda que perdió un cliente) pero también deben decidir que producto quieren consumir cuando los comienzan a atender y al ser atendidos deben dar una reseña a la empresa con respecto a que tanto le gustó la atención y la confección del producto.

## Funcionamiento de la simulación

Nuestra simulación de los picos de demandas de las cadenas de suministros está basada en eventos discretos, es decir, nosotros no modelamos el avance del tiempo de forma continua (segundo a segundo) sino que lo hacemos en intervalos de tiempos variables que están determinados por la ocurrencia de eventos.
Cada paso de nuestra simulación está determinado por la ejecución de un evento.

Nosotros podemos describir el flujo de ejecución de nuestra simulación dividiéndola en 2 partes:
- Inicialización
- Procesamiento de la cola de eventos

### Inicialización

Al comienzo de la simulación no hay ningún evento que procesar y es por esto que se hace necesario rellenar la simulación con unos eventos iniciales. Para esto se pasa por cada empresa del entorno y se llama a un método `Start()` que cada empresa debe implementar. Este método lo que hace es agregar a la simulación eventos iniciales de la empresa (como crear el evento que dice en que momento al proveedor se le rellena el stock) y llamar al método `Start()` que contiene cada agente, que nuevamente lo que hace es crear los eventos iniciales que el agente considera necesarios para realizar su correcta planificación.

> Nota: En el método `Start()` de las tiendas debe estar el funcionamiento para generar el evento del arribo del primer cliente y al procesarse este evento es que se crea un el evento del nuevo arribo de un cliente.

### Procesamiento de la cola de eventos

Los eventos que se deben ejecutar en nuestra simulación son almacenados en una cola de prioridad que procesa primero el evento con menor tiempo almacenado en esta y si 2 eventos tienen el mismo tiempo de procesamiento entonces se usa la propiedad llamada `priority` que se encuentra en cada evento para poder desambiguar entre que evento ejecutar primero.
La lógica que se debe realizar al procesar un evento está contenida en el método `execute(environment)` que cada evento debe sobrescribir. Esté método recibe la instancia del entorno en el que todas las entidades están contenidas y el tiempo en el que se encuentra la simulación actualmente. Es por esto que se puede ejecutar casi cualquier lógica dentro de estos eventos y se desacopla está implementación del entorno.

### Terminación de la simulación

Nuestra simulación al inicializarse tiene definido el tiempo en el que debe parar. De donde al pedirle a la simulación añadir un evento que deba ocurrir luego del tiempo de terminación implica descartar el evento pues nunca será procesado.

## Descripción de cada evento implementado

<!-- TODO: Aquí se debe escribir la lógica general de cada evento -->

