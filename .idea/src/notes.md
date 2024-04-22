
# A modelar:

- [ ] Producto base:
   - [ ] comportamiento interno:
     - [x] calidad: función que dictamina la calidad del producto en un momento $ t_i $ depende de los eventos:
        - [ ] tiempo que ha transcurrido 
        - [ ] temperatura en el tiempo transcurrido
   - [ ] Propiedades:
     - Temperatura ideal 
     - Humedad ideal
     - Rango de temperatura
     
     
        
- [ ] Producto generico (hereda los atributos de producto base) : 
  - [x] La raíz de productos de la cadena de suministro.
  - [X] Los nodos hijos son los productos necesarios para la confección del mismo 
  - [X] Las aristas la (cantidad de producto, calidad mínima requerida)
   - [ ] Propiedades:
     - Temperatura ideal 
     - Rango de temperatura
- [ ] mapa:
  - Inicialmente como un grafo dirigido. (Sujeto a cambios)
      - [x]  Nodos intercepciones de las calles
      - [x] Aristas las calles (su longitud, límite de velocidad, tipo calle, carga máxima (por los puentes ), altura máxima (por tuneles o puentes que esten delante) )
      - [x] Gasolineras(tipo de combustible a despachar, coste por litro, capacidad en stock de combustible(inicialmente la capacidad en stock es infnito ))
      - [x] Vehículos que van a servir a la logística (carga maxima, volumen maximo (), coeficiente de relacion velocidad carga, velocidad maxima, acelaracion, consumo medio por tramos de combustible, capacidad de combustible, tipo de combustible)
      - [x] 
- [ ] empresas:
  - [ ] proveedores: venden los productos
  - [ ] manufactureras: venden servicios
  - [ ] distribuidores: mover la mercancía
  - [ ] almacenes: guardar la mercancía
  - [ ] tiendas: venta al público
  - [ ] empresa matriz
  - [ ] Caja negra de social review
- [ ] cliente 
