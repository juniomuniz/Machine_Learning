import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dataclasses import dataclass
from datetime import datetime, date
import requests
import html as html_lib
import yfinance as yf

# ─────────────────────────────
# 🔑 CHAVE DA API — EDITE APENAS AQUI
# ─────────────────────────────
OPENWEATHER_API_KEY = "573cc9633e26c55989dfd60069cd306f"
# Chave gratuita em: https://openweathermap.org/api
# Plano Free: 1.000 chamadas/dia | Forecast 5 dias incluso

# ─────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────
st.set_page_config(
    page_title="🚢 Porto Pricing Tool",
    page_icon="🚢",
    layout="wide"
)

# ─────────────────────────────
# CSS GLOBAL
# ─────────────────────────────
st.markdown("""
<style>
.stApp {
    background-color: #f0f4f8;
    background-image: none;
}
div[data-testid="stSidebarContent"] {
    background: #ffffff;
    border-right: 2px solid #bbdefb;
}
.stSelectbox label,
.stSlider label,
.stNumberInput label,
.stTextInput label,
.stDateInput label,
.stToggle label {
    color: #1565C0 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}
.hero-banner {
    background: linear-gradient(
        135deg,#1565C0 0%,#1E88E5 60%,#42A5F5 100%
    );
    border-radius: 20px;
    padding: 50px 40px 40px 40px;
    margin-bottom: 24px;
    box-shadow: 0 6px 24px rgba(21,101,192,0.25);
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.25);
    border: 1px solid rgba(255,255,255,0.6);
    color: #ffffff;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px 4px 4px 0;
}
.porto-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 25px;
    padding: 5px 14px;
    font-size: 13px;
    color: #ffffff;
    font-weight: 600;
}
.metric-card {
    background: #ffffff;
    padding: 20px;
    border-radius: 14px;
    border: 2px solid #bbdefb;
    text-align: center;
    margin: 5px;
    box-shadow: 0 4px 12px rgba(21,101,192,0.12);
}
.metric-value {
    font-size: 32px;
    font-weight: 800;
    color: #1565C0;
}
.metric-label {
    font-size: 14px;
    font-weight: 600;
    color: #37474f;
    margin-top: 6px;
}
.info-box {
    background: #e3f2fd;
    padding: 16px;
    border-radius: 10px;
    font-size: 15px;
    color: #1a237e;
    font-weight: 500;
    border: 1px solid #90caf9;
    margin-bottom: 10px;
}
.custo-card {
    background: #ffffff;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #1E88E5;
    margin: 8px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.custo-card-green  { border-left: 5px solid #2e7d32 !important; }
.custo-card-yellow { border-left: 5px solid #f57f17 !important; }
.custo-card-red    { border-left: 5px solid #c62828 !important; }
.total-card {
    background: linear-gradient(135deg,#1565C0,#0d47a1);
    padding: 28px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(21,101,192,0.35);
    margin: 18px 0;
}
.clima-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 16px 20px;
    border: 2px solid #bbdefb;
    box-shadow: 0 4px 12px rgba(21,101,192,0.10);
    margin-bottom: 8px;
}
.clima-card-alerta {
    border: 2px solid #f57f17;
    background: #fff8e1;
}
.clima-card-perigo {
    border: 2px solid #c62828;
    background: #ffebee;
}
.clima-cidade {
    font-size: 14px;
    font-weight: 700;
    color: #1565C0;
    margin-bottom: 6px;
}
.clima-temp {
    font-size: 36px;
    font-weight: 900;
    color: #1a237e;
    line-height: 1;
}
.clima-desc {
    font-size: 13px;
    color: #546e7a;
    margin-top: 4px;
    text-transform: capitalize;
}
.clima-detalhe {
    font-size: 12px;
    color: #78909c;
    margin-top: 8px;
    border-top: 1px solid #e3f2fd;
    padding-top: 8px;
}
.clima-aviso {
    background: #fff3e0;
    border: 1px solid #f57f17;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    color: #e65100;
    margin-top: 6px;
    font-weight: 600;
}
.cambio-mini-box {
    background: #f8fafb;
    border-radius: 10px;
    padding: 10px 12px;
    border: 1px solid #e0e0e0;
    margin-bottom: 6px;
}
.cambio-em-uso {
    background: #e3f2fd;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    margin-top: 8px;
}
.stTabs [data-baseweb="tab-list"] {
    background: #e3f2fd;
    border-radius: 12px;
    padding: 5px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: #ffffff;
    border-radius: 8px;
    color: #1565C0;
    font-weight: 700;
    font-size: 15px;
    padding: 10px 20px;
    border: 1px solid #90caf9;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(
        135deg,#1565C0,#1E88E5
    ) !important;
    color: white !important;
    border-color: transparent !important;
}
h2, h3, h4 { color: #0d47a1 !important; }
p, li       { font-size: 15px; color: #1a237e; }
hr          { border-color: #bbdefb !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────
# DATACLASSES
# ─────────────────────────────
@dataclass
class Caixa:
    nome: str
    comp: float
    larg: float
    alt: float
    peso: float
    cor: str
    cor_borda: str

@dataclass
class Container:
    tipo: str
    comp: float
    larg: float
    alt: float
    peso_max: float


# ─────────────────────────────
# DADOS
# ─────────────────────────────
CONTAINERS = {
    "📦 Container 20ft":
        Container("20ft",     589, 235, 239, 28200),
    "📦 Container 40ft":
        Container("40ft",    1203, 235, 239, 26700),
    "📦 Container 40ft HC":
        Container("40ft HC", 1203, 235, 269, 26580),
}

CAIXAS = {
    "🔴 Pequena (30×20×15cm)":
        Caixa("Pequena", 30, 20, 15,  2.5,
              "rgba(255,100,100,0.8)", "#ff4444"),
    "🔵 Média (50×40×30cm)":
        Caixa("Média",   50, 40, 30,  8.0,
              "rgba(100,180,255,0.8)", "#4488ff"),
    "🟢 Grande (80×60×50cm)":
        Caixa("Grande",  80, 60, 50, 20.0,
              "rgba(100,220,150,0.8)", "#44cc88"),
    "🟡 XL (100×80×70cm)":
        Caixa("XL",     100, 80, 70, 35.0,
              "rgba(255,220,100,0.8)", "#ffcc44"),
    "🟣 Custom":
        Caixa("Custom",  40, 30, 25,  5.0,
              "rgba(200,100,255,0.8)", "#cc44ff"),
}

TAXAS_PORTUARIAS = {
    "THC - Terminal Handling Charge":
        {"20ft": 650,  "40ft": 850,  "40ft HC": 900},
    "BL Fee - Bill of Lading":
        {"20ft": 150,  "40ft": 150,  "40ft HC": 150},
    "ISPS - Segurança Portuária":
        {"20ft":  45,  "40ft":  55,  "40ft HC":  55},
    "Capatazia":
        {"20ft": 380,  "40ft": 520,  "40ft HC": 560},
    "Liberação do Container":
        {"20ft": 220,  "40ft": 280,  "40ft HC": 280},
}

SURCHARGES = {
    "GRI - General Rate Increase":
        {"20ft": 300, "40ft": 400, "40ft HC": 450},
    "BAF - Bunker Adjustment Factor":
        {"20ft": 200, "40ft": 280, "40ft HC": 280},
    "PSS - Peak Season Surcharge":
        {"20ft": 150, "40ft": 200, "40ft HC": 200},
    "D/O - Delivery Order":
        {"20ft":  80, "40ft":  80, "40ft HC":  80},
    "VGM - Verificação Massa Bruta":
        {"20ft":  45, "40ft":  45, "40ft HC":  45},
}

ALIQUOTAS_NCM = {
    "Eletrônicos":
        {"II": 14.0, "IPI": 10.0, "PIS": 2.1, "COFINS": 9.65},
    "Vestuário":
        {"II": 20.0, "IPI":  0.0, "PIS": 2.1, "COFINS": 9.65},
    "Alimentos":
        {"II": 10.0, "IPI":  0.0, "PIS": 2.1, "COFINS": 9.65},
    "Máquinas/Equipamentos":
        {"II": 12.0, "IPI":  5.0, "PIS": 2.1, "COFINS": 9.65},
    "Químicos":
        {"II":  8.0, "IPI":  0.0, "PIS": 2.1, "COFINS": 9.65},
    "Automóveis":
        {"II": 35.0, "IPI": 25.0, "PIS": 2.1, "COFINS": 9.65},
    "Personalizado":
        {"II":  0.0, "IPI":  0.0, "PIS": 2.1, "COFINS": 9.65},
}

ARMADORES_REFERENCIA = {
    "Maersk":      {"20ft": 2200, "40ft": 3100, "40ft HC": 3300},
    "MSC":         {"20ft": 2100, "40ft": 3000, "40ft HC": 3200},
    "Hapag-Lloyd": {"20ft": 2300, "40ft": 3200, "40ft HC": 3400},
    "CMA CGM":     {"20ft": 2150, "40ft": 3050, "40ft HC": 3250},
    "Evergreen":   {"20ft": 2050, "40ft": 2900, "40ft HC": 3100},
    "ONE":         {"20ft": 2000, "40ft": 2850, "40ft HC": 3050},
}


# ─────────────────────────────
# CLIMA — EMOJIS E AVISOS
# ─────────────────────────────
CLIMA_EMOJI = {
    "thunderstorm": "⛈️",
    "drizzle":      "🌦️",
    "rain":         "🌧️",
    "snow":         "❄️",
    "mist":         "🌫️",
    "fog":          "🌫️",
    "haze":         "🌫️",
    "clear":        "☀️",
    "clouds":       "☁️",
    "smoke":        "💨",
    "dust":         "💨",
    "tornado":      "🌪️",
}

CLIMA_AVISOS = {
    "thunderstorm": "⚠️ Tempestade — possível paralisação portuária",
    "snow":         "⚠️ Neve — verifique rotas rodoviárias",
    "tornado":      "🚨 Tornado — operações suspensas",
    "mist":         "⚠️ Neblina — visibilidade reduzida no porto",
    "fog":          "⚠️ Névoa densa — visibilidade reduzida",
    "rain":         "ℹ️ Chuva — monitore guindaste e carga a granel",
    "drizzle":      "ℹ️ Garoa — atenção a carga sensível à umidade",
}

PERIODO_EMOJI = {
    "madrugada": "🌙",
    "manha":     "🌅",
    "tarde":     "☀️",
    "noite":     "🌆",
}

def get_periodo_emoji(hora: int) -> str:
    if 0  <= hora < 6:  return "🌙"
    if 6  <= hora < 12: return "🌅"
    if 12 <= hora < 18: return "☀️"
    return "🌆"


# ─────────────────────────────
# CLIMA ATUAL
# ─────────────────────────────
@st.cache_data(ttl=1800)
def get_clima(cidade: str, api_key: str = OPENWEATHER_API_KEY):
    if not api_key or len(api_key) < 10:
        return None, "API Key não configurada no código"
    try:
        url = (
            "http://api.openweathermap.org/data/2.5/weather"
            f"?q={cidade}&appid={api_key}"
            "&units=metric&lang=pt_br"
        )
        resp = requests.get(url, timeout=5)
        if resp.status_code == 401:
            return None, "API Key inválida"
        if resp.status_code == 404:
            return None, f"Cidade '{cidade}' não encontrada"
        resp.raise_for_status()
        d           = resp.json()
        condicao_id = d["weather"][0]["main"].lower()
        return {
            "cidade":      d["name"],
            "pais":        d["sys"]["country"],
            "temp":        d["main"]["temp"],
            "temp_min":    d["main"]["temp_min"],
            "temp_max":    d["main"]["temp_max"],
            "sensacao":    d["main"]["feels_like"],
            "umidade":     d["main"]["humidity"],
            "descricao":   d["weather"][0]["description"],
            "condicao_id": condicao_id,
            "emoji":       CLIMA_EMOJI.get(condicao_id, "🌡️"),
            "aviso":       CLIMA_AVISOS.get(condicao_id, ""),
            "vento_ms":    d["wind"]["speed"],
            "vento_kmh":   round(d["wind"]["speed"] * 3.6, 1),
            "visib_km":    round(d.get("visibility", 10000) / 1000, 1),
            "pressao":     d["main"]["pressure"],
        }, ""
    except requests.exceptions.Timeout:
        return None, "Timeout > 5s"
    except Exception as e:
        return None, f"Erro: {e}"


def render_clima_card(dados, titulo, cidade_input):
    if dados is None:
        st.markdown(f"""
        <div class='clima-card'>
            <div class='clima-cidade'>{titulo}</div>
            <div style='color:#90a4ae;font-size:13px;padding:8px 0;'>
                🌐 "{cidade_input}"<br>
                ⚠️ Dados indisponíveis — verifique a API Key
                ou o nome da cidade.
            </div>
        </div>""", unsafe_allow_html=True)
        return

    card_class = "clima-card"
    if dados["condicao_id"] in ["thunderstorm", "tornado"]:
        card_class = "clima-card clima-card-perigo"
    elif dados["condicao_id"] in ["rain","snow","mist","fog","drizzle"]:
        card_class = "clima-card clima-card-alerta"

    aviso_html = (
        f"<div class='clima-aviso'>{dados['aviso']}</div>"
        if dados["aviso"] else ""
    )
    st.markdown(f"""
    <div class='{card_class}'>
        <div class='clima-cidade'>
            {titulo} &nbsp;·&nbsp; {dados['cidade']}, {dados['pais']}
        </div>
        <div style='display:flex;align-items:flex-end;gap:12px;'>
            <div style='font-size:44px;line-height:1;'>{dados['emoji']}</div>
            <div>
                <div class='clima-temp'>{dados['temp']:.0f}°C</div>
                <div class='clima-desc'>{dados['descricao']}</div>
            </div>
        </div>
        <div class='clima-detalhe'>
            🌡️ Mín {dados['temp_min']:.0f}° · Máx {dados['temp_max']:.0f}°
            &nbsp;|&nbsp; 🤔 Sensação {dados['sensacao']:.0f}°C
            &nbsp;|&nbsp; 💧 Umidade {dados['umidade']}%<br>
            💨 Vento {dados['vento_kmh']} km/h
            &nbsp;|&nbsp; 👁️ Visibilidade {dados['visib_km']} km
            &nbsp;|&nbsp; 📊 Pressão {dados['pressao']} hPa
        </div>
        {aviso_html}
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────
# FORECAST 5 DIAS
# ─────────────────────────────
@st.cache_data(ttl=3600)
def get_forecast_5dias(cidade: str, api_key: str = OPENWEATHER_API_KEY):
    if not api_key or len(api_key) < 10:
        return None, "API Key não configurada"
    try:
        url = (
            "http://api.openweathermap.org/data/2.5/forecast"
            f"?q={cidade}&appid={api_key}"
            "&units=metric&lang=pt_br&cnt=40"
        )
        resp = requests.get(url, timeout=8)
        if resp.status_code == 401:
            return None, "API Key inválida"
        if resp.status_code == 404:
            return None, f"Cidade '{cidade}' não encontrada"
        resp.raise_for_status()

        dados       = resp.json()
        nome_cidade = dados["city"]["name"]
        pais        = dados["city"]["country"]
        lista       = dados["list"]

        por_dia = {}
        for item in lista:
            dt         = datetime.fromtimestamp(item["dt"])
            dia_key    = dt.strftime("%Y-%m-%d")
            dia_label  = dt.strftime("%d/%m")
            dia_semana = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"][dt.weekday()]
            hora       = dt.hour
            cond_id    = item["weather"][0]["main"].lower()

            if dia_key not in por_dia:
                por_dia[dia_key] = {
                    "label":      dia_label,
                    "semana":     dia_semana,
                    "temps":      [],
                    "umidades":   [],
                    "ventos_kmh": [],
                    "descricoes": [],
                    "condicoes":  [],
                    "periodos":   [],
                }

            por_dia[dia_key]["temps"].append(item["main"]["temp"])
            por_dia[dia_key]["umidades"].append(item["main"]["humidity"])
            por_dia[dia_key]["ventos_kmh"].append(
                round(item["wind"]["speed"] * 3.6, 1)
            )
            por_dia[dia_key]["descricoes"].append(
                item["weather"][0]["description"]
            )
            por_dia[dia_key]["condicoes"].append(cond_id)
            por_dia[dia_key]["periodos"].append({
                "hora":     dt.strftime("%H:%M"),
                "hora_int": hora,
                "temp":     item["main"]["temp"],
                "desc":     item["weather"][0]["description"],
                "cond":     cond_id,
                "emoji":    CLIMA_EMOJI.get(cond_id, "🌡️"),
                "periodo":  get_periodo_emoji(hora),
                "umidade":  item["main"]["humidity"],
                "vento":    round(item["wind"]["speed"] * 3.6, 1),
                "chuva_mm": item.get("rain", {}).get("3h", 0.0),
                "pop":      round(item.get("pop", 0) * 100),
            })

        resumo = {}
        for dia_key, d in por_dia.items():
            cond_freq = max(set(d["condicoes"]), key=d["condicoes"].count)
            resumo[dia_key] = {
                "label":       d["label"],
                "semana":      d["semana"],
                "temp_max":    max(d["temps"]),
                "temp_min":    min(d["temps"]),
                "umidade":     round(sum(d["umidades"]) / len(d["umidades"])),
                "vento":       round(max(d["ventos_kmh"]), 1),
                "descricao":   max(set(d["descricoes"]),
                                   key=d["descricoes"].count),
                "condicao":    cond_freq,
                "emoji":       CLIMA_EMOJI.get(cond_freq, "🌡️"),
                "aviso":       CLIMA_AVISOS.get(cond_freq, ""),
                "chuva_total": sum(p["chuva_mm"] for p in d["periodos"]),
                "pop_max":     max(p["pop"] for p in d["periodos"]),
                "periodos":    d["periodos"],
                "cidade":      nome_cidade,
                "pais":        pais,
            }
        return resumo, ""

    except requests.exceptions.Timeout:
        return None, "Timeout > 8s"
    except Exception as e:
        return None, f"Erro: {e}"


def render_forecast_cards(resumo: dict, titulo: str):
    if not resumo:
        st.warning(f"⚠️ Forecast indisponível para {titulo}")
        return

    dias        = list(resumo.values())
    cidade_nome = dias[0]["cidade"] if dias else titulo

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1565C0,#1E88E5);
                border-radius:14px;padding:14px 20px;margin-bottom:14px;'>
        <span style='color:#ffffff;font-size:17px;font-weight:800;'>
            🌤️ Previsão 5 Dias · {titulo}
        </span>
        <span style='color:#B3D9F7;font-size:13px;margin-left:10px;'>
            {cidade_nome}, {dias[0]['pais'] if dias else ''}
        </span>
    </div>""", unsafe_allow_html=True)

    cols = st.columns(len(dias))
    for i, (dia_key, dia) in enumerate(resumo.items()):
        bg_cor = "#ffffff"; borda = "#bbdefb"
        if dia["condicao"] in ["thunderstorm","tornado"]:
            bg_cor = "#ffebee"; borda = "#c62828"
        elif dia["condicao"] in ["rain","snow","drizzle"]:
            bg_cor = "#fff8e1"; borda = "#f57f17"

        aviso_html = ""
        if dia["aviso"]:
            aviso_html = f"""
            <div style='background:#fff3e0;border:1px solid #f57f17;
                        border-radius:6px;padding:5px 8px;
                        font-size:10px;color:#e65100;
                        margin-top:6px;font-weight:600;'>
                {dia['aviso']}
            </div>"""

        chuva_html = ""
        if dia["chuva_total"] > 0:
            chuva_html = f"""
            <div style='color:#1565C0;font-size:11px;margin-top:3px;'>
                🌧️ {dia['chuva_total']:.1f} mm · {dia['pop_max']}% prob.
            </div>"""

        with cols[i]:
            st.markdown(f"""
            <div style='background:{bg_cor};border:2px solid {borda};
                        border-radius:14px;padding:14px 10px;
                        text-align:center;
                        box-shadow:0 3px 10px rgba(21,101,192,0.10);'>
                <div style='font-size:12px;font-weight:700;
                            color:#546e7a;'>{dia['semana']}</div>
                <div style='font-size:13px;font-weight:700;
                            color:#1a237e;'>{dia['label']}</div>
                <div style='font-size:36px;margin:6px 0;
                            line-height:1;'>{dia['emoji']}</div>
                <div style='font-size:22px;font-weight:900;
                            color:#1565C0;'>{dia['temp_max']:.0f}°</div>
                <div style='font-size:13px;color:#78909c;'>
                    ↓ {dia['temp_min']:.0f}°C</div>
                <div style='font-size:11px;color:#546e7a;
                            margin-top:4px;text-transform:capitalize;'>
                    {dia['descricao']}</div>
                <div style='font-size:11px;color:#78909c;margin-top:4px;'>
                    💧{dia['umidade']}% · 💨{dia['vento']}km/h</div>
                {chuva_html}
                {aviso_html}
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    labels_dias = [f"{d['semana']}\n{d['label']}" for d in dias]
    temps_max   = [d["temp_max"]    for d in dias]
    temps_min   = [d["temp_min"]    for d in dias]
    chuvas      = [d["chuva_total"] for d in dias]

    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(
        x=labels_dias, y=temps_max,
        name="Máxima",
        mode="lines+markers+text",
        line=dict(color="#e53935", width=3),
        marker=dict(size=9, color="#e53935"),
        text=[f"{v:.0f}°" for v in temps_max],
        textposition="top center",
        textfont=dict(color="#e53935", size=12),
        fill="tonexty",
        fillcolor="rgba(229,57,53,0.08)"
    ))
    fig_temp.add_trace(go.Scatter(
        x=labels_dias, y=temps_min,
        name="Mínima",
        mode="lines+markers+text",
        line=dict(color="#1565C0", width=3),
        marker=dict(size=9, color="#1565C0"),
        text=[f"{v:.0f}°" for v in temps_min],
        textposition="bottom center",
        textfont=dict(color="#1565C0", size=12),
    ))
    if any(c > 0 for c in chuvas):
        fig_temp.add_trace(go.Bar(
            x=labels_dias, y=chuvas,
            name="Chuva (mm)",
            marker_color="rgba(21,101,192,0.25)",
            yaxis="y2",
        ))
    fig_temp.update_layout(
        paper_bgcolor="rgba(240,244,248,0.5)",
        plot_bgcolor="rgba(240,244,248,0.5)",
        font=dict(color="#1a237e"),
        height=260,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor="rgba(21,101,192,0.15)", color="#1a237e"),
        yaxis=dict(
            title="Temperatura (°C)",
            gridcolor="rgba(21,101,192,0.15)",
            color="#1a237e"
        ),
        yaxis2=dict(
            title="Chuva (mm)", overlaying="y",
            side="right", color="#1565C0", showgrid=False
        ),
        legend=dict(
            bgcolor="rgba(240,244,248,0.8)",
            font=dict(color="#1a237e", size=12)
        ),
        hovermode="x unified"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    with st.expander("🕐 Ver horários detalhados (intervalos de 3h)"):
        for dia_key, dia in resumo.items():
            st.markdown(f"**📅 {dia['semana']} {dia['label']}**")
            n_cols = min(len(dia["periodos"]), 8)
            if n_cols == 0:
                continue
            p_cols = st.columns(n_cols)
            for j, p in enumerate(dia["periodos"]):
                cor_pop = (
                    "#e53935" if p["pop"] >= 70
                    else "#f57f17" if p["pop"] >= 40
                    else "#43a047"
                )
                with p_cols[j % n_cols]:
                    st.markdown(f"""
                    <div style='background:#f8fafb;border-radius:10px;
                                padding:8px 6px;text-align:center;
                                border:1px solid #e0e0e0;font-size:12px;'>
                        <div>{p['periodo']} <b>{p['hora']}</b></div>
                        <div style='font-size:22px;'>{p['emoji']}</div>
                        <div style='font-weight:700;color:#1565C0;
                                    font-size:14px;'>{p['temp']:.0f}°C</div>
                        <div style='color:#78909c;font-size:10px;
                                    text-transform:capitalize;'>
                            {p['desc']}</div>
                        <div style='color:#546e7a;font-size:10px;
                                    margin-top:3px;'>
                            💧{p['umidade']}%</div>
                        <div style='color:{cor_pop};font-size:10px;
                                    font-weight:600;'>
                            🌧️ {p['pop']}%</div>
                        <div style='color:#78909c;font-size:10px;'>
                            💨{p['vento']}km/h</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown("---")


# ─────────────────────────────
# YAHOO FINANCE
# ─────────────────────────────
@st.cache_data(ttl=300)
def get_cambio_yahoo():
    try:
        ticker = yf.Ticker("USDBRL=X")
        hist   = ticker.history(period="1d")
        if hist.empty:
            return 5.20, "Sem dados — Yahoo Finance", False
        preco = float(hist["Close"].iloc[-1])
        return preco, "Yahoo Finance · yfinance (USDBRL=X)", True
    except Exception as e:
        return 5.20, f"Erro yfinance: {e}", False


@st.cache_data(ttl=3600)
def get_historico_cambio():
    try:
        ticker = yf.Ticker("USDBRL=X")
        hist   = ticker.history(period="1mo")
        if hist.empty:
            return pd.DataFrame(), False
        df = hist[["Close"]].copy().reset_index()
        df.columns = ["Data", "Fechamento"]
        try:
            df["Data"] = df["Data"].dt.tz_localize(None)
        except TypeError:
            df["Data"] = df["Data"].dt.tz_convert(None)
        return df, True
    except Exception:
        return pd.DataFrame(), False


def criar_mini_grafico(df_hist):
    if df_hist.empty:
        return None, 0.0
    primeiro = float(df_hist["Fechamento"].iloc[0])
    ultimo   = float(df_hist["Fechamento"].iloc[-1])
    variacao = ((ultimo - primeiro) / primeiro) * 100
    cor_linha = "#2e7d32" if variacao >= 0 else "#c62828"
    cor_fill  = (
        "rgba(46,125,50,0.12)" if variacao >= 0
        else "rgba(198,40,40,0.12)"
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_hist["Data"], y=df_hist["Fechamento"],
        mode="lines",
        line=dict(color=cor_linha, width=2),
        fill="tozeroy", fillcolor=cor_fill,
        hovertemplate="%{x|%d/%m}<br><b>R$ %{y:.4f}</b><extra></extra>"
    ))
    fig.add_hline(
        y=ultimo, line_dash="dot",
        line_color=cor_linha, line_width=1, opacity=0.5
    )
    fig.update_layout(
        height=110,
        margin=dict(l=0, r=0, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(
            visible=True, showgrid=False,
            tickfont=dict(size=9, color="#546e7a"),
            tickformat=",.3f", side="right",
        ),
        showlegend=False,
        hovermode="x unified",
    )
    return fig, variacao


# ─────────────────────────────
# SIDEBAR
# ─────────────────────────────
def bloco_cambio_sidebar():
    st.sidebar.markdown(
        "<h3 style='color:#1565C0;margin-bottom:4px;'>"
        "💱 Câmbio USD/BRL</h3>",
        unsafe_allow_html=True
    )
    valor_api, fonte, ok = get_cambio_yahoo()
    df_hist, hist_ok     = get_historico_cambio()

    if ok:
        st.sidebar.success(f"✅ **R$ {valor_api:.4f}** — ao vivo")
        st.sidebar.caption(f"📡 {fonte} · atualiza a cada 5 min")
    else:
        st.sidebar.error(f"⚠️ Sem dados do Yahoo Finance\n\n_{fonte}_")
        st.sidebar.caption("Configure o câmbio manualmente abaixo.")

    if hist_ok and not df_hist.empty:
        fig_mini, variacao = criar_mini_grafico(df_hist)
        minimo  = float(df_hist["Fechamento"].min())
        maximo  = float(df_hist["Fechamento"].max())
        emoji_v = "📈" if variacao >= 0 else "📉"
        cor_v   = "#2e7d32" if variacao >= 0 else "#c62828"
        sinal   = "+" if variacao >= 0 else ""
        st.sidebar.markdown(
            f"<div class='cambio-mini-box'>"
            f"<span style='font-size:11px;color:#546e7a;font-weight:600;'>"
            f"📅 Últimos 30 dias (USD/BRL)</span><br>"
            f"<span style='color:{cor_v};font-weight:700;font-size:15px;'>"
            f"{emoji_v} {sinal}{variacao:.2f}%</span>&nbsp;&nbsp;"
            f"<span style='color:#546e7a;font-size:11px;'>"
            f"Mín R${minimo:.3f} · Máx R${maximo:.3f}</span></div>",
            unsafe_allow_html=True
        )
        if fig_mini:
            st.sidebar.plotly_chart(
                fig_mini, use_container_width=True,
                config={"displayModeBar": False}
            )
    else:
        st.sidebar.caption("📊 Histórico indisponível.")

    st.sidebar.markdown("---")

    if ok:
        usar_auto = st.sidebar.toggle(
            "🔄 Usar cotação automática",
            value=True, key="toggle_cambio"
        )
    else:
        usar_auto = False

    if usar_auto and ok:
        cambio = valor_api
        st.sidebar.caption("💡 Desative o toggle para inserir manualmente.")
    else:
        cambio = st.sidebar.number_input(
            "✏️ Câmbio manual (USD/BRL)",
            min_value=1.00, max_value=20.00,
            value=valor_api if ok else 5.20,
            step=0.01, format="%.4f",
            key="cambio_manual"
        )

    st.sidebar.markdown(
        f"<div class='cambio-em-uso'>"
        f"<span style='color:#546e7a;font-size:12px;'>Câmbio em uso agora</span><br>"
        f"<b style='color:#1565C0;font-size:30px;'>R$ {cambio:.4f}</b></div>",
        unsafe_allow_html=True
    )

    if st.sidebar.button("🔁 Forçar atualização", key="btn_refresh"):
        st.cache_data.clear()
        st.rerun()

    # ── Status API Clima ──
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<h3 style='color:#1565C0;margin-bottom:4px;'>"
        "🌤️ Clima Portuário</h3>",
        unsafe_allow_html=True
    )
    st.sidebar.caption(
        "Powered by OpenWeatherMap · "
        "[Obter chave gratuita](https://openweathermap.org/api)"
    )

    chave_ok = (
        bool(OPENWEATHER_API_KEY)
        and OPENWEATHER_API_KEY != "COLE_SUA_CHAVE_AQUI"
        and len(OPENWEATHER_API_KEY) > 10
    )
    if chave_ok:
        st.sidebar.success("🔑 API Key OpenWeather ativa")
        st.sidebar.caption(
            "Chave configurada no código · "
            "Previsão 5 dias disponível na aba 🌦️"
        )
    else:
        st.sidebar.error(
            "⚠️ API Key não configurada!\n\n"
            "Edite **OPENWEATHER_API_KEY** no topo do arquivo .py"
        )

    st.session_state["weather_key"]   = OPENWEATHER_API_KEY
    st.session_state["cambio_global"] = cambio
    return cambio


# ─────────────────────────────
# FUNÇÕES 3D
# ─────────────────────────────
def criar_container_wireframe(container):
    c  = container
    vx = [0, c.comp, c.comp, 0,     0,     c.comp, c.comp, 0    ]
    vy = [0, 0,      c.larg, c.larg,0,     0,      c.larg, c.larg]
    vz = [0, 0,      0,      0,     c.alt, c.alt,  c.alt,  c.alt ]
    arestas = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
    ex, ey, ez = [], [], []
    for (a, b) in arestas:
        ex += [vx[a], vx[b], None]
        ey += [vy[a], vy[b], None]
        ez += [vz[a], vz[b], None]
    return go.Scatter3d(
        x=ex, y=ey, z=ez,
        mode='lines',
        line=dict(color='#64B5F6', width=3),
        name='Container', hoverinfo='skip'
    )


@st.cache_data(show_spinner=False)
def calcular_e_plotar(
    cont_tipo, cont_comp, cont_larg, cont_alt, cont_peso_max,
    cx_nome, cx_comp, cx_larg, cx_alt, cx_peso,
    cx_cor, cx_cor_borda, percentual
):
    if cx_comp <= 0 or cx_larg <= 0 or cx_alt <= 0 or cx_peso <= 0:
        return go.Figure(), {}

    container   = Container(cont_tipo, cont_comp, cont_larg, cont_alt, cont_peso_max)
    qtd_c       = int(cont_comp / cx_comp)
    qtd_l       = int(cont_larg / cx_larg)
    qtd_a       = int(cont_alt  / cx_alt)
    total_vol   = qtd_c * qtd_l * qtd_a
    max_peso    = int(cont_peso_max / cx_peso)
    total_real  = min(total_vol, max_peso)
    qtd_mostrar = min(int(total_real * percentual / 100), 2000)

    all_x, all_y, all_z = [], [], []
    all_i, all_j, all_k = [], [], []
    edge_x, edge_y, edge_z = [], [], []
    arestas = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]

    count = 0
    for az in range(qtd_a):
        for al in range(qtd_l):
            for ac in range(qtd_c):
                if count >= qtd_mostrar:
                    break
                x  = ac * cx_comp
                y  = al * cx_larg
                z  = az * cx_alt
                dx, dy, dz = cx_comp, cx_larg, cx_alt
                offset = len(all_x)
                vx = [x,    x+dx, x+dx, x,    x,    x+dx, x+dx, x   ]
                vy = [y,    y,    y+dy, y+dy, y,    y,    y+dy, y+dy ]
                vz = [z,    z,    z,    z,    z+dz, z+dz, z+dz, z+dz ]
                all_x.extend(vx); all_y.extend(vy); all_z.extend(vz)
                i_l = [0,0, 1,1, 0,0, 3,3, 0,0, 4,4]
                j_l = [1,2, 2,5, 4,5, 2,6, 3,7, 5,6]
                k_l = [2,3, 5,6, 5,4, 6,7, 7,4, 6,7]
                all_i.extend([i + offset for i in i_l])
                all_j.extend([j + offset for j in j_l])
                all_k.extend([k + offset for k in k_l])
                for (a, b) in arestas:
                    edge_x += [vx[a], vx[b], None]
                    edge_y += [vy[a], vy[b], None]
                    edge_z += [vz[a], vz[b], None]
                count += 1
            if count >= qtd_mostrar:
                break
        if count >= qtd_mostrar:
            break

    traces = [criar_container_wireframe(container)]
    if all_x:
        traces.append(go.Mesh3d(
            x=all_x, y=all_y, z=all_z,
            i=all_i, j=all_j, k=all_k,
            color=cx_cor, opacity=0.85, flatshading=True,
            lighting=dict(ambient=0.7, diffuse=0.9,
                          specular=0.2, roughness=0.5, fresnel=0.1),
            lightposition=dict(x=1000, y=1000, z=1500),
            showscale=False, hoverinfo='skip', name='Caixas'
        ))
    if edge_x:
        traces.append(go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color=cx_cor_borda, width=1),
            hoverinfo='skip', showlegend=False, name='Bordas'
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title=dict(text='Comprimento (cm)', font=dict(color='#90CAF9')),
                backgroundcolor='rgba(5,10,30,0.8)',
                gridcolor='rgba(45,90,142,0.5)',
                showbackground=True, zerolinecolor='#2d5a8e',
                tickfont=dict(color='#90CAF9')
            ),
            yaxis=dict(
                title=dict(text='Largura (cm)', font=dict(color='#90CAF9')),
                backgroundcolor='rgba(5,10,30,0.8)',
                gridcolor='rgba(45,90,142,0.5)',
                showbackground=True, zerolinecolor='#2d5a8e',
                tickfont=dict(color='#90CAF9')
            ),
            zaxis=dict(
                title=dict(text='Altura (cm)', font=dict(color='#90CAF9')),
                backgroundcolor='rgba(5,10,30,0.8)',
                gridcolor='rgba(45,90,142,0.5)',
                showbackground=True, zerolinecolor='#2d5a8e',
                tickfont=dict(color='#90CAF9')
            ),
            bgcolor='rgba(5,10,30,0.85)',
            camera=dict(eye=dict(x=1.8, y=-1.8, z=1.2),
                        up=dict(x=0, y=0, z=1)),
            aspectmode='data'
        ),
        paper_bgcolor='rgba(5,10,30,0.5)',
        plot_bgcolor='rgba(5,10,30,0.5)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=600, showlegend=False
    )

    vol_pct  = (
        total_real * cx_comp * cx_larg * cx_alt
        / (cont_comp * cont_larg * cont_alt) * 100
    )
    peso_pct = (total_real * cx_peso / cont_peso_max) * 100
    stats = {
        "total":      total_real,
        "mostradas":  qtd_mostrar,
        "qtd_c":      qtd_c,
        "qtd_l":      qtd_l,
        "qtd_a":      qtd_a,
        "peso_total": total_real * cx_peso,
        "vol_pct":    vol_pct,
        "peso_pct":   peso_pct,
        "limitador":  "Peso ⚖️" if max_peso < total_vol else "Volume 📦",
    }
    return fig, stats


# ─────────────────────────────
# FUNÇÕES — PRICING / IMPOSTOS
# ─────────────────────────────
def calcular_impostos(
    valor_cif_usd, cambio, categoria, icms_estado=18.0
):
    aliq          = ALIQUOTAS_NCM[categoria]
    valor_cif_brl = valor_cif_usd * cambio
    afrmm         = valor_cif_brl * 0.08
    ii            = valor_cif_brl * (aliq["II"]     / 100)
    base_ipi      = valor_cif_brl + ii
    ipi           = base_ipi      * (aliq["IPI"]    / 100)
    pis           = valor_cif_brl * (aliq["PIS"]    / 100)
    cofins        = valor_cif_brl * (aliq["COFINS"] / 100)
    soma_antes    = valor_cif_brl + ii + ipi + pis + cofins + afrmm
    icms          = (
        soma_antes / (1 - icms_estado / 100) * (icms_estado / 100)
    )
    siscomex      = 214.50
    total_imp     = ii + ipi + pis + cofins + icms + afrmm + siscomex
    total_geral   = valor_cif_brl + total_imp
    return {
        "valor_cif_brl":  valor_cif_brl,
        "II":             ii,
        "IPI":            ipi,
        "PIS":            pis,
        "COFINS":         cofins,
        "ICMS":           icms,
        "AFRMM":          afrmm,
        "Siscomex":       siscomex,
        "total_impostos": total_imp,
        "total_geral":    total_geral,
        "aliquotas":      aliq,
        "icms_estado":    icms_estado,
    }


def calcular_demurrage(
    dias_livres: int, dias_usados: int, tipo_cont: str
) -> float:
    TARIFAS = {"20ft": 85, "40ft": 110, "40ft HC": 120}
    dias_excedentes = max(0, dias_usados - dias_livres)
    return dias_excedentes * TARIFAS.get(tipo_cont, 85)


# ═══════════════════════════════════════════
# INICIALIZAÇÃO
# ═══════════════════════════════════════════
cambio_atual = bloco_cambio_sidebar()


# ═══════════════════════════════════════════
# HERO BANNER
# ═══════════════════════════════════════════
st.markdown(f"""
<div class='hero-banner'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div>
      <div class='porto-tag'>⚓ Porto de Santos — SP, Brasil</div>
      <h1 style='font-size:52px;font-weight:900;color:#ffffff;
                 margin:14px 0 0 0;line-height:1.1;
                 text-shadow:0 2px 8px rgba(0,0,0,0.2);'>
        🚢 Porto Pricing Tool
      </h1>
      <p style='color:#e3f2fd;font-size:19px;margin-top:10px;font-weight:400;'>
        Plataforma completa de otimização de carga e precificação portuária
      </p>
      <div style='margin-top:15px;'>
        <span class='hero-badge'>📦 3D Container</span>
        <span class='hero-badge'>💰 Custos & Fretes</span>
        <span class='hero-badge'>🛃 Impostos</span>
        <span class='hero-badge'>📊 Cenários</span>
        <span class='hero-badge'>📄 Relatório</span>
        <span class='hero-badge'>🌦️ Previsão 5 Dias</span>
      </div>
      <div style='margin-top:18px;background:rgba(255,255,255,0.2);
                  border-radius:10px;padding:10px 18px;display:inline-block;'>
        💱 Câmbio USD/BRL:
        <b style='color:#ffffff;font-size:22px;'>R$ {cambio_atual:.4f}</b>
        &nbsp;
        <span style='color:#e3f2fd;font-size:12px;'>ao vivo · Yahoo Finance</span>
      </div>
    </div>
    <div style='font-size:100px;opacity:0.20;padding-right:20px;'>🚢</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# ABAS
# ═══════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📦  Container 3D",
    "💰  Custos & Fretes",
    "🛃  Impostos",
    "📊  Simulador de Cenários",
    "📄  Relatório Final",
    "🌦️  Previsão do Tempo",
])
# ═══════════════════════════════════════════
# ABA 1 — CONTAINER 3D
# ═══════════════════════════════════════════
with tab1:
    col_main, col_side = st.columns([3, 1])

    with col_side:
        st.markdown(
            "<h3 style='color:#1565C0;'>⚙️ Configurações</h3>",
            unsafe_allow_html=True
        )
        container_nome = st.selectbox(
            "🚢 Tipo de Container",
            list(CONTAINERS.keys()), key="t1_cont"
        )
        container = CONTAINERS[container_nome]

        caixa_nome = st.selectbox(
            "📦 Tipo de Caixa",
            list(CAIXAS.keys()), key="t1_caixa"
        )
        caixa = CAIXAS[caixa_nome]

        if "Custom" in caixa_nome:
            st.markdown("#### 🔧 Dimensões da Caixa")
            c_comp = st.slider("Comprimento (cm)", 10, 200, 40, key="cc")
            c_larg = st.slider("Largura (cm)",     10, 200, 30, key="cl")
            c_alt  = st.slider("Altura (cm)",      10, 200, 25, key="ca")
            c_peso = st.slider("Peso (kg)",          1, 500,  5, key="cp")
            caixa  = Caixa(
                "Custom", c_comp, c_larg, c_alt, c_peso,
                "rgba(200,100,255,0.8)", "#cc44ff"
            )

        percentual = st.slider(
            "🔄 Percentual de Carga",
            0, 100, 100, 5, key="t1_perc",
            help="Simule diferentes níveis de preenchimento"
        )

        st.markdown("---")
        st.markdown(f"""
        <div class='info-box'>
            <b>📐 Container:</b> {container.tipo}<br>
            {container.comp}×{container.larg}×{container.alt} cm<br>
            Vol: {container.comp*container.larg*container.alt/1e6:.1f} m³<br>
            <b>Carga Máx: {container.peso_max:,} kg</b>
        </div>
        <div class='info-box'>
            <b>📦 Caixa:</b> {caixa.nome}<br>
            {caixa.comp}×{caixa.larg}×{caixa.alt} cm<br>
            Vol: {caixa.comp*caixa.larg*caixa.alt/1e6:.4f} m³<br>
            <b>Peso: {caixa.peso} kg</b>
        </div>
        """, unsafe_allow_html=True)

    with col_main:
        fig, stats = calcular_e_plotar(
            container.tipo,
            container.comp, container.larg,
            container.alt,  container.peso_max,
            caixa.nome,
            caixa.comp, caixa.larg,
            caixa.alt,  caixa.peso,
            caixa.cor,  caixa.cor_borda,
            percentual
        )

        m1, m2, m3, m4, m5 = st.columns(5)
        for col, icon, val, label in [
            (m1, "📦", stats.get("total", 0),              "Total Caixas"),
            (m2, "✅", stats.get("mostradas", 0),           "Carregadas"),
            (m3, "📐", f"{stats.get('vol_pct',0):.1f}%",   "Vol. Utilizado"),
            (m4, "⚖️", f"{stats.get('peso_total',0):,.0f}", "Peso (kg)"),
            (m5, "🎯", stats.get("limitador", "—"),         "Limitante"),
        ]:
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size:22px;'>{icon}</div>
                    <div class='metric-value'>{val}</div>
                    <div class='metric-label'>{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown(
            "<p style='color:#1a237e;font-size:14px;margin-top:10px;'>"
            "💡 <b>Dica:</b> Arraste para rotacionar "
            "| Scroll para zoom | Duplo clique para resetar</p>",
            unsafe_allow_html=True
        )
        st.plotly_chart(fig, use_container_width=True)

        p1, p2 = st.columns(2)
        with p1:
            st.markdown(
                "<p style='color:#1a237e;font-weight:600;'>"
                "📦 Volume Utilizado</p>",
                unsafe_allow_html=True
            )
            st.progress(min(stats.get("vol_pct", 0) / 100, 1.0))
            st.markdown(
                f"<b style='color:#1565C0;font-size:16px;'>"
                f"{stats.get('vol_pct',0):.1f}%</b>",
                unsafe_allow_html=True
            )
        with p2:
            st.markdown(
                "<p style='color:#1a237e;font-weight:600;'>"
                "⚖️ Peso Utilizado</p>",
                unsafe_allow_html=True
            )
            st.progress(min(stats.get("peso_pct", 0) / 100, 1.0))
            st.markdown(
                f"<b style='color:#1565C0;font-size:16px;'>"
                f"{stats.get('peso_pct',0):.1f}%</b>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown(
            "<h4 style='color:#1565C0;'>📐 Arranjo Espacial</h4>",
            unsafe_allow_html=True
        )
        a1, a2, a3 = st.columns(3)
        for col, icon, val, label in [
            (a1, "↔️", stats.get("qtd_c", 0), "Colunas (Comprimento)"),
            (a2, "↕️", stats.get("qtd_l", 0), "Fileiras (Largura)"),
            (a3, "🔝", stats.get("qtd_a", 0), "Camadas (Altura)"),
        ]:
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size:20px;'>{icon}</div>
                    <div class='metric-value'>{val}</div>
                    <div class='metric-label'>{label}</div>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# ABA 2 — CUSTOS & FRETES
# ═══════════════════════════════════════════
with tab2:
    st.markdown(
        "<h2 style='color:#1565C0;'>"
        "💰 Calculadora de Custos & Fretes</h2>",
        unsafe_allow_html=True
    )
    st.markdown(f"""
    <div class='info-box'>
        💱 <b>Câmbio USD/BRL em uso:</b>
        <span style='color:#1565C0;font-size:22px;font-weight:bold;'>
            R$ {cambio_atual:.4f}
        </span>
        &nbsp;
        <span style='color:#546e7a;font-size:12px;'>
            (Yahoo Finance — ajuste na sidebar)
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    col_form, col_result = st.columns(2)

    with col_form:
        st.markdown(
            "<h4 style='color:#1565C0;'>🚢 Dados do Embarque</h4>",
            unsafe_allow_html=True
        )
        tipo_op = st.selectbox(
            "Tipo de Operação",
            ["Importação", "Exportação"], key="t2_op"
        )
        cont_tipo = st.selectbox(
            "Tipo de Container",
            ["20ft", "40ft", "40ft HC"], key="t2_cont"
        )
        qtd_containers = st.number_input(
            "Quantidade de Containers",
            min_value=1, value=1, key="t2_qtd"
        )
        origem  = st.text_input(
            "Porto de Origem",  "Shanghai", key="t2_orig"
        )
        destino = st.text_input(
            "Porto de Destino", "Santos",   key="t2_dest"
        )

        # ── CLIMA ATUAL ──
        weather_key = st.session_state.get("weather_key", "")
        st.markdown("---")
        st.markdown(
            "<h4 style='color:#1565C0;'>🌤️ Clima Atual nos Portos</h4>",
            unsafe_allow_html=True
        )
        chave_ativa = (
            bool(weather_key)
            and weather_key != "COLE_SUA_CHAVE_AQUI"
            and len(weather_key) > 10
        )
        if not chave_ativa:
            st.info(
                "🔑 Configure **OPENWEATHER_API_KEY** no topo "
                "do arquivo para ver o clima em tempo real.\n\n"
                "Chave gratuita em: openweathermap.org/api"
            )
        else:
            with st.spinner("🌍 Consultando clima atual..."):
                dados_orig, err_orig = get_clima(origem,  weather_key)
                dados_dest, err_dest = get_clima(destino, weather_key)
            render_clima_card(
                dados_orig, f"📍 Origem · {origem}",   origem
            )
            render_clima_card(
                dados_dest, f"🏁 Destino · {destino}", destino
            )
            if st.button("🔄 Atualizar Clima", key="btn_clima"):
                st.cache_data.clear()
                st.rerun()

        # ── COMPARATIVO ARMADORES ──
        st.markdown("---")
        st.markdown(
            "<h4 style='color:#1565C0;'>🚢 Comparativo de Armadores</h4>",
            unsafe_allow_html=True
        )
        df_arm = pd.DataFrame([
            {
                "Armador":      arm,
                "Frete (USD)":  f"USD {precos[cont_tipo]:,.0f}",
                "Frete (BRL)":  f"R$ {precos[cont_tipo]*cambio_atual:,.2f}",
                "Transit Time": "28–35 dias",
            }
            for arm, precos in ARMADORES_REFERENCIA.items()
        ])
        st.dataframe(df_arm, use_container_width=True, hide_index=True)

        melhor = min(
            ARMADORES_REFERENCIA.items(),
            key=lambda x: x[1][cont_tipo]
        )
        st.success(
            f"💡 **Menor frete:** {melhor[0]} — "
            f"USD {melhor[1][cont_tipo]:,.0f} "
            f"(R$ {melhor[1][cont_tipo]*cambio_atual:,.2f})"
        )

        # ── VALORES USD ──
        st.markdown("---")
        st.markdown(
            "<h4 style='color:#1565C0;'>💵 Valores (USD)</h4>",
            unsafe_allow_html=True
        )
        valor_mercadoria = st.number_input(
            "Valor da Mercadoria (USD)",
            min_value=0.0, value=50000.0,
            format="%.2f", key="t2_merc"
        )
        frete_maritimo = st.number_input(
            "Frete Marítimo (USD)",
            min_value=0.0, value=2500.0,
            format="%.2f", key="t2_frete"
        )
        seguro_pct = st.slider(
            "Seguro de Carga (%)",
            0.0, 3.0, 0.3, 0.05, key="t2_seg"
        )

        # ── SURCHARGES ──
        st.markdown("---")
        st.markdown(
            "<h4 style='color:#1565C0;'>📦 Surcharges</h4>",
            unsafe_allow_html=True
        )
        usar_gri = st.checkbox(
            "GRI - General Rate Increase", value=False, key="gri"
        )
        usar_baf = st.checkbox(
            "BAF - Bunker Adjustment",     value=True,  key="baf"
        )
        usar_pss = st.checkbox(
            "PSS - Peak Season Surcharge", value=False, key="pss"
        )
        usar_do  = st.checkbox(
            "D/O - Delivery Order",        value=True,  key="do"
        )
        usar_vgm = st.checkbox(
            "VGM - Verificação Massa Bruta", value=True, key="vgm"
        )

        surcharges_total_usd = sum([
            SURCHARGES["GRI - General Rate Increase"][cont_tipo]   if usar_gri else 0,
            SURCHARGES["BAF - Bunker Adjustment Factor"][cont_tipo] if usar_baf else 0,
            SURCHARGES["PSS - Peak Season Surcharge"][cont_tipo]    if usar_pss else 0,
            SURCHARGES["D/O - Delivery Order"][cont_tipo]           if usar_do  else 0,
            SURCHARGES["VGM - Verificação Massa Bruta"][cont_tipo]  if usar_vgm else 0,
        ])

        # ── DEMURRAGE ──
        st.markdown("---")
        st.markdown(
            "<h4 style='color:#1565C0;'>⏱️ Demurrage & Detention</h4>",
            unsafe_allow_html=True
        )
        dias_livres      = st.number_input(
            "Dias Livres no Porto", 7, 30, 14, key="t2_dl"
        )
        dias_usados_port = st.number_input(
            "Dias Utilizados", 0, 60, 10, key="t2_du"
        )

        # ✅ Pré-calculado fora do f-string — sem erro de chaves
        TARIFAS_DEMURRAGE = {"20ft": 85, "40ft": 110, "40ft HC": 120}
        tarifa_dia        = TARIFAS_DEMURRAGE.get(cont_tipo, 85)
        dias_excedentes   = max(0, int(dias_usados_port) - int(dias_livres))
        demurrage_usd     = calcular_demurrage(
            int(dias_livres), int(dias_usados_port), cont_tipo
        )

        if demurrage_usd > 0:
            st.warning(
                f"⚠️ **Demurrage:** USD {demurrage_usd:,.2f} "
                f"({dias_excedentes} dias excedentes × "
                f"USD {tarifa_dia}/dia)"
            )
        else:
            st.success("✅ Sem demurrage — dentro do período livre")

        # ── LOGÍSTICA INTERNA ──
        st.markdown("---")
        st.markdown(
            "<h4 style='color:#1565C0;'>🚛 Logística Interna</h4>",
            unsafe_allow_html=True
        )
        frete_rodoviario = st.number_input(
            "Frete Rodoviário (R$)",
            min_value=0.0, value=3500.0,
            format="%.2f", key="t2_rod"
        )
        despachante = st.number_input(
            "Despachante Aduaneiro (R$)",
            min_value=0.0, value=2800.0,
            format="%.2f", key="t2_desp"
        )
        armazenagem_dias = st.number_input(
            "Dias de Armazenagem",
            min_value=0, value=5, key="t2_arm"
        )
        cambio_usado = st.number_input(
            "Câmbio USD/BRL (editável)",
            min_value=1.0, value=float(cambio_atual),
            format="%.4f", key="t2_cambio"
        )

        st.session_state["val_mercadoria"] = valor_mercadoria
        st.session_state["frete_maritimo"] = frete_maritimo
        st.session_state["frete_rodo"]     = frete_rodoviario
        st.session_state["despachante"]    = despachante
        st.session_state["cont_tipo_rel"]  = cont_tipo

    # ── COLUNA DE RESULTADOS ──
    with col_result:
        st.markdown(
            "<h4 style='color:#1565C0;'>📊 Resumo de Custos</h4>",
            unsafe_allow_html=True
        )

        seguro_usd      = valor_mercadoria * (seguro_pct / 100)
        valor_cif_usd   = valor_mercadoria + frete_maritimo + seguro_usd
        valor_cif_brl   = valor_cif_usd * cambio_usado
        total_taxas_brl = (
            sum(v[cont_tipo] for v in TAXAS_PORTUARIAS.values())
            * qtd_containers * cambio_usado
        )
        surcharges_brl = (
            surcharges_total_usd * cambio_usado * qtd_containers
        )
        demurrage_brl = demurrage_usd * cambio_usado * qtd_containers

        if armazenagem_dias <= 5:
            arm_brl = armazenagem_dias * 180
        elif armazenagem_dias <= 10:
            arm_brl = 5*180 + (armazenagem_dias - 5) * 280
        else:
            arm_brl = 5*180 + 5*280 + (armazenagem_dias - 10) * 420
        arm_brl *= qtd_containers

        total_brl = (
            valor_cif_brl    + total_taxas_brl
            + surcharges_brl + demurrage_brl
            + arm_brl        + frete_rodoviario
            + despachante
        )

        itens = [
            (
                "🌊 Frete Marítimo",
                frete_maritimo * cambio_usado,
                f"USD {frete_maritimo:,.2f} × {cambio_usado:.4f}",
                "custo-card"
            ),
            (
                "🛡️ Seguro de Carga",
                seguro_usd * cambio_usado,
                f"{seguro_pct}% sobre mercadoria",
                "custo-card"
            ),
            (
                "📦 Surcharges (GRI/BAF/PSS/D.O/VGM)",
                surcharges_brl,
                f"USD {surcharges_total_usd:,.0f} × {qtd_containers} cont.",
                "custo-card"
            ),
            (
                "⏱️ Demurrage & Detention",
                demurrage_brl,
                f"USD {demurrage_usd:,.0f} × {qtd_containers} cont.",
                "custo-card-red" if demurrage_brl > 0 else "custo-card"
            ),
            (
                "🏭 Taxas Portuárias",
                total_taxas_brl,
                f"THC+BL+ISPS+Capatazia × {qtd_containers} cont.",
                "custo-card-yellow"
            ),
            (
                "🏗️ Armazenagem",
                arm_brl,
                f"{armazenagem_dias} dias (escalonado)",
                "custo-card-yellow"
            ),
            (
                "🚛 Frete Rodoviário",
                frete_rodoviario,
                "Porto → Destino final",
                "custo-card-green"
            ),
            (
                "📋 Despachante",
                despachante,
                "Serviços aduaneiros",
                "custo-card-green"
            ),
        ]

        for nome, valor, detalhe, classe in itens:
            st.markdown(f"""
            <div class='custo-card {classe}'>
              <div style='display:flex;justify-content:space-between;
                          align-items:center;'>
                <div>
                  <b style='color:#1a237e;font-size:15px;'>{nome}</b><br>
                  <small style='color:#546e7a;font-size:13px;'>
                    {detalhe}</small>
                </div>
                <div style='font-size:20px;font-weight:bold;
                            color:#1565C0;'>
                  R$ {valor:,.2f}
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='total-card'>
          <p style='color:#B3D9F7;margin:0;font-size:14px;'>
            CUSTO TOTAL DA OPERAÇÃO</p>
          <h1 style='color:white;margin:8px 0;font-size:42px;'>
            R$ {total_brl:,.2f}</h1>
          <p style='color:#90CAF9;margin:0;font-size:13px;'>
            ≈ USD {total_brl/cambio_usado:,.2f}
            &nbsp;|&nbsp;
            R$ {total_brl/qtd_containers:,.2f} por container
          </p>
        </div>""", unsafe_allow_html=True)

        with st.expander("📋 Detalhamento Taxas Portuárias"):
            for taxa, valores in TAXAS_PORTUARIAS.items():
                val_t = (
                    valores[cont_tipo] * cambio_usado * qtd_containers
                )
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;
                            padding:8px;border-bottom:1px solid #e3f2fd;'>
                  <span style='color:#37474f;font-size:14px;'>
                    {taxa}</span>
                  <span style='color:#1565C0;font-weight:bold;
                               font-size:14px;'>
                    R$ {val_t:,.2f}</span>
                </div>""", unsafe_allow_html=True)

        with st.expander("📦 Detalhamento Surcharges"):
            surcharges_map = {
                "GRI - General Rate Increase":   usar_gri,
                "BAF - Bunker Adjustment Factor": usar_baf,
                "PSS - Peak Season Surcharge":    usar_pss,
                "D/O - Delivery Order":           usar_do,
                "VGM - Verificação Massa Bruta":  usar_vgm,
            }
            for nome_s, ativo in surcharges_map.items():
                val_s = (
                    SURCHARGES[nome_s][cont_tipo]
                    * cambio_usado * qtd_containers
                    if ativo else 0
                )
                status = "✅" if ativo else "⬜"
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;
                            padding:8px;border-bottom:1px solid #e3f2fd;'>
                  <span style='color:#37474f;font-size:14px;'>
                    {status} {nome_s}</span>
                  <span style='color:{"#1565C0" if ativo else "#90a4ae"};
                               font-weight:bold;font-size:14px;'>
                    R$ {val_s:,.2f}</span>
                </div>""", unsafe_allow_html=True)

        if st.button("💾 Salvar Cotação", key="t2_save"):
            if "cotacoes" not in st.session_state:
                st.session_state.cotacoes = []
            st.session_state.cotacoes.append({
                "Data":       datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Origem":     html_lib.escape(str(origem)),
                "Destino":    html_lib.escape(str(destino)),
                "Container":  cont_tipo,
                "Qtd":        qtd_containers,
                "Total (R$)": f"R$ {total_brl:,.2f}",
                "Câmbio":     f"{cambio_usado:.4f}",
            })
            st.success("✅ Cotação salva com sucesso!")


# ═══════════════════════════════════════════
# ABA 3 — IMPOSTOS
# ═══════════════════════════════════════════
with tab3:
    st.markdown(
        "<h2 style='color:#1565C0;'>"
        "🛃 Simulador de Impostos de Importação</h2>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class='info-box'>
        ℹ️ Cálculo em <b>cascata</b> conforme legislação brasileira:<br>
        II → IPI → PIS/COFINS → ICMS (por dentro) → AFRMM → Siscomex
    </div>
    """, unsafe_allow_html=True)

    col_imp1, col_imp2 = st.columns(2)

    with col_imp1:
        st.markdown(
            "<h4 style='color:#1565C0;'>📦 Dados da Mercadoria</h4>",
            unsafe_allow_html=True
        )
        categoria = st.selectbox(
            "Categoria NCM",
            list(ALIQUOTAS_NCM.keys()), key="t3_cat"
        )
        if categoria == "Personalizado":
            st.markdown("#### ⚙️ Alíquotas (%)")
            ii_c  = st.number_input(
                "II (%)",  0.0, 100.0, 0.0, key="ii_c"
            )
            ipi_c = st.number_input(
                "IPI (%)", 0.0, 100.0, 0.0, key="ipi_c"
            )
            ALIQUOTAS_NCM["Personalizado"]["II"]  = ii_c
            ALIQUOTAS_NCM["Personalizado"]["IPI"] = ipi_c

        valor_cif_imp = st.number_input(
            "Valor CIF (USD)",
            min_value=0.0, value=50000.0,
            format="%.2f", key="t3_cif",
            help="Cost + Insurance + Freight"
        )
        cambio_imp = st.number_input(
            "Câmbio USD/BRL",
            min_value=1.0, value=float(cambio_atual),
            format="%.4f", key="t3_cambio"
        )
        icms_estado = st.selectbox(
            "Estado de Destino (ICMS)",
            options=[
                ("SP - São Paulo",         18.0),
                ("RJ - Rio de Janeiro",    20.0),
                ("MG - Minas Gerais",      18.0),
                ("SC - Santa Catarina",    17.0),
                ("RS - Rio Grande do Sul", 17.0),
                ("PR - Paraná",            12.0),
                ("BA - Bahia",             19.0),
                ("Outro",                  17.0),
            ],
            format_func=lambda x: x[0],
            key="t3_icms"
        )
        aliq_icms = icms_estado[1]
        aliq      = ALIQUOTAS_NCM[categoria]

        st.markdown(f"""
        <div class='info-box' style='margin-top:15px;'>
            <b>📊 Alíquotas — {categoria}:</b><br>
            II: <b>{aliq['II']}%</b> &nbsp;|&nbsp;
            IPI: <b>{aliq['IPI']}%</b> &nbsp;|&nbsp;
            PIS: <b>{aliq['PIS']}%</b> &nbsp;|&nbsp;
            COFINS: <b>{aliq['COFINS']}%</b> &nbsp;|&nbsp;
            ICMS: <b>{aliq_icms}%</b>
        </div>
        """, unsafe_allow_html=True)

    with col_imp2:
        st.markdown(
            "<h4 style='color:#1565C0;'>📊 Resultado dos Impostos</h4>",
            unsafe_allow_html=True
        )
        imp = calcular_impostos(
            valor_cif_imp, cambio_imp, categoria, aliq_icms
        )

        impostos_items = [
            ("🏛️ II — Imposto de Importação", imp["II"],       aliq["II"]),
            ("🏭 IPI — Imposto sobre Produto", imp["IPI"],      aliq["IPI"]),
            ("📊 PIS Importação",              imp["PIS"],      aliq["PIS"]),
            ("📊 COFINS Importação",           imp["COFINS"],   aliq["COFINS"]),
            ("🏙️ ICMS Importação",            imp["ICMS"],     aliq_icms),
            ("⚓ AFRMM — Marinha Mercante",    imp["AFRMM"],    8.0),
            ("💻 Siscomex",                    imp["Siscomex"], 0.0),
        ]

        for nome, valor, aliquota in impostos_items:
            pct = f"({aliquota}%)" if aliquota > 0 else "(fixo)"
            st.markdown(f"""
            <div class='custo-card'>
              <div style='display:flex;justify-content:space-between;
                          align-items:center;'>
                <div>
                  <b style='color:#1a237e;font-size:14px;'>{nome}</b>
                  <small style='color:#546e7a;'> {pct}</small>
                </div>
                <b style='color:#1565C0;font-size:18px;'>
                  R$ {valor:,.2f}</b>
              </div>
            </div>""", unsafe_allow_html=True)

        carga_trib_pct_t3 = (
            imp["total_impostos"] / imp["valor_cif_brl"]
        ) * 100

        st.markdown(f"""
        <div class='total-card' style='margin-top:15px;'>
          <p style='color:#B3D9F7;margin:0;font-size:13px;'>
            TOTAL DE IMPOSTOS</p>
          <h2 style='color:#ff6b6b;margin:6px 0;'>
            R$ {imp['total_impostos']:,.2f}</h2>
          <p style='color:#B3D9F7;margin:4px 0 0;font-size:13px;'>
            VALOR TOTAL NACIONALIZADO</p>
          <h1 style='color:white;margin:6px 0;font-size:36px;'>
            R$ {imp['total_geral']:,.2f}</h1>
          <p style='color:#90CAF9;margin:0;font-size:12px;'>
            Carga tributária: {carga_trib_pct_t3:.1f}%
            sobre o valor CIF</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<h4 style='color:#1565C0;'>📊 Composição Tributária</h4>",
        unsafe_allow_html=True
    )
    labels = [
        "II", "IPI", "PIS", "COFINS",
        "ICMS", "AFRMM", "Siscomex"
    ]
    values = [
        imp["II"],    imp["IPI"],      imp["PIS"],
        imp["COFINS"], imp["ICMS"],
        imp["AFRMM"], imp["Siscomex"]
    ]
    colors = [
        "#e53935", "#fb8c00", "#43a047", "#00897b",
        "#8e24aa", "#00acc1", "#6d4c41"
    ]

    g1, g2 = st.columns(2)
    with g1:
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, values=values,
            marker=dict(colors=colors),
            hole=0.45,
            textinfo="label+percent",
            textfont=dict(color="#1a1a1a", size=13)
        )])
        fig_pie.update_layout(
            paper_bgcolor="rgba(240,244,248,0.5)",
            plot_bgcolor="rgba(240,244,248,0.5)",
            font=dict(color="#1a237e"),
            height=360, showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with g2:
        fig_bar = go.Figure(data=[go.Bar(
            x=labels, y=values,
            marker=dict(color=colors, opacity=0.85),
            text=[f"R$ {v:,.0f}" for v in values],
            textposition="outside",
            textfont=dict(color="#1a237e", size=11)
        )])
        fig_bar.update_layout(
            paper_bgcolor="rgba(240,244,248,0.5)",
            plot_bgcolor="rgba(240,244,248,0.5)",
            font=dict(color="#1a237e"),
            height=360,
            xaxis=dict(
                gridcolor="rgba(21,101,192,0.2)", color="#1a237e"
            ),
            yaxis=dict(
                gridcolor="rgba(21,101,192,0.2)", color="#1a237e"
            ),
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ═══════════════════════════════════════════
# ABA 4 — SIMULADOR DE CENÁRIOS
# ═══════════════════════════════════════════
with tab4:
    st.markdown(
        "<h2 style='color:#1565C0;'>📊 Simulador de Cenários</h2>",
        unsafe_allow_html=True
    )
    sc1, sc2 = st.columns([1, 2])

    with sc1:
        st.markdown(
            "<h4 style='color:#1565C0;'>⚙️ Parâmetros Base</h4>",
            unsafe_allow_html=True
        )
        val_base = st.number_input(
            "Valor da Mercadoria (USD)",
            min_value=1000.0, value=50000.0,
            format="%.2f", key="sc_val"
        )
        frete_base = st.number_input(
            "Frete Marítimo (USD)",
            min_value=0.0, value=2500.0,
            format="%.2f", key="sc_frete"
        )
        cat_base = st.selectbox(
            "Categoria NCM",
            list(ALIQUOTAS_NCM.keys()), key="sc_cat"
        )
        cont_cenario = st.selectbox(
            "Tipo de Container",
            ["20ft", "40ft", "40ft HC"], key="sc_cont"
        )

        st.markdown("---")
        st.markdown(
            "<h4 style='color:#1565C0;'>💱 Variação Cambial</h4>",
            unsafe_allow_html=True
        )
        cambio_min = st.number_input(
            "Câmbio Mínimo", 3.0, 10.0, 4.0, 0.10, key="sc_cmin"
        )
        cambio_max = st.number_input(
            "Câmbio Máximo", 3.0, 15.0, 7.0, 0.10, key="sc_cmax"
        )

        st.markdown("---")
        st.markdown(
            "<h4 style='color:#1565C0;'>📦 Variação de Volume</h4>",
            unsafe_allow_html=True
        )
        cont_min = st.number_input(
            "Mín. Containers", 1, 50,  1, key="sc_vmin"
        )
        cont_max = st.number_input(
            "Máx. Containers", 1, 50, 10, key="sc_vmax"
        )

    with sc2:
        st.markdown(
            "<h4 style='color:#1565C0;'>"
            "💱 Impacto do Câmbio no Custo Total</h4>",
            unsafe_allow_html=True
        )
        cambios       = np.linspace(cambio_min, cambio_max, 30)
        custos_cambio = []
        for c in cambios:
            imp_c = calcular_impostos(
                val_base + frete_base, c, cat_base
            )
            custos_cambio.append(
                imp_c["total_geral"] + 3500 + 2800
            )

        fig_cambio = go.Figure()
        fig_cambio.add_trace(go.Scatter(
            x=cambios, y=custos_cambio,
            mode="lines+markers",
            line=dict(color="#1565C0", width=3),
            marker=dict(size=6, color="#1565C0"),
            fill="tozeroy",
            fillcolor="rgba(21,101,192,0.1)",
            name="Custo Total"
        ))
        fig_cambio.add_vline(
            x=cambio_atual, line_dash="dash",
            line_color="#f57f17",
            annotation_text=f"Atual: R${cambio_atual:.2f}",
            annotation_font_color="#f57f17"
        )
        fig_cambio.update_layout(
            paper_bgcolor="rgba(240,244,248,0.5)",
            plot_bgcolor="rgba(240,244,248,0.5)",
            font=dict(color="#1a237e"), height=280,
            xaxis=dict(
                title="Câmbio USD/BRL",
                gridcolor="rgba(21,101,192,0.2)", color="#1a237e"
            ),
            yaxis=dict(
                title="Custo Total (R$)",
                gridcolor="rgba(21,101,192,0.2)", color="#1a237e"
            ),
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_cambio, use_container_width=True)

        st.markdown(
            "<h4 style='color:#1565C0;'>"
            "📦 Economia de Escala por Volume</h4>",
            unsafe_allow_html=True
        )
        qtds           = list(range(int(cont_min), int(cont_max) + 1))
        custo_unit     = []
        custo_tot_list = []

        for q in qtds:
            taxas_q = (
                sum(v[cont_cenario] for v in TAXAS_PORTUARIAS.values())
                * q * cambio_atual
            )
            imp_q   = calcular_impostos(
                val_base + frete_base, cambio_atual, cat_base
            )
            total_q = imp_q["total_geral"] + taxas_q + 3500*q + 2800
            custo_unit.append(total_q / q)
            custo_tot_list.append(total_q)

        fig_vol = go.Figure()
        fig_vol.add_trace(go.Bar(
            x=qtds, y=custo_tot_list, name="Custo Total",
            marker_color="rgba(21,101,192,0.6)", yaxis="y"
        ))
        fig_vol.add_trace(go.Scatter(
            x=qtds, y=custo_unit, name="Custo Unitário",
            mode="lines+markers",
            line=dict(color="#f57f17", width=3),
            marker=dict(size=7), yaxis="y2"
        ))
        fig_vol.update_layout(
            paper_bgcolor="rgba(240,244,248,0.5)",
            plot_bgcolor="rgba(240,244,248,0.5)",
            font=dict(color="#1a237e"), height=280,
            xaxis=dict(
                title="Quantidade de Containers",
                gridcolor="rgba(21,101,192,0.2)", color="#1a237e"
            ),
            yaxis=dict(
                title="Custo Total (R$)",
                gridcolor="rgba(21,101,192,0.2)", color="#1a237e"
            ),
            yaxis2=dict(
                title="Custo Unitário (R$)",
                overlaying="y", side="right", color="#f57f17"
            ),
            legend=dict(
                bgcolor="rgba(240,244,248,0.8)",
                font=dict(color="#1a237e")
            ),
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_vol, use_container_width=True)

        # ── Tabela de cenários ──
        st.markdown(
            "<h4 style='color:#1565C0;'>📋 Tabela de Cenários</h4>",
            unsafe_allow_html=True
        )
        cenario_medio = (cambio_min + cambio_max) / 2
        cenarios = []
        for c, rotulo in [
            (cambio_min,    "🟢 Otimista"),
            (cenario_medio, "🟡 Base"),
            (cambio_max,    "🔴 Pessimista"),
        ]:
            imp_c = calcular_impostos(
                val_base + frete_base, c, cat_base
            )
            total_c = imp_c["total_geral"] + 3500 + 2800
            cenarios.append({
                "Cenário":          rotulo,
                "Câmbio":           f"R$ {c:.2f}",
                "Custo Total":      f"R$ {total_c:,.2f}",
                "Total Impostos":   f"R$ {imp_c['total_impostos']:,.2f}",
                "Carga Tributária": (
                    f"{(imp_c['total_impostos']/imp_c['valor_cif_brl'])*100:.1f}%"
                ),
            })
        st.dataframe(
            pd.DataFrame(cenarios),
            use_container_width=True,
            hide_index=True
        )


# ═══════════════════════════════════════════
# ABA 5 — RELATÓRIO FINAL
# ═══════════════════════════════════════════
with tab5:
    st.markdown("## 📄 Relatório Final da Operação")
    st.markdown("---")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        ref_numero  = st.text_input(
            "🔢 Nº da Proposta", "PP-2024-001", key="r_num"
        )
        cliente = st.text_input(
            "👤 Cliente", "Empresa ABC Ltda", key="r_cli"
        )
    with col_b:
        data_prop   = st.date_input(
            "📅 Data", date.today(), key="r_data"
        )
        responsavel = st.text_input(
            "🙋 Responsável", "João Silva", key="r_resp"
        )
    with col_c:
        validade = st.number_input(
            "⏳ Validade (dias)", 1, 90, 15, key="r_val"
        )

    st.markdown("---")

    cambio_rel = st.session_state.get("cambio_global", 5.20)
    val_rel    = st.session_state.get("val_mercadoria", 50000.0)
    frete_rel  = st.session_state.get("frete_maritimo",  2500.0)
    seg_rel    = val_rel * 0.003
    cif_rel    = val_rel + frete_rel + seg_rel
    cont_rel   = st.session_state.get("cont_tipo_rel", "20ft")
    cat_rel    = st.session_state.get("t3_cat", "Eletrônicos")
    imp_rel    = calcular_impostos(cif_rel, cambio_rel, cat_rel, 18.0)
    taxas_rel  = (
        sum(v[cont_rel] for v in TAXAS_PORTUARIAS.values())
        * cambio_rel
    )
    frod_rel  = st.session_state.get("frete_rodo", 3500.0)
    desp_rel  = st.session_state.get("despachante", 2800.0)
    total_rel = (
        imp_rel["total_geral"] + taxas_rel + frod_rel + desp_rel
    )

    st.info(
        f"**🚢 Porto Pricing Tool** — Proposta "
        f"**{html_lib.escape(str(ref_numero))}**\n\n"
        f"👤 Cliente: **{html_lib.escape(str(cliente))}** "
        f"· 🙋 Responsável: **{html_lib.escape(str(responsavel))}**\n\n"
        f"📅 Data: **{data_prop.strftime('%d/%m/%Y')}** "
        f"· ⏳ Válido por **{int(validade)} dias**\n\n"
        f"🚢 Operação: **Importação · Container {cont_rel} "
        f"· Categoria: {cat_rel}**\n\n"
        f"💱 Câmbio: **R$ {cambio_rel:.4f}** "
        f"(Yahoo Finance · ao vivo)"
    )

    st.markdown("---")
    st.markdown("### 💰 Resumo Executivo")

    carga_trib_pct        = (
        imp_rel["total_impostos"] / imp_rel["valor_cif_brl"]
    ) * 100
    total_taxas_logistica = taxas_rel + frod_rel + desp_rel
    total_usd_rel         = total_rel / cambio_rel

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(
        label="📦 Valor CIF",
        value=f"R$ {imp_rel['valor_cif_brl']:,.0f}",
        delta=f"USD {cif_rel:,.0f}"
    )
    k2.metric(
        label="🏛️ Total Impostos",
        value=f"R$ {imp_rel['total_impostos']:,.0f}",
        delta=f"{carga_trib_pct:.1f}% sobre CIF",
        delta_color="inverse"
    )
    k3.metric(
        label="🏭 Taxas & Logística",
        value=f"R$ {total_taxas_logistica:,.0f}"
    )
    k4.metric(
        label="💰 TOTAL GERAL",
        value=f"R$ {total_rel:,.0f}",
        delta=f"≈ USD {total_usd_rel:,.0f}"
    )

    st.markdown("---")
    st.markdown("### 📋 Composição Detalhada de Custos")

    valores_brutos = [
        imp_rel["valor_cif_brl"],
        imp_rel["II"],       imp_rel["IPI"],
        imp_rel["PIS"],      imp_rel["COFINS"],
        imp_rel["ICMS"],     imp_rel["AFRMM"],
        imp_rel["Siscomex"],
        taxas_rel, frod_rel, desp_rel,
    ]
    ii_pct     = ALIQUOTAS_NCM[cat_rel]["II"]
    ipi_pct    = ALIQUOTAS_NCM[cat_rel]["IPI"]
    nomes = [
        "Valor da Mercadoria (CIF)",
        f"Imposto de Importação (II) — {ii_pct}%",
        f"IPI — {ipi_pct}%",
        "PIS Importação — 2,1%",
        "COFINS Importação — 9,65%",
        "ICMS Importação — 18%",
        "AFRMM — Marinha Mercante 8%",
        "Siscomex (fixo)",
        "Taxas Portuárias (THC + BL + ISPS + Capatazia)",
        "Frete Rodoviário",
        "Despachante Aduaneiro",
    ]
    categorias_rel = [
        "📦 Mercadoria",
        "🏛️ Imposto", "🏛️ Imposto",
        "🏛️ Imposto", "🏛️ Imposto",
        "🏛️ Imposto", "⚓ Taxa Federal",
        "💻 Taxa Federal",
        "🏭 Taxa Portuária",
        "🚛 Logística",
        "📋 Serviço",
    ]

    df = pd.DataFrame({
        "Item":       nomes,
        "Categoria":  categorias_rel,
        "Valor (R$)": [f"R$ {v:,.2f}" for v in valores_brutos],
        "% do Total": [
            f"{v/total_rel*100:.1f}%" for v in valores_brutos
        ],
    })

    st.dataframe(
        df, use_container_width=True, hide_index=True,
        column_config={
            "Item":       st.column_config.TextColumn(
                "📋 Item",         width="large"
            ),
            "Categoria":  st.column_config.TextColumn(
                "🏷️ Categoria",   width="medium"
            ),
            "Valor (R$)": st.column_config.TextColumn(
                "💰 Valor",        width="medium"
            ),
            "% do Total": st.column_config.TextColumn(
                "📊 Participação", width="small"
            ),
        }
    )

    # ── Export Excel ──
    try:
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Custos", index=False)
        buffer.seek(0)
        st.download_button(
            label="📥 Exportar Excel",
            data=buffer,
            file_name=f"proposta_{ref_numero}.xlsx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            )
        )
    except ImportError:
        st.caption(
            "💡 Instale openpyxl para habilitar o export: "
            "`pip install openpyxl`"
        )

    st.markdown("---")
    st.markdown("### 📊 Composição Visual dos Custos")

    labels_rel = [
        "CIF", "II", "IPI", "PIS", "COFINS", "ICMS",
        "AFRMM", "Siscomex", "Portuário", "Rodoviário", "Despachante"
    ]
    colors_rel = [
        "#1E88E5", "#e53935", "#fb8c00", "#43a047", "#00897b",
        "#8e24aa", "#00acc1", "#6d4c41", "#f4511e", "#3949ab", "#546e7a"
    ]
    fig_pizza = go.Figure(data=[go.Pie(
        labels=labels_rel, values=valores_brutos,
        marker=dict(colors=colors_rel),
        hole=0.4,
        textinfo="label+percent",
        textfont=dict(color="#1a1a1a", size=13)
    )])
    fig_pizza.update_layout(
        paper_bgcolor="rgba(240,244,248,0.5)",
        plot_bgcolor="rgba(240,244,248,0.5)",
        font=dict(color="#1a237e", size=14),
        height=420, showlegend=True,
        legend=dict(font=dict(color="#1a237e", size=13)),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

    st.markdown("---")
    st.success(
        f"### 🏆 VALOR TOTAL DA OPERAÇÃO: R$ {total_rel:,.2f}\n\n"
        f"≈ **USD {total_usd_rel:,.2f}** "
        f"· Câmbio: **R$ {cambio_rel:.4f}** "
        f"· Data: {date.today().strftime('%d/%m/%Y')}"
    )

    st.markdown("---")
    st.markdown("### 📜 Histórico de Cotações Salvas")

    if "cotacoes" in st.session_state and st.session_state.cotacoes:
        df_hist_cot = pd.DataFrame(st.session_state.cotacoes)
        st.dataframe(
            df_hist_cot, use_container_width=True, hide_index=True
        )
        if st.button("🗑️ Limpar Histórico", key="r_clear"):
            st.session_state.cotacoes = []
            st.rerun()
    else:
        st.info(
            "📭 Nenhuma cotação salva ainda. "
            "Vá em **💰 Custos & Fretes** "
            "e clique em **💾 Salvar Cotação**."
        )

    st.markdown("---")
    st.warning(
        "⚠️ **Aviso:** Valores calculados com base em dados "
        "aproximados. Consulte sempre um despachante aduaneiro "
        "habilitado para operações reais."
    )
    st.caption(
        "🚢 Porto Pricing Tool · ⚓ Porto de Santos, SP · "
        "Streamlit + Plotly + Yahoo Finance + OpenWeatherMap 🚀"
    )


# ═══════════════════════════════════════════
# ABA 6 — PREVISÃO DO TEMPO 5 DIAS
# ═══════════════════════════════════════════
with tab6:
    st.markdown(
        "<h2 style='color:#1565C0;'>"
        "🌦️ Previsão Meteorológica Portuária — 5 Dias</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='info-box'>
        ⚓ <b>Por que isso importa?</b> Condições climáticas afetam
        diretamente operações de carga/descarga, disponibilidade de
        guindastes, janelas de atracação, segurança da carga a granel
        e prazos de entrega. Monitore sempre <b>origem e destino</b>
        antes de confirmar um embarque.
    </div>
    """, unsafe_allow_html=True)

    # ── Lê cidades da Aba 2 ──
    cidade_origem  = st.session_state.get("t2_orig",  "Shanghai")
    cidade_destino = st.session_state.get("t2_dest",  "Santos")

    st.markdown(f"""
    <div style='background:#e3f2fd;border-radius:10px;
                padding:12px 18px;margin-bottom:16px;
                border:1px solid #90caf9;'>
        📍 Usando cidades definidas na aba
        <b>💰 Custos & Fretes</b>: &nbsp;
        <b style='color:#1565C0;'>📤 {cidade_origem}</b>
        &nbsp;→&nbsp;
        <b style='color:#1565C0;'>📥 {cidade_destino}</b>
        <br>
        <small style='color:#546e7a;'>
            Altere as cidades na aba Custos & Fretes
            para atualizar a previsão automaticamente.
        </small>
    </div>
    """, unsafe_allow_html=True)

    # ── Verificação da chave ──
    chave_configurada = (
        bool(OPENWEATHER_API_KEY)
        and OPENWEATHER_API_KEY != "COLE_SUA_CHAVE_AQUI"
        and len(OPENWEATHER_API_KEY) > 10
    )

    if not chave_configurada:
        st.error(
            "🔑 **API Key não configurada!**\n\n"
            "Abra o arquivo `.py` e edite a linha no topo:\n\n"
            "```python\n"
            "OPENWEATHER_API_KEY = \"COLE_SUA_CHAVE_AQUI\"\n"
            "```\n\n"
            "Chave gratuita em: https://openweathermap.org/api"
        )
    else:
        col_f1, col_f2 = st.columns(2)

        # ── ORIGEM ──
        with col_f1:
            with st.spinner(
                f"🌍 Carregando forecast {cidade_origem}..."
            ):
                forecast_orig, err_orig = get_forecast_5dias(
                    cidade_origem, OPENWEATHER_API_KEY
                )
            if err_orig:
                st.error(f"❌ {cidade_origem}: {err_orig}")
            else:
                render_forecast_cards(
                    forecast_orig,
                    f"📤 Origem · {cidade_origem}"
                )

        # ── DESTINO ──
        with col_f2:
            with st.spinner(
                f"🌍 Carregando forecast {cidade_destino}..."
            ):
                forecast_dest, err_dest = get_forecast_5dias(
                    cidade_destino, OPENWEATHER_API_KEY
                )
            if err_dest:
                st.error(f"❌ {cidade_destino}: {err_dest}")
            else:
                render_forecast_cards(
                    forecast_dest,
                    f"📥 Destino · {cidade_destino}"
                )

        st.markdown("---")

        # ── Alertas Operacionais ──
        st.markdown(
            "<h4 style='color:#1565C0;'>🚨 Alertas Operacionais</h4>",
            unsafe_allow_html=True
        )

        alertas = []
        for label, forecast, err in [
            (cidade_origem,
             forecast_orig if not err_orig else None, err_orig),
            (cidade_destino,
             forecast_dest if not err_dest else None, err_dest),
        ]:
            if not forecast:
                continue
            for dia_key, dia in forecast.items():
                if dia["aviso"]:
                    alertas.append({
                        "📍 Local":     label,
                        "📅 Data":      f"{dia['semana']} {dia['label']}",
                        "🌤️ Condição": dia["descricao"].capitalize(),
                        "⚠️ Alerta":    dia["aviso"],
                        "🌡️ Máx":      f"{dia['temp_max']:.0f}°C",
                        "🌧️ Chuva":    f"{dia['chuva_total']:.1f} mm",
                        "🌬️ Vento":    f"{dia['vento']} km/h",
                    })

        if alertas:
            df_alertas = pd.DataFrame(alertas)
            st.dataframe(
                df_alertas,
                use_container_width=True,
                hide_index=True
            )

            # ── Impacto financeiro estimado ──
            n_alertas_graves = sum(
                1 for a in alertas
                if "paralisação" in a["⚠️ Alerta"].lower()
                or "suspensas"   in a["⚠️ Alerta"].lower()
            )
            if n_alertas_graves > 0:
                custo_dia_parado = 15000
                dias_risco       = n_alertas_graves
                custo_estimado   = custo_dia_parado * dias_risco
                st.markdown(f"""
                <div style='background:#ffebee;
                            border:2px solid #c62828;
                            border-radius:12px;
                            padding:16px;margin-top:12px;'>
                    <b style='color:#c62828;font-size:16px;'>
                        🚨 Risco de Paralisação Portuária
                    </b><br>
                    <span style='color:#37474f;font-size:14px;'>
                        {dias_risco} dia(s) com risco detectado(s)
                        na rota.<br>
                        Custo estimado por dia parado:
                        <b>R$ {custo_dia_parado:,.0f}</b>
                        (demurrage + armazenagem + lucro cessante).<br>
                        Custo total estimado:
                        <b style='color:#c62828;'>
                            R$ {custo_estimado:,.0f}
                        </b><br>
                        ⚡ Acione seu seguro de carga e
                        notifique o armador imediatamente.
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success(
                "✅ Nenhum alerta operacional identificado "
                "para os próximos 5 dias nas rotas selecionadas."
            )

        st.markdown("---")

        # ── Índices de referência ──
        st.markdown(
            "<h4 style='color:#1565C0;'>"
            "📊 Referências do Mercado</h4>",
            unsafe_allow_html=True
        )
        ref1, ref2, ref3, ref4 = st.columns(4)
        ref1.metric("🌊 WCI (Drewry)",  "USD 1.847/FEU", "−3.2% semana")
        ref2.metric("📦 SCFI",          "2.143 pts",     "+1.1% semana")
        ref3.metric("🚢 BDI",           "1.892 pts",     "−0.8% semana")
        ref4.metric("⛽ Bunker VLSFO",  "USD 612/ton",   "+2.3% semana")
        st.caption(
            "⚠️ Índices ilustrativos — integre com API de mercado "
            "(Drewry, Baltic Exchange) para dados reais."
        )

        st.markdown("---")

        # ── Botões de ação ──
        col_btn1, col_btn2, _ = st.columns([1, 1, 3])
        with col_btn1:
            if st.button(
                "🔄 Atualizar Previsão", key="btn_fc_refresh"
            ):
                st.cache_data.clear()
                st.rerun()
        with col_btn2:
            st.caption(
                "⏱️ Cache: 60 min · Powered by OpenWeatherMap"
            )

    st.markdown("---")
    st.caption(
        "🚢 Porto Pricing Tool · ⚓ Porto de Santos, SP · "
        "Streamlit + Plotly + Yahoo Finance + OpenWeatherMap 🚀"
    )
