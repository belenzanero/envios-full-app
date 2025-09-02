# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 14:49:23 2025

@author: bzane
"""

import streamlit as st
import pandas as pd
import altair as alt

# =============================
# Lógica de negocio (tal cual tu función)
# =============================

def costo_envio(distancia_km: float, ancho_m: float, largo_m: float, alto_m: float):
    """
    Calcula volumen (m³) y costo estimado interpolado según distancia y volumen.
    Devuelve (volumen_m3, costo_estimado, detalle_tramo)
    """
    v = ancho_m * largo_m * alto_m

    # Tabla: (dist_min, dist_max) -> [(vol_min, vol_max, precio_min, precio_max), ...]
    tarifas = {
        (0, 5): [
            (0, 0.05, 7805, 7805),
            (0.05, 0.10, 7805, 15610),
            (0.10, 0.20, 10965, 21929),
            (0.20, 0.30, 16446, 24669),
            (0.30, 0.50, 13888, 23146),
            (0.50, 1, 13932, 27864),
            (1, 2, 16889, 33778),
            (2, 5, 26002, 65005),
            (5, 10, 54675, 109350),
            (10, 20, 97880, 195760),
            (20, 35, 152560, 266980),
            (35, 50, 260820, 372600)
        ],
        (5, 20): [
            (0, 0.05, 9403, 9403),
            (0.05, 0.10, 9403, 18805),
            (0.10, 0.20, 12537, 25074),
            (0.20, 0.30, 20515, 30772),
            (0.30, 0.50, 19817, 33028),
            (0.50, 1, 19933, 39866),
            (1, 2, 24138, 48276),
            (2, 5, 36990, 92475),
            (5, 10, 78300, 156600),
            (10, 20, 140540, 281080),
            (20, 35, 218700, 382725),
            (35, 50, 374220, 534600)
        ],
        (20, 40): [
            (0, 0.05, 9403, 9403),
            (0.05, 0.10, 9403, 18805),
            (0.10, 0.20, 12537, 25074),
            (0.20, 0.30, 20515, 30772),
            (0.30, 0.50, 21797, 36329),
            (0.50, 1, 21911, 43821),
            (1, 2, 26595, 53190),
            (2, 5, 40798, 101995),
            (5, 10, 86265, 172530),
            (10, 20, 154980, 309960),
            (20, 35, 241120, 421960),
            (35, 50, 413910, 591300)
        ],
        (40, 60): [
            (0, 0.05, 9403, 9403),
            (0.05, 0.10, 9403, 18805),
            (0.10, 0.20, 12537, 25074),
            (0.20, 0.30, 20515, 30772),
            (0.30, 0.50, 23782, 39636),
            (0.50, 1, 23875, 47750),
            (1, 2, 28866, 57732),
            (2, 5, 43298, 108245),
            (5, 10, 90820, 181640),
            (10, 20, 168890, 337780),
            (20, 35, 261640, 457870),
            (35, 50, 449365, 641950)
        ],
        (60, 100): [
            (0, 0.05, 9403, 9403),
            (0.05, 0.10, 9403, 18805),
            (0.10, 0.20, 12537, 25074),
            (0.20, 0.30, 20515, 30772),
            (0.30, 0.50, 26038, 43397),
            (0.50, 1, 31978, 63955),
            (1, 2, 28866, 57732),
            (2, 5, 43298, 108245),
            (5, 10, 90820, 181640),
            (10, 20, 181640, 363280),
            (20, 35, 356340, 623595),
            (35, 50, 470505, 672150)
        ],
        (100, 150): [
            (0, 0.05, 9403, 9403),
            (0.05, 0.10, 9403, 18805),
            (0.10, 0.20, 12537, 25074),
            (0.20, 0.30, 20515, 30772),
            (0.30, 0.50, 26038, 43397),
            (0.50, 1, 33699, 67397),
            (1, 2, 28866, 57732),
            (2, 5, 43298, 108245),
            (5, 10, 90820, 181640),
            (10, 20, 181640, 363280),
            (20, 35, 356340, 623595),
            (35, 50, 470505, 672150)
        ],
        (150, 250): [
            (0, 0.05, 11398, 11398),
            (0.05, 0.10, 11398, 22795),
            (0.10, 0.20, 14528, 29056),
            (0.20, 0.30, 23542, 35313),
            (0.30, 0.50, 28692, 47820),
            (0.50, 1, 34220, 68440),
            (1, 2, 33540, 67080),
            (2, 5, 50420, 126050),
            (5, 10, 106100, 212200),
            (10, 20, 212200, 424400),
            (20, 35, 375400, 656950),
            (35, 50, 548450, 783500)
        ],
        (250, 400): [
            (0, 0.05, 11398, 11398),
            (0.05, 0.10, 11398, 22795),
            (0.10, 0.20, 14549, 29098),
            (0.20, 0.30, 23542, 35313),
            (0.30, 0.50, 28692, 47820),
            (0.50, 1, 44045, 88090),
            (1, 2, 36070, 72140),
            (2, 5, 54220, 135550),
            (5, 10, 114150, 228300),
            (10, 20, 228100, 456200),
            (20, 35, 447600, 783300),
            (35, 50, 589050, 841500)
        ],
        (400, 999999): [
            (0, 0.05, 11398, 11398),
            (0.05, 0.10, 11398, 22795),
            (0.10, 0.20, 14549, 29098),
            (0.20, 0.30, 23542, 35313),
            (0.30, 0.50, 28692, 47820),
            (0.50, 1, 44055, 88110),
            (1, 2, 44500, 89000),
            (2, 5, 66840, 167100),
            (5, 10, 140700, 281400),
            (10, 20, 281300, 562600),
            (20, 35, 551800, 965650),
            (35, 50, 726600, 1038000)
        ],
    }

    # Buscar tramo de distancia
    tramo_dist = None
    for r in tarifas:
        if r[0] <= distancia_km <= r[1]:
            tramo_dist = r
            break
    if tramo_dist is None:
        return v, None, "Sin tarifa para esa distancia"

    # Buscar tramo de volumen
    for vol_min, vol_max, p_min, p_max in tarifas[tramo_dist]:
        if vol_min <= v <= vol_max:
            if p_min == p_max:  # precio fijo
                return v, float(p_min), f"Dist {tramo_dist} km | Vol {vol_min}-{vol_max} m³ (precio fijo)"
            # Interpolación lineal dentro del tramo
            t = 0 if vol_max == vol_min else (v - vol_min) / (vol_max - vol_min)
            costo = p_min + t * (p_max - p_min)
            return v, float(round(costo, 2)), f"Dist {tramo_dist} km | Vol {vol_min}-{vol_max} m³"

    return v, None, "Sin tarifa para ese volumen"


def tabla_tarifas():
    """Devuelve el mismo diccionario de tarifas utilizado por costo_envio."""
    # Para reutilizar en la gráfica y tabla
    return costo_envio.__defaults__[0] if costo_envio.__defaults__ else None


# =============================
# App Streamlit
# =============================

st.set_page_config(page_title="Calculadora de costo de envío", page_icon="🚚", layout="centered")
st.title("🚚 Calculadora de costo de envío")
st.caption("Ingresá medidas en **metros** y distancia en **km**. El cálculo interpola linealmente el precio dentro de cada tramo de volumen.")

with st.sidebar:
    st.header("Parámetros")
    distancia = st.number_input("Distancia (km)", min_value=0.0, value=10.0, step=1.0, help="Distancia total del envío")
    col1, col2, col3 = st.columns(3)
    with col1:
        ancho = st.number_input("Ancho (m)", min_value=0.0, value=0.3, step=0.01)
    with col2:
        largo = st.number_input("Largo (m)", min_value=0.0, value=0.3, step=0.01)
    with col3:
        alto = st.number_input("Alto (m)", min_value=0.0, value=0.3, step=0.01)

    calcular = st.button("Calcular")

if calcular:
    if any(x <= 0 for x in [distancia, ancho, largo, alto]):
        st.error("Ingresá valores **mayores a cero** para todos los campos.")
    else:
        vol, costo, detalle = costo_envio(distancia, ancho, largo, alto)
        st.subheader("Resultado")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Volumen (m³)", f"{vol:,.4f}".replace(",", "X").replace(".", ",").replace("X", "."))
        with c2:
            if costo is not None:
                st.metric("Costo estimado", f"$ {costo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            else:
                st.metric("Costo estimado", "No disponible")
        with c3:
            st.metric("Distancia (km)", f"{distancia:,.0f}".replace(",", "."))

        if costo is not None:
            st.success(f"Detalle: {detalle}")
        else:
            st.warning(detalle)

        # =============================
        # Curva de precios por volumen para el tramo de distancia elegido
        # =============================
        st.divider()
        st.subheader("Curva de precio por volumen para esta distancia")

        # Recalcular tramo de distancia y segmentos para graficar
        # (copiamos la parte de detección de tramo para obtener los segmentos)
        # Tomamos las tarifas desde la función
        # (accedemos al objeto dentro de la función copiándolo aquí para simplicidad)
        tarifas = {
            (0, 5): [
                (0, 0.05, 7805, 7805), (0.05, 0.10, 7805, 15610), (0.10, 0.20, 10965, 21929),
                (0.20, 0.30, 16446, 24669), (0.30, 0.50, 13888, 23146), (0.50, 1, 13932, 27864),
                (1, 2, 16889, 33778), (2, 5, 26002, 65005), (5, 10, 54675, 109350), (10, 20, 97880, 195760),
                (20, 35, 152560, 266980), (35, 50, 260820, 372600)
            ],
            (5, 20): [
                (0, 0.05, 9403, 9403), (0.05, 0.10, 9403, 18805), (0.10, 0.20, 12537, 25074),
                (0.20, 0.30, 20515, 30772), (0.30, 0.50, 19817, 33028), (0.50, 1, 19933, 39866),
                (1, 2, 24138, 48276), (2, 5, 36990, 92475), (5, 10, 78300, 156600), (10, 20, 140540, 281080),
                (20, 35, 218700, 382725), (35, 50, 374220, 534600)
            ],
            (20, 40): [
                (0, 0.05, 9403, 9403), (0.05, 0.10, 9403, 18805), (0.10, 0.20, 12537, 25074),
                (0.20, 0.30, 20515, 30772), (0.30, 0.50, 21797, 36329), (0.50, 1, 21911, 43821),
                (1, 2, 26595, 53190), (2, 5, 40798, 101995), (5, 10, 86265, 172530), (10, 20, 154980, 309960),
                (20, 35, 241120, 421960), (35, 50, 413910, 591300)
            ],
            (40, 60): [
                (0, 0.05, 9403, 9403), (0.05, 0.10, 9403, 18805), (0.10, 0.20, 12537, 25074),
                (0.20, 0.30, 20515, 30772), (0.30, 0.50, 23782, 39636), (0.50, 1, 23875, 47750),
                (1, 2, 28866, 57732), (2, 5, 43298, 108245), (5, 10, 90820, 181640), (10, 20, 168890, 337780),
                (20, 35, 261640, 457870), (35, 50, 449365, 641950)
            ],
            (60, 100): [
                (0, 0.05, 9403, 9403), (0.05, 0.10, 9403, 18805), (0.10, 0.20, 12537, 25074),
                (0.20, 0.30, 20515, 30772), (0.30, 0.50, 26038, 43397), (0.50, 1, 31978, 63955),
                (1, 2, 28866, 57732), (2, 5, 43298, 108245), (5, 10, 90820, 181640), (10, 20, 181640, 363280),
                (20, 35, 356340, 623595), (35, 50, 470505, 672150)
            ],
            (100, 150): [
                (0, 0.05, 9403, 9403), (0.05, 0.10, 9403, 18805), (0.10, 0.20, 12537, 25074),
                (0.20, 0.30, 20515, 30772), (0.30, 0.50, 26038, 43397), (0.50, 1, 33699, 67397),
                (1, 2, 28866, 57732), (2, 5, 43298, 108245), (5, 10, 90820, 181640), (10, 20, 181640, 363280),
                (20, 35, 356340, 623595), (35, 50, 470505, 672150)
            ],
            (150, 250): [
                (0, 0.05, 11398, 11398), (0.05, 0.10, 11398, 22795), (0.10, 0.20, 14528, 29056),
                (0.20, 0.30, 23542, 35313), (0.30, 0.50, 28692, 47820), (0.50, 1, 34220, 68440),
                (1, 2, 33540, 67080), (2, 5, 50420, 126050), (5, 10, 106100, 212200), (10, 20, 212200, 424400),
                (20, 35, 375400, 656950), (35, 50, 548450, 783500)
            ],
            (250, 400): [
                (0, 0.05, 11398, 11398), (0.05, 0.10, 11398, 22795), (0.10, 0.20, 14549, 29098),
                (0.20, 0.30, 23542, 35313), (0.30, 0.50, 28692, 47820), (0.50, 1, 44045, 88090),
                (1, 2, 36070, 72140), (2, 5, 54220, 135550), (5, 10, 114150, 228300), (10, 20, 228100, 456200),
                (20, 35, 447600, 783300), (35, 50, 589050, 841500)
            ],
            (400, 999999): [
                (0, 0.05, 11398, 11398), (0.05, 0.10, 11398, 22795), (0.10, 0.20, 14549, 29098),
                (0.20, 0.30, 23542, 35313), (0.30, 0.50, 28692, 47820), (0.50, 1, 44055, 88110),
                (1, 2, 44500, 89000), (2, 5, 66840, 167100), (5, 10, 140700, 281400), (10, 20, 281300, 562600),
                (20, 35, 551800, 965650), (35, 50, 726600, 1038000)
            ],
        }

        tramo_dist = None
        for r in tarifas:
            if r[0] <= distancia <= r[1]:
                tramo_dist = r
                break

        if tramo_dist is None:
            st.info("No hay tarifas para esta distancia.")
        else:
            # Construimos una curva piecewise a partir de los tramos de volumen
            puntos = []
            for vol_min, vol_max, p_min, p_max in tarifas[tramo_dist]:
                # agregamos ambos extremos del tramo
                puntos.append((vol_min, p_min))
                puntos.append((vol_max, p_max))
            # Ordenar y deduplicar
            puntos = sorted(set(puntos), key=lambda x: x[0])
            df = pd.DataFrame(puntos, columns=["volumen_m3", "precio"])

            chart = (
                alt.Chart(df)
                .mark_line()
                .encode(x=alt.X("volumen_m3", title="Volumen (m³)"), y=alt.Y("precio", title="Precio ($)"))
            )
            # Punto actual
            punto_actual = pd.DataFrame({"volumen_m3": [vol], "precio": [costo if costo is not None else None]})
            puntos_layer = alt.Chart(punto_actual).mark_point(size=100).encode(x="volumen_m3", y="precio")

            st.altair_chart(chart + puntos_layer, use_container_width=True)

            with st.expander("Ver tabla de segmentos de volumen y precios"):
                segs = pd.DataFrame(
                    tarifas[tramo_dist],
                    columns=["vol_min", "vol_max", "precio_min", "precio_max"],
                )
                st.dataframe(segs, use_container_width=True)

# =============================
# Ayuda rápida
# =============================
with st.expander("Cómo usar"):
    st.markdown(
        """
        1. Cargá la **distancia** en km y las medidas del bulto en **metros**.
        2. Tocá **Calcular**.
        3. Verás el **volumen**, el **costo estimado** y el **tramo** aplicado.
        4. Abajo podés explorar la **curva de precio vs. volumen** para la distancia elegida.
        """
    )

st.caption("Made with ❤️ en Streamlit. Datos de tarifas provistos en el código.")
