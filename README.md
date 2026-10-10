# Optimización de Rutas Turísticas en Coclé, Panamá

**Aplicación del algoritmo de Dijkstra para el cálculo de rutas turísticas de menor distancia**

<p align="center">
  <strong>Universidad de Panamá</strong><br>
  Facultad de Informática<br>
  Proyecto académico de optimización de rutas turísticas
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Algoritmo-Dijkstra-green" alt="Dijkstra">
  <img src="https://img.shields.io/badge/Nodos-29-orange" alt="29 nodos">
  <img src="https://img.shields.io/badge/Aristas-53-purple" alt="53 aristas">
</p>

## 📌 Descripción

Este proyecto desarrolla un programa en Python para el cálculo y la optimización de rutas turísticas en la provincia de Coclé, Panamá. Utiliza un grafo ponderado que representa 29 lugares turísticos y urbanos conectados mediante 53 aristas.

La aplicación implementa el algoritmo de Dijkstra para calcular caminos mínimos entre los nodos de la red. A partir de estas distancias mínimas, emplea una búsqueda exhaustiva de permutaciones para determinar el orden de visita de los destinos de cada itinerario, considerando la salida y el regreso a Penonomé.

El sistema organiza los recorridos en siete días y ofrece herramientas para consultar rutas, visualizar grafos, exportar resultados y realizar pruebas computacionales.

**Criterio oficial de optimización: distancia recorrida.** El tiempo estimado y el costo se incluyen como métricas complementarias.

## 🎯 Objetivos

* Modelar una red de atractivos turísticos mediante la teoría de grafos.
* Implementar Dijkstra para calcular caminos mínimos entre los lugares.
* Determinar el orden de visita de los destinos de cada itinerario mediante búsqueda exhaustiva.
* Organizar recorridos turísticos de siete días por zonas de la provincia.
* Verificar la consistencia de los resultados mediante pruebas computacionales.
* Facilitar la consulta, visualización y exportación de los datos obtenidos.

## 🗺️ Características principales

* **Red turística:** 29 nodos y 53 aristas.
* **Siete itinerarios:** recorridos organizados manualmente por zonas geográficas.
* **Cálculo de caminos mínimos:** implementación propia de Dijkstra con una cola de prioridad (`heapq`).
* **Orden de visita:** búsqueda exhaustiva mediante permutaciones, relacionada con el problema del viajante (TSP).
* **Tres métricas:** distancia, tiempo y costo.
* **Visualización:** grafos completos e itinerarios diarios mediante Matplotlib.
* **Exportación:** generación de un archivo Excel con las rutas, las aristas y la matriz de distancias mínimas.
* **Validaciones:** pruebas de integridad, verificación del algoritmo, consistencia interna y análisis de sensibilidad.
* **Validación externa:** generación de una plantilla CSV para comparar los datos del modelo con mediciones independientes.

## 🧮 Fundamento matemático

La red se representa mediante un grafo ponderado:

$$
G=(V,E)
$$

Donde:

* \(V\) representa el conjunto de nodos o lugares turísticos.
* \(E\) representa las aristas o conexiones entre los nodos.
* Los pesos de las aristas contienen los valores de distancia, tiempo y costo.

El algoritmo de Dijkstra determina el camino mínimo entre dos nodos para un criterio seleccionado, siempre que los pesos sean no negativos.

Para cada itinerario, el programa evalúa las permutaciones de los destinos y suma las distancias mínimas entre cada par consecutivo, incluyendo el regreso a Penonomé. De esta manera, **Dijkstra calcula los caminos mínimos entre pares de lugares, mientras que las permutaciones determinan el orden de visita del itinerario**.

La agrupación de los destinos por día se encuentra definida previamente en el código.

## 📏 Criterios de cálculo

| Criterio  | Descripción                                                           |
| --------- | --------------------------------------------------------------------- |
| Distancia | Kilómetros recorridos; criterio oficial del proyecto.                 |
| Tiempo    | Tiempo estimado de desplazamiento, expresado en minutos.              |
| Costo     | Estimación calculada a partir de la distancia y una tarifa constante. |

El programa define `COSTO_POR_KM = 0.15` USD/km. Este valor es un supuesto de cálculo que debe justificarse documentalmente en la investigación.

**Nota sobre los datos:** las distancias y los tiempos registrados en las aristas están identificados en el código como estimaciones basadas en Google Maps. Deben contrastarse con una fuente independiente antes de presentarse como mediciones verificadas.

## 🛠️ Tecnologías y dependencias

* **Python:** implementación del programa.
* **NetworkX:** construcción y análisis del grafo, además de la verificación independiente del algoritmo.
* **Matplotlib:** generación de gráficos y visualizaciones.
* **OpenPyXL:** creación y formato de archivos Excel.
* **Heapq:** cola de prioridad utilizada por la implementación propia de Dijkstra.
* **CSV:** generación y evaluación de plantillas de validación.
* **Itertools:** generación de permutaciones para el orden de visita.

El código intenta comprobar e instalar automáticamente las dependencias `networkx`, `matplotlib` y `openpyxl` cuando se inicia.

## 💻 Requisitos

* Python 3.
* Conexión a Internet si es necesario instalar las dependencias.
* Una terminal o consola para ejecutar el programa.
* Un entorno compatible con Matplotlib para visualizar los grafos. Si no hay pantalla gráfica disponible, el código puede guardar las imágenes como archivos PNG.

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/jc5536201-droid/optimizacion-rutas-turisticas-cocle.git
```

### 2. Entrar en la carpeta del proyecto

```bash
cd optimizacion-rutas-turisticas-cocle
```

### 3. Ejecutar el programa

Guarda el código en el archivo `rutas_cocle_dijkstra.py` y ejecuta:

```bash
python rutas_cocle_dijkstra.py
```

El programa inicializa el grafo, calcula las matrices de caminos mínimos y presenta el menú interactivo.

### 4. Ejecutar las pruebas sin utilizar el menú

```bash
python rutas_cocle_dijkstra.py --pruebas
```

Este modo ejecuta las principales pruebas y análisis, muestra resultados y genera archivos de salida.

> Los comandos anteriores presuponen que el archivo se encuentra en la raíz del repositorio y que su nombre es `rutas_cocle_dijkstra.py`.

## 📋 Opciones del menú

| Opción | Funcionalidad                                  |
| ------ | ---------------------------------------------- |
| 1      | Consultar el inventario de los 29 atractivos.  |
| 2      | Visualizar el grafo completo.                  |
| 3      | Consultar la ruta óptima de un día específico. |
| 4      | Mostrar los itinerarios de los siete días.     |
| 5      | Calcular el camino mínimo entre dos nodos.     |
| 6      | Exportar los resultados a Excel.               |
| 7      | Guardar los grafos como imágenes PNG.          |
| 8      | Acceder a las validaciones del modelo.         |
| 9      | Ejecutar pruebas computacionales.              |
| 0      | Salir del programa.                            |

## 🧪 Validaciones y pruebas computacionales

El código incorpora herramientas para examinar tanto el modelo de datos como los resultados de los algoritmos.

### Validaciones del modelo

* **Validación externa:** crea una plantilla CSV para registrar valores de referencia independientes, su fuente y su fecha, y calcular los errores de las mediciones.
* **Consistencia interna:** verifica la propiedad de subestructura óptima de los caminos mínimos.
* **Análisis de sensibilidad:** compara caminos obtenidos por distancia y tiempo, y estudia la estabilidad de los itinerarios ante perturbaciones simuladas del ±10 % y ±20 % en las distancias.

### Pruebas computacionales

* **Integridad de datos:** examina nodos, aristas, conectividad y posibles inconsistencias.
* **Caja negra:** compara resultados de casos de prueba con los valores esperados.
* **Verificación independiente:** compara las matrices calculadas con NetworkX y Floyd–Warshall.
* **Tiempo de ejecución:** mide el rendimiento de Dijkstra en grafos de distintos tamaños y el tiempo empleado en calcular los itinerarios.

Estas funciones permiten comprobar propiedades matemáticas, detectar problemas en los datos y evaluar el comportamiento computacional. La validación externa solo estará respaldada por mediciones independientes cuando se complete la plantilla con datos documentados.

## 📊 Archivos de salida

Dependiendo de las opciones ejecutadas, el programa puede generar los siguientes archivos:

| Archivo o carpeta                   | Contenido                                                                    |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| `Rutas_Cocle.xlsx`                  | Itinerarios de siete días, aristas del grafo y matriz de distancias mínimas. |
| `grafos_cocle/`                     | Grafos del sistema y de los siete días, guardados como imágenes PNG.         |
| `validacion_externa_plantilla.csv`  | Plantilla para introducir datos de referencia independientes.                |
| `validacion_externa_resultados.csv` | Resultados de la evaluación externa, cuando existen filas válidas.           |
| `caja_negra_resultados.csv`         | Resultados de los casos de prueba de caja negra.                             |

Los archivos se crean al ejecutar las funciones correspondientes; no todos aparecen necesariamente al iniciar el programa.

## ⚠️ Limitaciones

* Las distancias y los tiempos incluidos en el modelo están definidos como estimaciones y requieren validación independiente.
* La agrupación de lugares por día es manual; no la determina automáticamente el algoritmo.
* El orden óptimo se calcula mediante búsqueda exhaustiva de permutaciones, por lo que el número de destinos influye considerablemente en el tiempo de ejecución.
* Las posiciones utilizadas para dibujar los grafos son esquemáticas y no representan coordenadas geográficas ni distancias a escala.
* El costo depende de una tarifa constante por kilómetro y no constituye por sí solo una estimación completa del gasto real de un viaje.
* Los resultados representan el modelo implementado y dependen de la calidad y precisión de sus datos de entrada.

## 🎓 Contexto académico

Este código forma parte de un proyecto académico sobre la aplicación de la teoría de grafos y los algoritmos de caminos mínimos a la planificación de rutas turísticas en la provincia de Coclé, Panamá.

Su finalidad es documentar el procedimiento computacional, facilitar la revisión de los resultados y servir como referencia para estudiantes, investigadores y desarrolladores interesados en la matemática aplicada y la optimización de rutas.

## 🤝 Uso, colaboración y reproducibilidad

El repositorio es público y permite consultar el código fuente. Las personas interesadas pueden estudiar su implementación, reproducir las pruebas con los datos disponibles y proponer mejoras.

Si deseas reutilizar, modificar o redistribuir el código, revisa la licencia incorporada al repositorio. La visibilidad pública, por sí sola, no concede automáticamente todos esos permisos.

## 📂 Repositorio

**Código fuente:**
https://github.com/jc5536201-droid/optimizacion-rutas-turisticas-cocle

---

*Optimización de rutas turísticas en la provincia de Coclé, Panamá. Aplicación de Dijkstra, teoría de grafos y pruebas computacionales.*

