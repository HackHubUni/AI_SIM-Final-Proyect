

# Ideas para Proyecto IA_Sim

### Definir Problematica a simular:
## Agente Empresas
+ Dado un numero $N$ de empresas las cuales comercializan un mismo producto final, se busca simular el comportamiento de estas empresas en base al dinamismo del mercado, la competencia y la demanda del producto.

- Primero habrá dinamismo en la cadena de suministro, para elaborar u re-vender un producto X puede adquirirse ese producto X de A provedores s un precio Ai y una cantidad máxima y mínima de pedido, este se le suma el precio intrinseco de hacer X producto final, o existe Xi formas de elaborar dicho producto ejemplo: si el producto a vender es una pizza, existen dos vertientes fundamentales:
<div align="center">

 ```mermaid
graph TD;
    A[Proveer]-->B[Comprar prelaborado];
    A-->C[Elaborar_desde_cero];
    C-->D[Comprar los productos necesarios];
    D-->E[Harina, pure de  tomate, queso, etc];
    D-->F[Elaborar alguna parte del producto como el puré de tomate]; 
    F-->G[Comprar Tomate Fresco];
    F-->H[Comprar Maquina para hacer puré de tomate];
```	
</div>

donde por medio de conocimiento intrinseco del propio agente este debe de hacer inferencias para poder resolver en ciertos momentos donde la oferta es menor que la demanda u un evento de ruptura de la cadena de suministro afecte a la cantidad de demanda que se puede satisfacer.

## Proveedores 

- Los proveedores son agentes que tienen en su base de conocomiento como generar variables aleatorias para en un determinado momento futuro $x<X Grande$ puede estimar cuanta mercancía tiene para poder vender. 
- Tiene la protestad de negociar acuerdos con las empresas para poder venderles a un precio menor o mayor, dependiendo de la cantidad de mercancia que se le compre.
- Puede ser que dada una nueva renegociacion con otra empresa el proveedor decida no cumplir su acuerdo con la anterior empresa dado que encontro un mejor trato con otra empresa.


## Medio Ambiente:
- Formado principalmente por el cjto de eventos aleatorios como la falla del suministro de un proveedor a una empresa durante un tiempo conocido o no.
- La cantidad de personas interesadas en un producto X de una empresa Y en un tiempo t
- La distribucion de los clientes de una empresa Y en un tiempo t
-  