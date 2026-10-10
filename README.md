# Optimización de Rutas Turísticas en la Provincia de Coclé, Panamá

**Aplicación del algoritmo de Dijkstra para la optimización de rutas turísticas**

Universidad de Panamá – Facultad de Informática

**Características principales:** 29 nodos · 53 aristas · 7 días de itinerarios · Menú interactivo

**Criterio oficial de optimización: DISTANCIA (km)**

## Descripción del proyecto

Este proyecto desarrolla un programa en Python para calcular caminos mínimos y optimizar el orden de visita de atractivos turísticos de la provincia de Coclé, Panamá. Se utiliza una representación mediante grafos ponderados y el algoritmo de Dijkstra para determinar las rutas de menor distancia entre los lugares registrados.

El sistema contempla 29 nodos turísticos y urbanos conectados mediante 53 aristas. A partir de esta estructura, permite calcular caminos mínimos, generar itinerarios de siete días con salida y regreso a Penonomé, visualizar grafos y exportar resultados a Excel.

El proyecto forma parte de un trabajo de graduación de la Licenciatura en Matemática de la Universidad de Panamá.

## Objetivo

Aplicar el algoritmo de Dijkstra para determinar caminos mínimos entre atractivos turísticos de Coclé y utilizar esas distancias para organizar itinerarios turísticos de manera eficiente.

El criterio principal del estudio es la **distancia mínima recorrida**, de acuerdo con las indicaciones del asesor del proyecto.

## Características del programa

* **Grafo turístico:** representa 29 nodos y 53 aristas.
* **Algoritmo de Dijkstra:** implementación propia que utiliza una cola de prioridad (`heapq`) para calcular caminos mínimos.
* **Matrices de caminos mínimos:** calcula las distancias mínimas entre todos los pares de nodos.
* **Optimización de itinerarios:** utiliza búsqueda exhaustiva mediante permutaciones para determinar el orden de visita de cada día.
* **Siete itinerarios turísticos:** organiza los atractivos por zonas geográficas.
* **Visualización gráfica:** genera diagramas del grafo completo y de las rutas diarias.
* **Exportación a Excel:** produce tablas con itinerarios, aristas y matriz de distancias mínimas.
* **Validaciones y pruebas:** incluye verificaciones del algoritmo, integridad de los datos, sensibilidad y tiempos de ejecución.
* **Validación externa:** permite comparar los datos del modelo con mediciones independientes de fuentes de rutas.

## Fundamentos del algoritmo

### 1. Representación mediante grafos

Los atractivos turísticos se representan como nodos y las conexiones entre ellos como aristas. Cada arista almacena tres atributos:

* **Distancia:** longitud estimada del trayecto en kilómetros.
* **Tiempo:** duración estimada del trayecto en minutos.
* **Costo:** estimación monetaria calculada a partir de la distancia.

El grafo se construye con NetworkX y se utiliza como estructura para ejecutar los cálculos.

### 2. Algoritmo de Dijkstra

Se implementa una versión propia del algoritmo de Dijkstra que emplea una cola de prioridad mediante `heapq`.

El algoritmo calcula el camino mínimo entre un nodo de origen y los demás nodos alcanzables. Al repetir el procedimiento para cada nodo de origen, se obtienen las matrices de caminos mínimos para los criterios disponibles.

### 3. Optimización del orden de visita

Dijkstra determina el camino mínimo entre dos nodos, pero **no determina por sí solo el orden óptimo para visitar varios lugares**.

Por ello, el programa utiliza una búsqueda exhaustiva mediante permutaciones, relacionada con el problema del viajante (*Traveling Salesperson Problem*, TSP). Se evalúan los posibles órdenes de visita y se selecciona el de menor distancia acumulada, con salida y regreso a Penonomé.

La agrupación de los atractivos por día se define previamente en `DIAS_CONFIG`, de acuerdo con las zonas turísticas establecidas en el proyecto.

### 4. Criterio de optimización

El criterio oficial es la distancia mínima, expresada en kilómetros. El programa también conserva el tiempo y el costo como métricas complementarias.

El costo se calcula mediante la expresión:

`costo = distancia × COSTO_POR_KM`

En la configuración actual, `COSTO_POR_KM = 0.15` USD/km. Este valor constituye una tarifa estimada del modelo y debe justificarse en la documentación académica mediante una fuente, fecha y supuestos de cálculo.

Como el costo es proporcional a la distancia mediante una constante positiva, minimizar el costo produce el mismo camino mínimo que minimizar la distancia, siempre que ambos criterios utilicen las mismas conexiones.

## Itinerarios turísticos

El programa incluye siete itinerarios organizados por zonas:

| Día | Zona temática                 |
| --- | ----------------------------- |
| 1   | Playas de Antón               |
| 2   | Penonomé Histórico            |
| 3   | La Pintada: Montaña y Cultura |
| 4   | Ruta Arqueológica de Natá     |
| 5   | Naturaleza de Antón           |
| 6   | Tesoros de Aguadulce          |
| 7   | Circuito Integrador           |

La agrupación de lugares es manual y está definida en `DIAS_CONFIG`. El algoritmo calcula el orden de visita de los destinos incluidos en cada grupo; no selecciona automáticamente los atractivos que integran cada día.

Los recorridos se plantean con salida y regreso a Penonomé. Las distancias, tiempos y costos obtenidos dependen de los datos registrados en el grafo.

## Requisitos

* Python 3.10 o superior recomendado.
* Conexión a Internet durante la instalación de dependencias, si no están disponibles.
* Terminal o consola compatible con Python.
* Un entorno gráfico compatible para visualizar las figuras interactivamente. En entornos sin pantalla gráfica, el programa puede guardar las imágenes como archivos PNG.

### Dependencias

El programa utiliza las siguientes bibliotecas:

| Biblioteca | Función                                                       |
| ---------- | ------------------------------------------------------------- |
| NetworkX   | Construcción y comprobación del grafo.                        |
| Matplotlib | Generación de diagramas y visualizaciones.                    |
| OpenPyXL   | Exportación de resultados a Excel.                            |
| Heapq      | Cola de prioridad utilizada por Dijkstra; pertenece a Python. |

También utiliza módulos de la biblioteca estándar, como `csv`, `itertools`, `random`, `statistics`, `time` y `math`.

El código intenta detectar e instalar automáticamente las dependencias externas que falten. También puedes instalarlas manualmente.

## Instalación y ejecución

### 1. Clonar el repositorio

Abre una terminal y ejecuta:

```bash
git clone https://github.com/jc5536201-droid/optimizacion-rutas-turisticas-cocle.git
```

### 2. Entrar en la carpeta del proyecto

```bash
cd optimizacion-rutas-turisticas-cocle
```

### 3. Instalar las dependencias

```bash
python -m pip install networkx matplotlib openpyxl
```

Si utilizas Windows y el comando `python` no funciona, prueba:

```bash
py -m pip install networkx matplotlib openpyxl
```

### 4. Ejecutar el programa

Comprueba que el archivo `rutas_cocle_dijkstra.py` esté en la carpeta del proyecto y ejecuta:

```bash
python rutas_cocle_dijkstra.py
```

En Windows también puedes utilizar:

```bash
py rutas_cocle_dijkstra.py
```

El programa inicializa el grafo, calcula las matrices de caminos mínimos y presenta el menú interactivo.

## Menú interactivo

Las opciones disponibles son:

| Opción | Función                                       |
| ------ | --------------------------------------------- |
| 1      | Consultar el inventario de los 29 atractivos. |
| 2      | Visualizar el grafo completo.                 |
| 3      | Calcular la ruta óptima de un día.            |
| 4      | Consultar los siete itinerarios.              |
| 5      | Calcular el camino mínimo entre dos nodos.    |
| 6      | Exportar los resultados a Excel.              |
| 7      | Guardar los grafos como imágenes PNG.         |
| 8      | Ejecutar las validaciones del modelo.         |
| 9      | Ejecutar las pruebas computacionales.         |
| 0      | Salir del programa.                           |

## Pruebas y validaciones

El programa incorpora procedimientos de comprobación destinados a evaluar la implementación y los datos utilizados.

### Validaciones del modelo

**Validación externa:** genera una plantilla CSV para comparar las distancias y los tiempos registrados con valores obtenidos de una fuente independiente. Los campos de referencia deben completarse antes de evaluar los errores.

**Consistencia interna:** comprueba la propiedad de subestructura óptima de los caminos mínimos.

**Análisis de sensibilidad:** compara los caminos calculados por distancia y tiempo, y utiliza simulaciones de Monte Carlo con perturbaciones de ±10 % y ±20 % en las distancias.

### Pruebas computacionales

* **Integridad de datos:** revisa nodos, aristas, identificadores, conectividad y posibles inconsistencias.
* **Caja negra:** compara resultados esperados y obtenidos para una colección de casos de prueba.
* **Verificación independiente:** contrasta los resultados con funciones de NetworkX y con Floyd-Warshall.
* **Tiempo de ejecución:** mide el tiempo necesario para calcular caminos mínimos en grafos de distintos tamaños.
* **Optimización de itinerarios:** mide el tiempo empleado para encontrar el orden de visita de cada día.

### Ejecutar las pruebas sin el menú

Para ejecutar el conjunto de pruebas y generar las tablas de resultados, utiliza:

```bash
python rutas_cocle_dijkstra.py --pruebas
```

Este modo también intenta exportar los resultados a Excel y generar una plantilla para la validación externa.

**Importante:** ejecutar las pruebas no equivale a superar todas las validaciones. Deben revisarse los resultados producidos, completar las mediciones de referencia y documentar los errores o advertencias encontrados.

## Archivos generados

Según las opciones ejecutadas, el programa puede generar los siguientes archivos:

| Archivo                             | Contenido                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------- |
| `Rutas_Cocle.xlsx`                  | Itinerarios, aristas y matriz de distancias mínimas.                          |
| `validacion_externa_plantilla.csv`  | Plantilla para registrar las mediciones de referencia.                        |
| `validacion_externa_resultados.csv` | Resultados de la comparación externa, cuando hay datos suficientes.           |
| `caja_negra_resultados.csv`         | Resultados de los casos de prueba de caja negra.                              |
| `grafo_completo_distancia.png`      | Diagrama del grafo completo, según la opción ejecutada.                       |
| `grafos_cocle/`                     | Carpeta con las visualizaciones guardadas mediante la opción correspondiente. |

Los nombres de los archivos pueden variar según las opciones seleccionadas y el criterio utilizado.

## Alcance y limitaciones

1. **Datos estimados:** las distancias y los tiempos introducidos en las aristas son estimaciones del modelo y deben contrastarse con fuentes independientes.
2. **Agrupación manual:** los lugares asignados a cada día no son seleccionados automáticamente por Dijkstra.
3. **Optimización exhaustiva:** el orden de visita se obtiene mediante permutaciones. Este enfoque es viable para grupos pequeños, pero su costo computacional crece factorialmente con el número de destinos.
4. **Visualizaciones esquemáticas:** las posiciones empleadas para dibujar el grafo son ilustrativas y no representan coordenadas geográficas ni distancias a escala.
5. **Costo estimado:** el valor monetario depende de la tarifa configurada y no debe interpretarse como un costo real medido sin una justificación documentada.
6. **Validación externa pendiente:** los resultados solo podrán considerarse validados frente a una fuente independiente cuando se registren las mediciones de referencia y se analicen las diferencias.

El programa calcula rutas a partir de la estructura y los pesos proporcionados. Por tanto, la calidad de los resultados depende tanto de la correcta implementación del algoritmo como de la precisión y consistencia de los datos de entrada.

## Reproducibilidad y código fuente

El código fuente se encuentra disponible públicamente en GitHub para facilitar su consulta, revisión y reproducción por parte de otros investigadores.

**Repositorio:**
https://github.com/jc5536201-droid/optimizacion-rutas-turisticas-cocle

Para reproducir los resultados, se recomienda utilizar la versión del código y los datos correspondientes, registrar el entorno de ejecución y conservar los archivos generados durante las pruebas.

## Autoría y contexto académico

Proyecto de optimización de rutas turísticas en la provincia de Coclé, Panamá, mediante teoría de grafos y el algoritmo de Dijkstra.

**Institución:** Universidad de Panamá
**Facultad:** Facultad de Informática
**Programa:** Licenciatura en Matemática
**Trabajo:** Proyecto de graduación presentado como opción de tesis.

## Licencia

No se especifica una licencia de distribución en este README. Si deseas permitir formalmente que otras personas reutilicen, modifiquen o distribuyan el código, agrega una licencia al repositorio, por ejemplo, MIT, después de decidir las condiciones de uso.

---

*Documento de presentación del proyecto. Los resultados numéricos, las fuentes de datos y el cumplimiento de las validaciones deben verificarse mediante la ejecución del programa y la documentación de las mediciones correspondientes.*

