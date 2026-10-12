# Optimización de Rutas Turísticas en Coclé, Panamá

**Aplicación del algoritmo de Dijkstra para el cálculo de rutas turísticas de menor distancia**

<p align="center">
  <strong>Universidad de Panamá</strong><br>
  Facultad de Ciencias Naturales y Exactas<br>
  Licenciatura en Matemáticas<br>
  Proyecto académico de optimización de rutas turísticas
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Algoritmo-Dijkstra-green" alt="Dijkstra">
  <img src="https://img.shields.io/badge/Nodos-29-orange" alt="29 nodos">
  <img src="https://img.shields.io/badge/Aristas-57-purple" alt="57 aristas">
</p>

## 📌 Descripción

Este proyecto desarrolla un programa en Python para el cálculo y la optimización de rutas turísticas en la provincia de Coclé, Panamá. Utiliza un grafo ponderado que representa **29 lugares turísticos y urbanos** conectados mediante **57 aristas**.

La aplicación implementa el algoritmo de Dijkstra para calcular caminos mínimos entre los nodos de la red. A partir de estas distancias mínimas, emplea una búsqueda exhaustiva de permutaciones para determinar el orden de visita de los destinos de cada itinerario, considerando la salida y el regreso a **Penonomé** (nodo 15), que actúa como hub central.

El sistema organiza los recorridos en **siete días** y ofrece herramientas para consultar rutas, visualizar grafos, exportar resultados y realizar pruebas computacionales.

**Criterio oficial de optimización: distancia recorrida.** El tiempo estimado y el costo se incluyen como métricas complementarias.

## 🎯 Objetivos

* Modelar una red de atractivos turísticos mediante la teoría de grafos.
* Implementar Dijkstra para calcular caminos mínimos entre los lugares.
* Determinar el orden de visita de los destinos de cada itinerario mediante búsqueda exhaustiva.
* Organizar recorridos turísticos de siete días por zonas de la provincia.
* Verificar la consistencia de los resultados mediante pruebas computacionales.
* Facilitar la consulta, visualización y exportación de los datos obtenidos.

## 🗺️ Características principales

* **Red turística:** 29 nodos y 57 aristas.
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
G = (V, E)
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

* Python 3.9 o superior.
* Conexión a Internet si es necesario instalar las dependencias.
* Una terminal o consola para ejecutar el programa.
* Un entorno compatible con Matplotlib para visualizar los grafos. Si no hay pantalla gráfica disponible, el código puede guardar las imágenes como archivos PNG.

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/jc5536201-droid/optimizacion-rutas-turisticas-cocle.git
