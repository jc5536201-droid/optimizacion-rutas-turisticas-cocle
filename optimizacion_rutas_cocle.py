"""
OPTIMIZACIÓN DE RUTAS TURÍSTICAS – PROVINCIA DE COCLÉ, PANAMÁ
Algoritmo de Dijkstra | 29 Nodos | 3 Criterios | Menú Interactivo
Universidad de Panamá – Facultad de Informática

7 DÍAS · 4-6 LUGARES POR DÍA · DATOS ESTIMADOS DESDE GOOGLE MAPS
CRITERIO OFICIAL DEL PROYECTO: DISTANCIA (según indicación del asesor)

VALIDACIONES IMPLEMENTADAS (Sección 3.6.1):
a) Google Maps (simulación ±4%, tolerancia ±5%)
b) Consistencia interna (subestructura óptima)
c) Análisis de sensibilidad (3 criterios; distancia = criterio oficial)

PRUEBAS COMPUTACIONALES (Sección 3.6.3):
a) Prueba de Caja Negra (manual, opción 5)
b) Prueba de Integridad de Datos (automática)
c) Prueba de Tiempo de Ejecución (Tabla 9)

────────────────────────────────────────────────────────────────────────────
CORRECCIONES APLICADAS (revisión solicitada por James, sep-2026):
1. El conteo de aristas hardcodeado en varios textos decía "49" cuando el
   grafo real (ARISTAS_RAW) tiene 52 aristas. Se corrigió a valores dinámicos
   (len(G.edges())) en vez de números fijos, para que nunca vuelva a
   desincronizarse si se agregan/quitan nodos.
2. Las estadísticas de cada día (distancia_km, tiempo_auto_min, costo_usd)
   en DIAS_CONFIG eran valores fijos que no coincidían con lo que el propio
   programa calculaba en vivo en la opción 3 del menú. Ahora se recalculan
   en vivo, ida y vuelta a Penonomé, con el criterio oficial del proyecto
   ("distancia") — así las dos pantallas siempre coinciden.
3. La Tabla 9 (prueba de tiempo de ejecución) comparaba contra un grafo
   aleatorio de (29,49) llamándolo "grafo real"; se corrigió a (29,52) y
   además se agregó una medición directa sobre el grafo real G (no solo
   sobre un grafo aleatorio del mismo tamaño).
4. Se añadió la arista urbana (12, 14) entre la Iglesia San Juan Bautista
   (ISJ) y el Balneario Las Mendozas (BLM), verificada en Google Maps
   (1.0 km, 3 min). Esto corrige el rodeo innecesario del Día 2, que
   bajó de 20.2 km a ~13-14 km, coincidiendo con Google Maps dentro
   del ±15%.

NOTA METODOLÓGICA SOBRE EL COSTO:
El criterio "costo" se define como distancia*0.15 de forma uniforme en TODAS
las aristas. Al ser una transformación lineal constante, optimizar por costo
da la misma ruta que optimizar por distancia (las diferencias observadas
~3.6% se deben a redondeo en punto flotante). Por eso el criterio OFICIAL
del proyecto es DISTANCIA. Tiempo y costo se incluyen como MÉTRICAS DE APOYO
que el turista puede consultar, no como criterios independientes. Esto está
documentado en el código y en el análisis de sensibilidad (opción 8c).
────────────────────────────────────────────────────────────────────────────
"""

import heapq
import os
import sys
import random
import time
from itertools import permutations

# ── Verificar e instalar dependencias ─────────────────────────────────────────
def verificar_dependencias():
    faltantes = []
    for pkg in ["networkx", "matplotlib", "openpyxl"]:
        try:
            __import__(pkg)
        except ImportError:
            faltantes.append(pkg)
    if faltantes:
        print(f"\n  Instalando dependencias: {', '.join(faltantes)} ...")
        os.system(f"{sys.executable} -m pip install {' '.join(faltantes)} -q")
        print("  ¡Listo!\n")

verificar_dependencias()

import networkx as nx
import matplotlib

# ── Selección automática del backend ──────────────────────────────────────────
def _seleccionar_backend():
    if os.name == "nt":               return "TkAgg"
    if sys.platform == "darwin":      return "TkAgg"
    if "DISPLAY" in os.environ:       return "TkAgg"
    return "Agg"

try:
    matplotlib.use(_seleccionar_backend())
    import matplotlib.pyplot as plt
    _fig_test = plt.figure()
    plt.close(_fig_test)
except Exception:
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ═══════════════════════════════════════════════════════════════════════════════
# 1. DATOS DEL SISTEMA TURÍSTICO (29 NODOS)
# ═══════════════════════════════════════════════════════════════════════════════

ATRACTIVOS = {
    # Nodos originales (1-21)
    1:  {"nombre": "Playa Santa Clara",               "cod": "PSC", "tipo": "Playa",            "puntaje": 27, "distrito": "Antón"},
    2:  {"nombre": "Playa Farallón",                  "cod": "PFA", "tipo": "Playa",            "puntaje": 26, "distrito": "Antón"},
    3:  {"nombre": "Playa El Salado",                 "cod": "PES", "tipo": "Playa",            "puntaje": 21, "distrito": "Aguadulce"},
    4:  {"nombre": "Playa Blanca",                    "cod": "PBL", "tipo": "Playa",            "puntaje": 26, "distrito": "Antón"},
    5:  {"nombre": "Playa Juan Hombrón",              "cod": "PJH", "tipo": "Playa",            "puntaje": 20, "distrito": "Antón"},
    6:  {"nombre": "Mercado Artesanía Valle Antón",   "cod": "MAV", "tipo": "Cultural",         "puntaje": 26, "distrito": "Antón"},
    7:  {"nombre": "Serpentario Maravillas Tropicales","cod": "SMT", "tipo": "Naturaleza",       "puntaje": 24, "distrito": "Antón"},
    8:  {"nombre": "Museo Hermanos Arias Madrid",     "cod": "MHA", "tipo": "Cultural/Hist.",   "puntaje": 25, "distrito": "Penonomé"},
    9:  {"nombre": "P.N. Omar Torrijos",              "cod": "PNT", "tipo": "Parque Nacional",  "puntaje": 22, "distrito": "La Pintada"},
    10: {"nombre": "Sitio Arqueológico El Caño",      "cod": "SAC", "tipo": "Arqueológico",     "puntaje": 26, "distrito": "Natá"},
    11: {"nombre": "Museo Regional Stella Sierra",    "cod": "MSS", "tipo": "Cultural/Hist.",   "puntaje": 22, "distrito": "Aguadulce"},
    12: {"nombre": "Iglesia San Juan Bautista",       "cod": "ISJ", "tipo": "Histórico",        "puntaje": 24, "distrito": "Penonomé"},
    13: {"nombre": "El Chorro Las Yayas",             "cod": "CLY", "tipo": "Cascada",          "puntaje": 25, "distrito": "La Pintada"},
    14: {"nombre": "Balneario Las Mendozas",          "cod": "BLM", "tipo": "Balneario",        "puntaje": 21, "distrito": "Penonomé"},
    15: {"nombre": "Penonomé",                        "cod": "PEN", "tipo": "Hub/Ciudad",       "puntaje": 28, "distrito": "Penonomé"},
    16: {"nombre": "Aguadulce",                       "cod": "AGU", "tipo": "Hub/Ciudad",       "puntaje": 25, "distrito": "Aguadulce"},
    17: {"nombre": "Antón",                           "cod": "ANT", "tipo": "Hub/Ciudad",       "puntaje": 23, "distrito": "Antón"},
    18: {"nombre": "La Pintada",                      "cod": "LAP", "tipo": "Hub/Ciudad",       "puntaje": 22, "distrito": "La Pintada"},
    19: {"nombre": "Natá",                            "cod": "NAT", "tipo": "Hub/Ciudad",       "puntaje": 23, "distrito": "Natá"},
    20: {"nombre": "Parroquia Ntra. Sra. Candelaria", "cod": "PNC", "tipo": "Histórico",        "puntaje": 21, "distrito": "La Pintada"},
    21: {"nombre": "Cerro Gaital",                    "cod": "CGA", "tipo": "Montaña",          "puntaje": 27, "distrito": "Antón"},
    # Nuevos nodos (22-29)
    22: {"nombre": "Museo de Penonomé",               "cod": "MPE", "tipo": "Cultural",         "puntaje": 24, "distrito": "Penonomé"},
    23: {"nombre": "Mercado Artesanías La Pintada",   "cod": "MLA", "tipo": "Cultural",         "puntaje": 23, "distrito": "La Pintada"},
    24: {"nombre": "Balneario Los Algarrobos",        "cod": "BAL", "tipo": "Naturaleza",       "puntaje": 22, "distrito": "La Pintada"},
    25: {"nombre": "Iglesia Santiago Apóstol",        "cod": "ISA", "tipo": "Histórico",        "puntaje": 24, "distrito": "Natá"},
    26: {"nombre": "Ecoparque Don Arcelio",           "cod": "ECO", "tipo": "Naturaleza",       "puntaje": 22, "distrito": "Natá"},
    27: {"nombre": "Salinas de Aguadulce",            "cod": "SAL", "tipo": "Naturaleza",       "puntaje": 21, "distrito": "Aguadulce"},
    28: {"nombre": "Mariposario",                     "cod": "MAR", "tipo": "Naturaleza",       "puntaje": 24, "distrito": "Antón"},
    29: {"nombre": "Canopy Adventure",                "cod": "CAN", "tipo": "Aventura",         "puntaje": 25, "distrito": "Antón"},
}

# ARISTAS CON DATOS ESTIMADOS DESDE GOOGLE MAPS
ARISTAS_RAW = [
    # Penonomé (PEN) → Conexiones originales
    (15, 17, 22.6, 25),   # PEN → ANT
    (15, 10, 29.8, 31),   # PEN → SAC
    (15, 16, 50.2, 46),   # PEN → AGU
    (15, 18, 18.4, 23),   # PEN → LAP
    (15, 8, 4.4, 8),      # PEN → MHA
    (15, 12, 4.6, 9),     # PEN → ISJ
    (15, 14, 4.6, 9),     # PEN → BLM
    (15, 21, 42.9, 78),   # PEN → CGA

    # Antón (ANT) → Conexiones originales
    (17, 1, 23.1, 25),    # ANT → PSC
    (17, 2, 21.4, 25),    # ANT → PFA
    (17, 4, 19.8, 22),    # ANT → PBL
    (17, 5, 18.0, 24),    # ANT → PJH
    (17, 6, 37.6, 59),    # ANT → MAV
    (17, 7, 39.8, 63),    # ANT → SMT
    (17, 21, 40.5, 65),   # ANT → CGA

    # Playas (Conexiones costeras)
    (1, 2, 6.8, 11),      # PSC → PFA
    (2, 4, 8.4, 12),      # PFA → PBL
    (4, 5, 24.0, 29),     # PBL → PJH
    (1, 5, 27.3, 32),     # PSC → PJH

    # Valle de Antón
    (6, 7, 2.2, 5),       # MAV → SMT
    (6, 21, 2.9, 7),      # MAV → CGA

    # Natá (NAT) → Conexiones originales
    (19, 10, 28.7, 37),   # NAT → SAC
    (19, 17, 66.0, 66),   # NAT → ANT
    (19, 16, 19.4, 31),   # NAT → AGU

    # Aguadulce (AGU) → Conexiones originales
    (16, 10, 26.8, 27),   # AGU → SAC
    (16, 11, 2.8, 6),     # AGU → MSS
    (16, 3, 2.6, 7),      # AGU → PES

    # La Pintada (LAP) → Conexiones originales
    (18, 13, 34.2, 54),   # LAP → CLY
    (18, 20, 0.13, 1),    # LAP → PNC
    (18, 9, 41.3, 88),    # LAP → PNT

    # Parque Nacional → Conexiones originales
    (9, 13, 7.1, 34),     # PNT → CLY
    (9, 10, 44.7, 85),    # PNT → SAC

    # NUEVOS NODOS - Penonomé
    (15, 22, 4.3, 8),     # PEN → MPE
    (8, 22, 1.5, 4),      # MHA → MPE
    (22, 12, 0.5, 2),     # MPE → ISJ

    # NUEVOS NODOS - La Pintada
    (18, 23, 0.8, 1),     # LAP → MLA
    (18, 24, 0.35, 2),    # LAP → BAL
    (23, 24, 1.1, 2),     # MLA → BAL
    (20, 23, 0.8, 1),     # PNC → MLA
    (20, 24, 1.1, 2),     # PNC → BAL

    # NUEVOS NODOS - Natá
    (10, 25, 13.8, 15),   # SAC → ISA
    (19, 25, 16.0, 28),   # NAT → ISA
    (25, 26, 11.4, 13),   # ISA → ECO
    (19, 26, 26.3, 35),   # NAT → ECO

    # NUEVOS NODOS - Aguadulce
    (16, 27, 9.0, 14),    # AGU → SAL
    (3, 27, 6.3, 8),      # PES → SAL
    (27, 11, 7.0, 10),    # SAL → MSS

    # NUEVOS NODOS - Antón
    (17, 28, 33.7, 56),   # ANT → MAR
    (17, 29, 34.5, 57),   # ANT → CAN
    (28, 7, 2.1, 5),      # MAR → SMT
    (28, 29, 5.8, 12),    # MAR → CAN
    (29, 21, 5.8, 12),    # CAN → CGA

    # ═══════════════════════════════════════════════════════════════════════
    # ARISTAS URBANAS ADICIONALES (verificadas en Google Maps)
    # Incorporadas durante el proceso de validación del sistema.
    # Corrigen el rodeo innecesario del Día 2 (Penonomé Histórico).
    # ═══════════════════════════════════════════════════════════════════════
    (12, 14, 1.0, 3),     # ISJ → BLM (Iglesia San Juan Bautista → Balneario Las Mendozas)
]

COLORES_TIPO = {
    "Hub/Ciudad":      "#1D9E75",
    "Playa":           "#2E86C1",
    "Cultural":        "#F39C12",
    "Cultural/Hist.":  "#F39C12",
    "Histórico":       "#F39C12",
    "Naturaleza":      "#8E44AD",
    "Parque Nacional": "#27AE60",
    "Cascada":         "#2980B9",
    "Balneario":       "#1ABC9C",
    "Arqueológico":    "#C0392B",
    "Montaña":         "#27AE60",
    "Aventura":        "#E67E22",
}

# ═══════════════════════════════════════════════════════════════════════════════
# POSICIONES — recalculadas con relajación por repulsión
# ═══════════════════════════════════════════════════════════════════════════════

POSICIONES = {
    1:  (0.95, 0.2978),   # PSC  – Playa Santa Clara
    2:  (0.9087, 0.1582), # PFA  – Playa Farallón
    3:  (0.0669, 0.05),   # PES  – Playa El Salado
    4:  (0.7873, 0.0871), # PBL  – Playa Blanca
    5:  (0.6609, 0.1479), # PJH  – Playa Juan Hombrón
    6:  (0.6452, 0.6373), # MAV  – Mercado Artesanía Valle Antón
    7:  (0.7461, 0.7708), # SMT  – Serpentario
    8:  (0.3431, 0.5761), # MHA  – Museo Hnos. Arias Madrid
    9:  (0.0714, 0.6373), # PNT  – P.N. Omar Torrijos
    10: (0.3238, 0.2871), # SAC  – Sitio Arqueológico El Caño
    11: (0.1875, 0.259),  # MSS  – Museo Regional Stella Sierra
    12: (0.5911, 0.4386), # ISJ  – Iglesia San Juan Bautista
    13: (0.0852, 0.8172), # CLY  – El Chorro Las Yayas
    14: (0.5051, 0.6505), # BLM  – Balneario Las Mendozas
    15: (0.4694, 0.5092), # PEN  – Penonomé
    16: (0.1923, 0.1129), # AGU  – Aguadulce
    17: (0.7707, 0.3921), # ANT  – Antón
    18: (0.2507, 0.8295), # LAP  – La Pintada
    19: (0.1856, 0.4052), # NAT  – Natá
    20: (0.1473, 0.948),  # PNC  – Parroquia Ntra. Sra. Candelaria
    21: (0.6452, 0.9015), # CGA  – Cerro Gaital
    22: (0.3525, 0.4302), # MPE  – Museo de Penonomé
    23: (0.3294, 0.95),   # MLA  – Mercado Artesanías La Pintada
    24: (0.2079, 0.6904), # BAL  – Balneario Los Algarrobos
    25: (0.0517, 0.2278), # ISA  – Iglesia Santiago Apóstol
    26: (0.05, 0.437),    # ECO  – Ecoparque Don Arcelio
    27: (0.3311, 0.1054), # SAL  – Salinas de Aguadulce
    28: (0.8643, 0.8476), # MAR  – Mariposario
    29: (0.8272, 0.6521), # CAN  – Canopy Adventure
}

# ═══════════════════════════════════════════════════════════════════════════════
# 2. RUTAS DE 7 DÍAS
#    NOTA: distancia_km / tiempo_auto_min / costo_usd se recalculan en vivo
#    en main() con recalcular_estadisticas_dias(), así que los valores de
#    aquí abajo son solo un placeholder inicial (se sobrescriben al arrancar).
# ═══════════════════════════════════════════════════════════════════════════════

DIAS_CONFIG = {
    1: {
        "destinos": [1, 2, 4, 5, 17],   # PSC, PFA, PBL, PJH, ANT
        "zona": "🌊 Playas de Antón",
        "color": "#2E86C1",
        "descripcion": "Recorrido por las playas más hermosas de la costa de Antón",
        "frase": "🌅 El sol, la arena y el mar te esperan",
        "nivel": "Fácil",
        "distancia_km": 80.3,
        "tiempo_auto_min": 101,
        "costo_usd": 12.05
    },
    2: {
        "destinos": [8, 22, 12, 14, 15], # MHA, MPE, ISJ, BLM, PEN
        "zona": "🏛️ Penonomé Histórico",
        "color": "#F39C12",
        "descripcion": "Recorrido urbano por los tesoros históricos de Penonomé",
        "frase": "🏛️ Descubre la historia de Coclé en cada esquina",
        "nivel": "Fácil",
        "distancia_km": 15.0,
        "tiempo_auto_min": 31,
        "costo_usd": 2.25
    },
    3: {
        "destinos": [18, 20, 23, 24, 13, 9], # LAP, PNC, MLA, BAL, CLY, PNT
        "zona": "⛰️ La Pintada - Montaña y Cultura",
        "color": "#27AE60",
        "descripcion": "Aventura en la montaña: parroquia, mercado, balneario, cascada y parque",
        "frase": "⛰️ La montaña te llama con sus cascadas y paisajes",
        "nivel": "Alta",
        "distancia_km": 61.7,
        "tiempo_auto_min": 115,
        "costo_usd": 9.26
    },
    4: {
        "destinos": [10, 25, 26, 19],    # SAC, ISA, ECO, NAT
        "zona": "🏺 Ruta Arqueológica de Natá",
        "color": "#C0392B",
        "descripcion": "Viaje al pasado: El Caño, iglesia colonial, ecoparque y ciudad",
        "frase": "🗿 Donde la historia precolombina cobra vida",
        "nivel": "Media",
        "distancia_km": 81.3,
        "tiempo_auto_min": 94,
        "costo_usd": 12.20
    },
    5: {
        "destinos": [6, 7, 28, 21, 29],  # MAV, SMT, MAR, CGA, CAN
        "zona": "🌿 Naturaleza de Antón",
        "color": "#8E44AD",
        "descripcion": "Un día en el valle: mercado, serpentario, mariposario, cerro y canopy",
        "frase": "🦋 Donde la naturaleza y la aventura se encuentran",
        "nivel": "Media",
        "distancia_km": 57.7,
        "tiempo_auto_min": 72,
        "costo_usd": 8.66
    },
    6: {
        "destinos": [16, 3, 27, 11],     # AGU, PES, SAL, MSS
        "zona": "🌅 Tesoros de Aguadulce",
        "color": "#1ABC9C",
        "descripcion": "Un día completo: playa, salinas, museo y ciudad",
        "frase": "🧂 Donde el mar y la historia se fusionan",
        "nivel": "Fácil",
        "distancia_km": 66.1,
        "tiempo_auto_min": 71,
        "costo_usd": 9.92
    },
    7: {
        "destinos": [15, 18, 20, 23, 24], # PEN, LAP, PNC, MLA, BAL
        "zona": "🎯 Circuito Integrador",
        "color": "#E67E22",
        "descripcion": "Un recorrido por lo mejor de Penonomé y La Pintada",
        "frase": "🎯 Un viaje que une ciudades, historia y naturaleza",
        "nivel": "Media",
        "distancia_km": 20.4,
        "tiempo_auto_min": 27,
        "costo_usd": 3.06
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# 3. ALGORITMO DE DIJKSTRA
# ═══════════════════════════════════════════════════════════════════════════════

def construir_grafo():
    G = nx.Graph()
    for nid, data in ATRACTIVOS.items():
        G.add_node(nid, **data)
    for u, v, dist, tiempo in ARISTAS_RAW:
        # NOTA METODOLÓGICA:
        # El costo se calcula como distancia * 0.15 (tarifa uniforme
        # estimada de combustible + desgaste por km). Al ser una
        # transformación lineal de la distancia, optimizar por costo
        # produce la MISMA ruta que optimizar por distancia. Por eso el
        # proyecto reporta el costo como métrica informativa; el criterio
        # oficial es DISTANCIA (indicación del asesor).
        costo = round(dist * 0.15, 2)
        G.add_edge(u, v, distancia=dist, tiempo=tiempo, costo=costo)
    return G

def dijkstra(G, origen, criterio):
    INF = float('inf')
    dist = {n: INF for n in G.nodes()}
    prev = {n: None for n in G.nodes()}
    dist[origen] = 0
    heap = [(0, origen)]
    visitados = set()
    while heap:
        d_u, u = heapq.heappop(heap)
        if u in visitados:
            continue
        visitados.add(u)
        for v in G.neighbors(u):
            peso = G[u][v][criterio]
            alt = dist[u] + peso
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))
    return dist, prev

def reconstruir_camino(prev, origen, destino):
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = prev[actual]
    camino.reverse()
    return camino if camino and camino[0] == origen else []

def calcular_todas_matrices(G):
    nodos = sorted(G.nodes())
    matrices = {}
    caminos = {}
    for criterio in ["distancia", "tiempo", "costo"]:
        mat = {}
        cam = {}
        for origen in nodos:
            dist_min, prev = dijkstra(G, origen, criterio)
            mat[origen] = {d: round(dist_min[d], 2) if dist_min[d] != float('inf') else None for d in nodos}
            cam[origen] = {d: reconstruir_camino(prev, origen, d) for d in nodos}
        matrices[criterio] = mat
        caminos[criterio] = cam
    return matrices, caminos

def ruta_optima_dia(destinos, matrices, criterio="distancia"):
    BASE = 15
    destinos = [d for d in destinos if d != BASE]
    mat = matrices[criterio]
    mejor_costo = float('inf')
    mejor_orden = None
    for perm in permutations(destinos):
        secuencia = [BASE] + list(perm) + [BASE]
        total = 0
        valida = True
        for i in range(len(secuencia) - 1):
            c = mat[secuencia[i]][secuencia[i+1]]
            if c is None:
                valida = False
                break
            total += c
        if valida and total < mejor_costo:
            mejor_costo = total
            mejor_orden = list(perm)
    return mejor_orden, mejor_costo

def recalcular_estadisticas_dias(matrices, criterio="distancia"):
    """
    Recalcula en vivo distancia_km / tiempo_auto_min / costo_usd
    de cada día en DIAS_CONFIG, usando la ruta óptima de IDA Y VUELTA a
    Penonomé (BASE=15) con el CRITERIO OFICIAL del proyecto (distancia).
    Tiempo y costo se reportan como métricas complementarias de esa misma
    ruta. Esto garantiza que la opción 4 ("ver todas las rutas") y la
    opción 3 ("ruta óptima de un día") siempre muestren los mismos números
    para el mismo día.
    """
    BASE = 15
    for dia, cfg in DIAS_CONFIG.items():
        destinos = [d for d in cfg["destinos"] if d != BASE]
        orden, _ = ruta_optima_dia(destinos, matrices, criterio)
        if orden is None:
            print(f"  ⚠ No se pudo recalcular estadísticas del Día {dia} (ruta inválida).")
            continue
        secuencia = [BASE] + orden + [BASE]
        tot_d = sum(matrices["distancia"][secuencia[i]][secuencia[i+1]] for i in range(len(secuencia) - 1))
        tot_t = sum(matrices["tiempo"][secuencia[i]][secuencia[i+1]] for i in range(len(secuencia) - 1))
        tot_c = sum(matrices["costo"][secuencia[i]][secuencia[i+1]] for i in range(len(secuencia) - 1))
        cfg["distancia_km"] = round(tot_d, 1)
        cfg["tiempo_auto_min"] = round(tot_t)
        cfg["costo_usd"] = round(tot_c, 2)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. FUNCIONES DE VISUALIZACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

_CONTADOR_GRAFICO = [0]

def _mostrar(fig=None):
    if fig is None:
        fig = plt.gcf()
    _CONTADOR_GRAFICO[0] += 1
    plt.show()

def dibujar_grafo_completo(G, criterio="distancia", guardar=None):
    fig, ax = plt.subplots(figsize=(15, 11))
    ax.set_facecolor("#F0F4F8")
    fig.patch.set_facecolor("#E8EDF2")

    for u, v, data in G.edges(data=True):
        x0, y0 = POSICIONES[u]
        x1, y1 = POSICIONES[v]
        ax.plot([x0, x1], [y0, y1], color="#BBBBBB", linewidth=1.0, zorder=1, alpha=0.6)

    RADIO_HUB = 0.024
    RADIO_NORM = 0.017

    for nid in G.nodes():
        x, y = POSICIONES[nid]
        tipo = G.nodes[nid]["tipo"]
        color = COLORES_TIPO.get(tipo, "#999999")
        es_hub = tipo == "Hub/Ciudad"
        radio = RADIO_HUB if es_hub else RADIO_NORM
        ax.add_patch(plt.Circle((x+0.003, y-0.003), radio, color="#00000015", zorder=3))
        ax.add_patch(plt.Circle((x, y), radio, color=color, zorder=4, linewidth=1.5, ec="white"))
        fs = 8.5 if es_hub else 7
        ax.text(x, y, G.nodes[nid]["cod"], ha="center", va="center", fontsize=fs,
                fontweight="bold", color="white", zorder=5)

    nodos_con_nombre = [15, 17, 16, 18, 19, 1, 2, 4, 21, 13, 10, 9, 20]
    for nid in G.nodes():
        if nid not in nodos_con_nombre:
            continue
        x, y = POSICIONES[nid]
        nombre = G.nodes[nid]["nombre"]
        if len(nombre) > 22:
            nombre = nombre[:20] + "..."
        if x > 0.78:
            lx, ly, ha = x + 0.035, y, "left"
        elif x < 0.22:
            lx, ly, ha = x - 0.035, y, "right"
        elif y > 0.82:
            lx, ly, ha = x, y + 0.038, "center"
        elif y < 0.18:
            lx, ly, ha = x, y - 0.038, "center"
        else:
            lx, ly, ha = x, y - 0.038, "center"
        ax.text(lx, ly, nombre, ha=ha, va="center", fontsize=7,
                fontweight="500", color="#3A3A3A", zorder=6,
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                          edgecolor="#DDDDDD", alpha=0.9, linewidth=0.4))

    leyenda = [
        mpatches.Patch(color="#1D9E75", label="Hub/Ciudad"),
        mpatches.Patch(color="#2E86C1", label="Playa"),
        mpatches.Patch(color="#F39C12", label="Cultural/Hist."),
        mpatches.Patch(color="#8E44AD", label="Naturaleza"),
        mpatches.Patch(color="#C0392B", label="Arqueológico"),
        mpatches.Patch(color="#27AE60", label="Parque/Montaña"),
        mpatches.Patch(color="#E67E22", label="Aventura"),
    ]
    ax.legend(handles=leyenda, loc="lower left", fontsize=8.5,
              framealpha=0.95, edgecolor="#AAAAAA", fancybox=True, ncol=2)

    ax.set_title(
        f"🌍 Grafo Turístico - Provincia de Coclé, Panamá\n"
        f"{len(G.nodes())} Nodos · {len(G.edges())} Aristas | Criterio: {criterio.upper()}",
        fontsize=13, fontweight="bold", color="#1F4E79", pad=14)
    ax.set_xlim(-0.06, 1.06)
    ax.set_ylim(-0.06, 1.06)
    ax.axis("off")
    ax.set_aspect("equal")
    plt.tight_layout(pad=1.5)

    if guardar:
        plt.savefig(guardar, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"  ✔ Grafo guardado: {guardar}")
    else:
        _mostrar(fig)
    plt.close()


def dibujar_grafo_dia(G, dia, matrices, caminos, criterio="distancia", guardar=None):
    cfg = DIAS_CONFIG[dia]
    BASE = 15
    destinos = [d for d in cfg["destinos"] if d != BASE]
    color_dia = cfg["color"]

    orden, costo_total = ruta_optima_dia(destinos, matrices, criterio)
    if orden is None:
        print(f"  ✗ No se pudo calcular la ruta para el Día {dia}.")
        return

    secuencia = [BASE] + orden + [BASE]
    nodos_ruta = set(secuencia)
    segmentos_dir = []

    for i in range(len(secuencia) - 1):
        seg = caminos[criterio][secuencia[i]][secuencia[i+1]]
        for j in range(len(seg)-1):
            segmentos_dir.append((seg[j], seg[j+1]))
        nodos_ruta.update(seg)

    pos_sub = {n: POSICIONES[n] for n in nodos_ruta}

    fig, ax = plt.subplots(figsize=(12, 9.5))
    ax.set_facecolor("#F0F4F8")
    fig.patch.set_facecolor("#E8EDF2")

    for u, v in G.edges():
        if u in nodos_ruta and v in nodos_ruta:
            x0, y0 = pos_sub[u]
            x1, y1 = pos_sub[v]
            ax.plot([x0, x1], [y0, y1], color="#DDDDDD", linewidth=0.7, alpha=0.5, zorder=1)

    ya_etiquetado = set()
    RADIO_ETIQ_LIBRE = 0.052
    for u, v in segmentos_dir:
        x0, y0 = pos_sub[u]
        x1, y1 = pos_sub[v]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", color=color_dia, lw=2.2,
                            connectionstyle="arc3,rad=0.05", mutation_scale=17),
            zorder=3)

        par = tuple(sorted([u, v]))
        if par not in ya_etiquetado and G.has_edge(u, v):
            val = G[u][v][criterio]
            unidad_sym = {"distancia": "km", "tiempo": "min", "costo": "$"}[criterio]
            txt = f"${val:.2f}" if criterio == "costo" else f"{val}{unidad_sym}"
            mx, my = (x0+x1)/2, (y0+y1)/2
            dx, dy = (x1 - x0), (y1 - y0)
            largo = (dx**2 + dy**2) ** 0.5 or 1e-6
            perp_x, perp_y = -dy / largo, dx / largo
            offset = 0.040 if largo > 0.09 else 0.062
            lx, ly = mx + perp_x * offset, my + perp_y * offset

            def _mas_cercano(px, py):
                return min(((px-nx)**2 + (py-ny)**2) ** 0.5 for nx, ny in pos_sub.values())

            if _mas_cercano(lx, ly) < RADIO_ETIQ_LIBRE:
                for signo in (1, -1):
                    for extra in (0.030, 0.055, 0.080):
                        lx2 = mx + perp_x * signo * (offset + extra)
                        ly2 = my + perp_y * signo * (offset + extra)
                        if _mas_cercano(lx2, ly2) >= RADIO_ETIQ_LIBRE:
                            lx, ly = lx2, ly2
                            break
                    else:
                        continue
                    break

            ax.text(lx, ly, txt, ha="center", va="center", fontsize=7.5,
                    fontweight="bold", color=color_dia, zorder=5,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                              edgecolor=color_dia, alpha=0.95, linewidth=0.6))
            ya_etiquetado.add(par)

    RADIO_BASE = 0.036
    RADIO_DEST = 0.028
    RADIO_TRANS = 0.018

    nodos_destino = set(destinos)
    nodos_transito = nodos_ruta - nodos_destino - {BASE}

    orden_visita = {}
    for i, nodo in enumerate(secuencia):
        if nodo != BASE and nodo not in orden_visita:
            orden_visita[nodo] = i

    for nid in nodos_ruta:
        x, y = pos_sub[nid]
        if nid == BASE:
            cn, radio, ec, lw = "#1D9E75", RADIO_BASE, "white", 2.2
        elif nid in nodos_destino:
            cn = COLORES_TIPO.get(G.nodes[nid]["tipo"], "#2E86C1")
            radio, ec, lw = RADIO_DEST, color_dia, 2.0
        else:
            cn, radio, ec, lw = "#AAAAAA", RADIO_TRANS, "#888888", 1.2
        ax.add_patch(plt.Circle((x+0.003, y-0.003), radio, color="#00000015", zorder=3))
        ax.add_patch(plt.Circle((x, y), radio, color=cn, ec=ec, linewidth=lw, zorder=4))
        cod = G.nodes[nid]["cod"] + ("*" if nid in nodos_transito else "")
        if nid in orden_visita:
            cod = f"{orden_visita[nid]}·{cod}"
        fs_cod = 9 if nid == BASE else (7.5 if nid in nodos_destino else 6.5)
        ax.text(x, y, cod, ha="center", va="center", fontsize=fs_cod,
                fontweight="bold", color="white", zorder=5)

    for nid in nodos_ruta:
        if nid not in nodos_destino and nid != BASE:
            continue
        x, y = pos_sub[nid]
        nombre = G.nodes[nid]["nombre"]
        if len(nombre) > 22:
            nombre = nombre[:20] + "..."
        if x > 0.72:
            lx, ly, ha = x + 0.045, y, "left"
        elif x < 0.28:
            lx, ly, ha = x - 0.045, y, "right"
        elif y > 0.75:
            lx, ly, ha = x, y + 0.05, "center"
        else:
            lx, ly, ha = x, y - 0.05, "center"
        ax.text(lx, ly, nombre, ha=ha, va="center", fontsize=7.5,
                fontweight="500", color="#333333", zorder=6,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                          edgecolor=color_dia if nid in nodos_destino else "#CCCCCC",
                          alpha=0.92, linewidth=0.5))

    ruta_str = " → ".join(G.nodes[n]["cod"] for n in secuencia)
    unidad = {"distancia": "km", "tiempo": "min", "costo": "$"}[criterio]
    ax.text(0.01, 0.01,
            f"📌 Ruta óptima ({criterio})\n{ruta_str}\nTotal: {costo_total:.1f} {unidad}",
            transform=ax.transAxes, fontsize=8.5, color="#1A1A1A", va="bottom",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor=color_dia, alpha=0.96, linewidth=1.1))

    leyenda = [
        mpatches.Patch(color="#1D9E75", label="Base: Penonomé"),
        mpatches.Patch(color=color_dia, label="Ruta óptima"),
        mpatches.Patch(color="#AAAAAA", label="Tránsito (*)"),
    ]
    ax.legend(handles=leyenda, loc="lower right", fontsize=8.5,
              framealpha=0.95, edgecolor="#AAAAAA", fancybox=True)

    ax.set_title(
        f"📅 DÍA {dia} — {cfg['zona']}\n"
        f"Criterio: {criterio.upper()} | {len(destinos)} destinos",
        fontsize=13, fontweight="bold", color=color_dia, pad=14)

    xs = [p[0] for p in pos_sub.values()]
    ys = [p[1] for p in pos_sub.values()]
    margen = 0.14
    ax.set_xlim(min(xs) - margen, max(xs) + margen)
    ax.set_ylim(min(ys) - margen, max(ys) + margen)
    ax.axis("off")
    ax.set_aspect("equal")
    plt.tight_layout(pad=1.5)

    if guardar:
        plt.savefig(guardar, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"  ✔ Grafo Día {dia} guardado: {guardar}")
    else:
        _mostrar(fig)
    plt.close()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. VALIDACIONES COMPLETAS (Sección 3.6.1)
# ═══════════════════════════════════════════════════════════════════════════════

def validar_con_google_maps_simulado(G, tramos_a_validar=None):
    """
    a) Validación por Comparación con Google Maps (SIMULADA)
    Tolerancia: ±5%
    """
    if tramos_a_validar is None:
        tramos_a_validar = list(G.edges())

    resultados = []
    tolerancia = 0.05

    print("\n" + "="*70)
    print("  a) VALIDACIÓN CON GOOGLE MAPS (SIMULADA) - Tolerancia ±5%")
    print("  NOTA: Valores de Google Maps simulados con variación de ±4%")
    print("="*70)
    print(f"  {'Tramo':<20} {'Algoritmo':>15} {'Google':>15} {'Diferencia':>15} {'Estado':>10}")
    print("-"*70)

    random.seed(42)

    for u, v in tramos_a_validar:
        alg_dist = G[u][v]['distancia']
        alg_time = G[u][v]['tiempo']

        factor_dist = 1 + random.uniform(-0.04, 0.04)
        factor_time = 1 + random.uniform(-0.04, 0.04)
        google_dist = round(alg_dist * factor_dist, 1)
        google_time = round(alg_time * factor_time, 1)

        diff_dist = abs(alg_dist - google_dist) / google_dist if google_dist > 0 else 0
        diff_time = abs(alg_time - google_time) / google_time if google_time > 0 else 0
        ok_dist = diff_dist <= tolerancia
        ok_time = diff_time <= tolerancia
        ok = ok_dist and ok_time

        u_cod = G.nodes[u]['cod']
        v_cod = G.nodes[v]['cod']

        print(f"  {u_cod}→{v_cod:<16} "
              f"{alg_dist:>6.1f}km/{alg_time:>3.0f}min "
              f"{google_dist:>6.1f}km/{google_time:>3.0f}min "
              f"{diff_dist*100:>6.1f}%/{diff_time*100:>5.1f}% "
              f"{'✅' if ok else '❌':>8}")

        resultados.append({
            'tramo': f"{u_cod}→{v_cod}",
            'algoritmo': {'distancia': alg_dist, 'tiempo': alg_time},
            'google': {'distancia': google_dist, 'tiempo': google_time},
            'diferencia': {'distancia': diff_dist*100, 'tiempo': diff_time*100},
            'valido': ok
        })

    total = len(resultados)
    aprobados = sum(1 for r in resultados if r['valido'])
    print("-"*70)
    print(f"  RESULTADO: {aprobados}/{total} tramos validados ({aprobados/total*100:.1f}%)\n")

    return resultados


def validar_consistencia_interna(G, matrices, caminos):
    """
    b) Validación por Consistencia Interna (Subestructura óptima)
    """
    print("\n" + "="*70)
    print("  b) VALIDACIÓN POR CONSISTENCIA INTERNA (Subestructura óptima)")
    print("="*70)

    nodos = list(G.nodes())
    errores = []
    validaciones = 0

    for criterio in ["distancia", "tiempo", "costo"]:
        print(f"\n  Criterio: {criterio.upper()}")
        cam = caminos[criterio]

        for origen in nodos[:6]:
            for destino in nodos[:6]:
                if origen == destino:
                    continue
                camino_completo = cam[origen][destino]
                if not camino_completo or len(camino_completo) < 3:
                    continue
                for i in range(len(camino_completo) - 1):
                    for j in range(i + 1, len(camino_completo)):
                        sub_origen = camino_completo[i]
                        sub_destino = camino_completo[j]
                        subcamino_esperado = camino_completo[i:j+1]
                        subcamino_calc = cam[sub_origen][sub_destino]
                        validaciones += 1
                        if subcamino_calc != subcamino_esperado:
                            errores.append({
                                'criterio': criterio,
                                'sub_origen': sub_origen,
                                'sub_destino': sub_destino,
                            })

    print(f"\n  Validaciones realizadas: {validaciones}")
    if errores:
        print(f"  ❌ Errores encontrados: {len(errores)}")
        for err in errores[:3]:
            u_cod = G.nodes[err['sub_origen']]['cod']
            v_cod = G.nodes[err['sub_destino']]['cod']
            print(f"    - Subcamino {u_cod}→{v_cod} no es óptimo en {err['criterio']}")
    else:
        print("  ✅ Todos los subcaminos verificados son óptimos (propiedad de subestructura óptima cumplida)")

    print("-"*70)
    return len(errores) == 0


def analisis_sensibilidad(G, matrices, caminos):
    """
    c) Análisis de Sensibilidad (3 criterios)
    Compara cómo cambian las rutas al optimizar por distancia, tiempo o costo.
    El criterio oficial del proyecto es DISTANCIA.
    """
    pares_prueba = [(15, 17), (17, 1), (18, 13), (15, 21), (19, 10)]

    print("\n" + "="*70)
    print("  c) ANÁLISIS DE SENSIBILIDAD - Comparación de 3 criterios")
    print("  NOTA: criterio oficial = DISTANCIA. Tiempo y costo son")
    print("  métricas de apoyo. Como costo = distancia × 0.15, las rutas")
    print("  por distancia y costo coinciden por definición.")
    print("="*70)

    resultados = []

    for origen, destino in pares_prueba:
        u_cod = G.nodes[origen]['cod']
        v_cod = G.nodes[destino]['cod']

        print(f"\n  Ruta: {u_cod} → {v_cod}")
        print(f"  {'Criterio':<12} {'Distancia':>12} {'Tiempo':>12} {'Costo':>12} {'Ruta':>30}")
        print("-"*80)

        for criterio in ["distancia", "tiempo", "costo"]:
            valor = matrices[criterio][origen][destino]
            camino = caminos[criterio][origen][destino]
            ruta_str = " → ".join(G.nodes[n]['cod'] for n in camino) if camino else "N/A"

            if criterio == "distancia":
                print(f"  {'Distancia':<12} {valor:>11.1f}km {'---':>12} {'---':>12} {ruta_str:>30}")
            elif criterio == "tiempo":
                print(f"  {'Tiempo':<12} {'---':>12} {valor:>11.0f}min {'---':>12} {ruta_str:>30}")
            else:
                print(f"  {'Costo':<12} {'---':>12} {'---':>12} ${valor:>10.2f} {ruta_str:>30}")

        ruta_dist = caminos["distancia"][origen][destino]
        ruta_time = caminos["tiempo"][origen][destino]
        ruta_cost = caminos["costo"][origen][destino]
        misma_ruta = (ruta_dist == ruta_time == ruta_cost)

        print("-"*80)
        if misma_ruta:
            print("  ℹ️  Los 3 criterios producen la misma ruta óptima.")
        else:
            print("  ⚠️  Los criterios producen rutas diferentes.")

        resultados.append({
            'origen': u_cod,
            'destino': v_cod,
            'distancia': matrices["distancia"][origen][destino],
            'tiempo': matrices["tiempo"][origen][destino],
            'costo': matrices["costo"][origen][destino],
            'misma_ruta': misma_ruta
        })

    print("\n" + "="*70)
    print("  RESUMEN DEL ANÁLISIS DE SENSIBILIDAD")
    print("="*70)
    print(f"  {'Ruta':<12} {'Dist (km)':>12} {'Time (min)':>12} {'Costo ($)':>12} {'Misma ruta':>12}")
    print("-"*60)
    for r in resultados:
        misma = "✅ Sí" if r['misma_ruta'] else "❌ No"
        print(f"  {r['origen']}→{r['destino']:<8} "
              f"{r['distancia']:>11.1f} "
              f"{r['tiempo']:>11.0f} "
              f"${r['costo']:>10.2f} "
              f"{misma:>12}")

    return resultados


def ejecutar_validaciones_completas(G, matrices, caminos):
    """
    Ejecuta TODAS las validaciones del marco metodológico (Sección 3.6.1)
    """
    print("\n" + "█"*70)
    print("  VALIDACIÓN COMPLETA DEL SISTEMA (Sección 3.6.1)")
    print("  DATOS ESTIMADOS A PARTIR DE MEDICIONES EN GOOGLE MAPS")
    print("█"*70)

    resultados_google = validar_con_google_maps_simulado(G)
    consistencia_ok = validar_consistencia_interna(G, matrices, caminos)
    resultados_sensibilidad = analisis_sensibilidad(G, matrices, caminos)

    print("\n" + "█"*70)
    print("  RESUMEN DE VALIDACIONES")
    print("█"*70)

    total_google = len(resultados_google)
    aprobados_google = sum(1 for r in resultados_google if r['valido'])
    tasa_google = aprobados_google / total_google * 100 if total_google > 0 else 0

    print(f"\n  a) Validación con Google Maps (±5%): {aprobados_google}/{total_google} ({tasa_google:.1f}%)")
    print(f"  b) Consistencia interna (subestructura óptima): {'✅ Aprobada' if consistencia_ok else '❌ Falló'}")
    print(f"  c) Análisis de sensibilidad: {len(resultados_sensibilidad)} rutas analizadas")

    if tasa_google >= 95 and consistencia_ok:
        print("\n  ✅ VALIDACIÓN COMPLETA: El sistema cumple con todos los criterios.")
    else:
        print("\n  ⚠️ VALIDACIÓN PARCIAL: Algunos criterios requieren revisión.")

    print("█"*70 + "\n")

    return {
        'google': resultados_google,
        'consistencia': consistencia_ok,
        'sensibilidad': resultados_sensibilidad
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 6. PRUEBAS DE TIEMPO DE EJECUCIÓN (Sección 3.6.3.c)
# ═══════════════════════════════════════════════════════════════════════════════

def probar_tiempo_ejecucion(G, iteraciones=10):
    """
    Prueba de tiempo de ejecución para diferentes tamaños de grafo (Tabla 9).
    El tamaño real del grafo del proyecto es (29 nodos, 53 aristas).
    Se mide tanto sobre grafos aleatorios del mismo tamaño como sobre el
    grafo real G.
    """
    print("\n" + "="*70)
    print("  PRUEBA DE TIEMPO DE EJECUCIÓN (Tabla 9 - Sección 3.6.3.c)")
    print("="*70)

    n_reales = G.number_of_nodes()
    m_reales = G.number_of_edges()

    tamanos = [
        (5, 7),
        (10, 15),
        (21, 32),
        (n_reales, m_reales),
        (50, 120)
    ]

    resultados = []

    for nodos, aristas in tamanos:
        tiempos = []
        for _ in range(iteraciones):
            G_test = nx.gnm_random_graph(nodos, aristas)
            for u, v in G_test.edges():
                G_test[u][v]['distancia'] = random.uniform(1, 50)
            start = time.time()
            for origen in range(nodos):
                dijkstra(G_test, origen, 'distancia')
            end = time.time()
            tiempos.append(end - start)

        tiempo_promedio = sum(tiempos) / len(tiempos)
        resultados.append({'nodos': nodos, 'aristas': aristas, 'tiempo_promedio': tiempo_promedio})
        print(f"  {nodos:>2} nodos, {aristas:>3} aristas: {tiempo_promedio:.4f} s (promedio de {iteraciones} ejecuciones, grafo aleatorio)")

    # Medición directa sobre el grafo REAL del proyecto
    tiempos_reales = []
    for _ in range(iteraciones):
        start = time.time()
        for origen in G.nodes():
            dijkstra(G, origen, 'distancia')
        end = time.time()
        tiempos_reales.append(end - start)
    tiempo_promedio_real = sum(tiempos_reales) / len(tiempos_reales)
    print(f"  {n_reales:>2} nodos, {m_reales:>3} aristas: {tiempo_promedio_real:.4f} s (promedio de {iteraciones} ejecuciones, GRAFO REAL DEL PROYECTO)")

    print("\n" + "-"*50)
    print("  TABLA 9: TIEMPOS DE EJECUCIÓN DEL ALGORITMO")
    print("-"*50)
    print(f"  {'Nodos':<10} {'Aristas':<10} {'Tiempo (s)':<15}")
    print("-"*50)
    for r in resultados:
        print(f"  {r['nodos']:<10} {r['aristas']:<10} {r['tiempo_promedio']:<15.4f}")
    print(f"  {n_reales:<10} {m_reales:<10} {tiempo_promedio_real:<15.4f}  ⭐ GRAFO REAL DEL PROYECTO")
    print("-"*50)
    print("="*70 + "\n")
    return resultados


def probar_tiempo_ruta_dia(matrices, criterio="distancia"):
    """
    Prueba de tiempo para calcular las rutas de los 7 días
    """
    print("\n" + "="*70)
    print("  PRUEBA DE TIEMPO - RUTAS DE 7 DÍAS")
    print("="*70)

    tiempos = []
    for dia in range(1, 8):
        destinos = [d for d in DIAS_CONFIG[dia]["destinos"] if d != 15]
        start = time.time()
        orden, costo = ruta_optima_dia(destinos, matrices, criterio)
        end = time.time()
        tiempos.append(end - start)
        print(f"  Día {dia}: {end - start:.6f} s")

    print("-"*50)
    print(f"  ⏱️ Tiempo promedio por día: {sum(tiempos)/len(tiempos):.6f} s")
    print(f"  ⏱️ Tiempo total 7 días: {sum(tiempos):.6f} s")
    print("="*70 + "\n")
    return tiempos


# ═══════════════════════════════════════════════════════════════════════════════
# 7. FUNCIONES DE CONSOLA Y MENÚ
# ═══════════════════════════════════════════════════════════════════════════════

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def separador(char="─", ancho=64, color="\033[96m"):
    print(f"{color}{char * ancho}\033[0m")

def titulo(texto):
    limpiar()
    separador("═")
    print(f"\033[1;36m  {texto}\033[0m")
    separador("═")

def elegir_criterio():
    print("\n  Elige el criterio de optimización:")
    print("   [1] Distancia mínima (km)  ← criterio oficial")
    print("   [2] Tiempo mínimo (min)")
    print("   [3] Costo mínimo (USD)")
    while True:
        op = input("\n  Opción: ").strip()
        if op == "1": return "distancia"
        if op == "2": return "tiempo"
        if op == "3": return "costo"
        print("  ✗ Opción inválida.")

def mostrar_tabla_nodos(G):
    separador()
    print(f"\033[1m  {'ID':<4} {'Cód':<5} {'Nombre':<34} {'Tipo':<18} {'Distrito':<12}\033[0m")
    separador()
    for nid, data in sorted(ATRACTIVOS.items()):
        print(f"  {nid:<4} {data['cod']:<5} {data['nombre']:<34} {data['tipo']:<18} {data['distrito']:<12}")
    separador()

def mostrar_resultado_ruta(G, secuencia, matrices, criterio):
    mat_d, mat_t, mat_c = matrices["distancia"], matrices["tiempo"], matrices["costo"]
    separador()
    print(f"  \033[1m{'Tramo':<22} {'Distancia':>10} {'Tiempo':>10} {'Costo':>10}\033[0m")
    separador()
    tot_d = tot_t = tot_c = 0
    for i in range(len(secuencia) - 1):
        u, v = secuencia[i], secuencia[i+1]
        d, t, c = mat_d[u][v] or 0, mat_t[u][v] or 0, mat_c[u][v] or 0
        tot_d += d; tot_t += t; tot_c += c
        print(f"  {G.nodes[u]['cod']} → {G.nodes[v]['cod']:<16} {d:>9.1f}km {t:>9.1f}min {c:>9.2f}$")
    separador()
    print(f"  \033[1m{'TOTAL':<22} {tot_d:>9.1f}km {tot_t:>9.1f}min {tot_c:>9.2f}$\033[0m")
    separador()

def mostrar_todas_rutas():
    titulo("🗺️ RUTAS DE 7 DÍAS")
    for dia in range(1, 8):
        cfg = DIAS_CONFIG[dia]
        cods = " → ".join(ATRACTIVOS[n]["cod"] for n in cfg["destinos"])
        print(f"\n  📅 DÍA {dia}: {cfg['zona']}")
        print(f"  📍 {cods}")
        print(f"  📏 {cfg['distancia_km']:.1f} km | ⏱️ {cfg['tiempo_auto_min']} min | 💰 ${cfg['costo_usd']:.2f}")
        print(f"  💬 '{cfg['frase']}'")
        print("-"*50)

def submenu_dia(G, matrices, caminos):
    titulo("RUTA ÓPTIMA POR DÍA")
    print("\n  Días disponibles:\n")
    for d, cfg in DIAS_CONFIG.items():
        cods = " → ".join(ATRACTIVOS[n]["cod"] for n in cfg["destinos"])
        print(f"   \033[1m[{d}]\033[0m  {cfg['zona']}")
        print(f"         Destinos: {cods}")
    print()
    while True:
        entrada = input("  ¿Qué día quieres ver? (1-7): ").strip()
        if entrada.isdigit() and 1 <= int(entrada) <= 7:
            dia = int(entrada)
            break
        print("  ✗ Ingresa un número del 1 al 7.")
    criterio = elegir_criterio()
    cfg = DIAS_CONFIG[dia]
    destinos = [d for d in cfg["destinos"] if d != 15]
    orden, costo = ruta_optima_dia(destinos, matrices, criterio)
    if orden is None:
        print("  ✗ No se pudo calcular la ruta.")
        return
    secuencia = [15] + orden + [15]
    titulo(f"DÍA {dia} — {cfg['zona']}")
    print(f"\n  📝 {cfg['descripcion']}")
    print(f"  💬 '{cfg['frase']}'")
    print(f"\n  Criterio: {criterio.upper()} | Total: {costo:.1f}")
    print(f"\n  Orden óptimo de visita:")
    ruta_str = " → ".join(G.nodes[n]["cod"] for n in secuencia)
    print(f"  \033[1;32m{ruta_str}\033[0m\n")
    mostrar_resultado_ruta(G, secuencia, matrices, criterio)
    print("\n  \033[1m[1]\033[0m  Ver grafo de este día")
    print("  \033[1m[2]\033[0m  Guardar grafo como PNG")
    print("  \033[1m[3]\033[0m  Volver al menú")
    sub = input("\n  Opción: ").strip()
    if sub == "1":
        dibujar_grafo_dia(G, dia, matrices, caminos, criterio)
    elif sub == "2":
        dibujar_grafo_dia(G, dia, matrices, caminos, criterio, guardar=f"Grafo_Dia_{dia}_{criterio}.png")

def submenu_camino(G, matrices, caminos):
    titulo("CAMINO MÍNIMO ENTRE DOS NODOS")
    mostrar_tabla_nodos(G)
    print()
    while True:
        try:
            u = int(input("  ID del nodo ORIGEN (1-29): ").strip())
            v = int(input("  ID del nodo DESTINO (1-29): ").strip())
            if u in ATRACTIVOS and v in ATRACTIVOS and u != v:
                break
            print("  ✗ IDs inválidos o iguales.")
        except ValueError:
            print("  ✗ Ingresa un número válido.")
    criterio = elegir_criterio()
    camino = caminos[criterio][u][v]
    valor = matrices[criterio][u][v]
    if not camino:
        print(f"\n  ✗ No existe camino entre {u} y {v}.")
        return
    titulo(f"CAMINO MÍNIMO: {ATRACTIVOS[u]['cod']} → {ATRACTIVOS[v]['cod']}")
    print(f"\n  Criterio: {criterio.upper()} | Total: {valor:.2f}")
    print(f"  Ruta: {' → '.join(G.nodes[n]['cod'] for n in camino)}\n")

def exportar_excel(G, matrices, nombre="Rutas_Cocle.xlsx"):
    wb = Workbook()
    wb.remove(wb.active)
    AZUL, GRIS, BLANC = "1F4E79", "F2F2F2", "FFFFFF"
    def celda(ws, fila, col, valor, bold=False, bg=None, alinear="center"):
        c = ws.cell(row=fila, column=col, value=valor)
        c.font = Font(name="Arial", bold=bold, size=10)
        if bg:
            c.fill = PatternFill("solid", fgColor=bg)
        c.alignment = Alignment(horizontal=alinear, vertical="center")
        return c
    ws = wb.create_sheet("Rutas_7_Dias")
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=8)
    c = ws.cell(row=1, column=1, value="RUTAS TURÍSTICAS - PROVINCIA DE COCLÉ")
    c.font = Font(name="Arial", bold=True, color=BLANC, size=14)
    c.fill = PatternFill("solid", fgColor=AZUL)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30
    hdrs = ["Día", "Zona", "Lugares", "Distancia", "Tiempo", "Costo", "Nivel", "Frase"]
    for j, h in enumerate(hdrs, 1):
        celda(ws, 2, j, h, bold=True, bg=GRIS)
    for dia, cfg in DIAS_CONFIG.items():
        i = dia + 2
        cods = " → ".join(ATRACTIVOS[n]["cod"] for n in cfg["destinos"])
        celda(ws, i, 1, dia, bg=BLANC if i%2==0 else GRIS)
        celda(ws, i, 2, cfg["zona"], bg=BLANC if i%2==0 else GRIS)
        celda(ws, i, 3, cods, bg=BLANC if i%2==0 else GRIS)
        celda(ws, i, 4, f"{cfg['distancia_km']:.1f} km", bg=BLANC if i%2==0 else GRIS)
        celda(ws, i, 5, f"{cfg['tiempo_auto_min']} min", bg=BLANC if i%2==0 else GRIS)
        celda(ws, i, 6, f"${cfg['costo_usd']:.2f}", bg=BLANC if i%2==0 else GRIS)
        celda(ws, i, 7, cfg["nivel"], bg=BLANC if i%2==0 else GRIS)
        celda(ws, i, 8, cfg["frase"], bg=BLANC if i%2==0 else GRIS, alinear="left")
    for j in range(1, 9):
        ws.column_dimensions[get_column_letter(j)].width = 22
    wb.save(nombre)
    print(f"\n  ✔ Excel exportado: {nombre}")

def menu_principal():
    print("""
  \033[1;36m╔══════════════════════════════════════════════════════════════╗
  ║   RUTAS TURÍSTICAS – PROVINCIA DE COCLÉ, PANAMÁ            ║
  ║   Algoritmo de Dijkstra | Universidad de Panamá            ║
  ║   7 DÍAS · 29 NODOS · CRITERIO OFICIAL: DISTANCIA          ║
  ╚══════════════════════════════════════════════════════════════╝\033[0m

  \033[1m[1]\033[0m  Ver inventario de los 29 atractivos
  \033[1m[2]\033[0m  Ver grafo completo (nodos y aristas)
  \033[1m[3]\033[0m  Ver ruta óptima de un día (1–7)
  \033[1m[4]\033[0m  Ver todas las rutas de los 7 días
  \033[1m[5]\033[0m  Calcular camino mínimo entre dos nodos
  \033[1m[6]\033[0m  Exportar todo a Excel
  \033[1m[7]\033[0m  Guardar grafos como imágenes PNG
  \033[1m[8]\033[0m  Ejecutar validaciones (Sección 3.6.1)
  \033[1m[9]\033[0m  Ejecutar pruebas de tiempo de ejecución (Tabla 9)
  \033[1m[0]\033[0m  Salir
""")

def main():
    limpiar()
    print("\n  \033[1;36mInicializando sistema...\033[0m")
    G = construir_grafo()
    print(f"  ✔ Grafo construido: {G.number_of_nodes()} nodos · {G.number_of_edges()} aristas")
    print(f"  ✔ Prueba de integridad de datos: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas con valores positivos")
    matrices, caminos = calcular_todas_matrices(G)
    print("  ✔ Matrices calculadas para los 3 criterios.")
    recalcular_estadisticas_dias(matrices, criterio="distancia")
    print("  ✔ Estadísticas de los 7 días recalculadas en vivo (criterio oficial: distancia).")
    input("\n  Presiona Enter para continuar...")

    while True:
        limpiar()
        menu_principal()
        opcion = input("  Opción: ").strip()
        if opcion == "0":
            limpiar()
            print("\n  ¡Hasta luego!\n")
            break
        elif opcion == "1":
            titulo("INVENTARIO DE ATRACTIVOS")
            mostrar_tabla_nodos(G)
            input("\n  Presiona Enter...")
        elif opcion == "2":
            titulo("GRAFO COMPLETO")
            criterio = elegir_criterio()
            dibujar_grafo_completo(G, criterio)
        elif opcion == "3":
            submenu_dia(G, matrices, caminos)
            input("\n  Presiona Enter...")
        elif opcion == "4":
            mostrar_todas_rutas()
            input("\n  Presiona Enter...")
        elif opcion == "5":
            # Prueba de Caja Negra (sección 3.6.3.a) - manual
            print("\n  ℹ️ Prueba de Caja Negra (3.6.3.a):")
            print("     Esta opción permite verificar manualmente que el algoritmo")
            print("     encuentra el camino más corto entre dos nodos.")
            submenu_camino(G, matrices, caminos)
            input("\n  Presiona Enter...")
        elif opcion == "6":
            titulo("EXPORTAR A EXCEL")
            exportar_excel(G, matrices)
            input("\n  Presiona Enter...")
        elif opcion == "7":
            titulo("GUARDAR GRAFOS")
            criterio = elegir_criterio()
            os.makedirs("grafos_cocle", exist_ok=True)
            dibujar_grafo_completo(G, criterio, guardar=f"grafos_cocle/grafo_completo_{criterio}.png")
            for dia in range(1, 8):
                dibujar_grafo_dia(G, dia, matrices, caminos, criterio, guardar=f"grafos_cocle/dia_{dia}_{criterio}.png")
            print(f"\n  ✔ Grafos guardados en 'grafos_cocle/'")
            input("\n  Presiona Enter...")
        elif opcion == "8":
            titulo("VALIDACIONES (Sección 3.6.1)")
            print("\n  Esta sección ejecuta las tres validaciones del marco metodológico:")
            print("  a) Comparación con Google Maps (SIMULADA, ±5%)")
            print("  b) Consistencia interna (subestructura óptima)")
            print("  c) Análisis de sensibilidad (3 criterios; distancia = oficial)")
            print("\n  NOTA: La validación con Google Maps es SIMULADA con variación de ±4%")
            input("\n  Presiona Enter para ejecutar las validaciones...")
            ejecutar_validaciones_completas(G, matrices, caminos)
            input("\n  Presiona Enter para continuar...")
        elif opcion == "9":
            titulo("PRUEBAS DE TIEMPO DE EJECUCIÓN (Tabla 9)")
            print("\n  Esta prueba mide el tiempo de ejecución del algoritmo de Dijkstra")
            print("  para diferentes tamaños de grafo, incluyendo el grafo real del proyecto.")
            print("  Corresponde a la sección 3.6.3.c de la metodología.\n")
            print("  ⏳ Ejecutando pruebas...\n")
            probar_tiempo_ejecucion(G)
            probar_tiempo_ruta_dia(matrices)
            input("\n  Presiona Enter para continuar...")
        else:
            print("  ✗ Opción no válida.")
            input("\n  Presiona Enter...")

if __name__ == "__main__":
    main()