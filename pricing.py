import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dataclasses import dataclass
from datetime import datetime, date
import requests

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
        background-image: 
            linear-gradient(rgba(5,10,30,0.82), rgba(5,10,30,0.82)),
            url("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Porto_de_Santos.jpg/1280px-Porto_de_Santos.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }

    .hero-banner {
        background-image: 
            linear-gradient(rgba(5,10,30,0.55), rgba(5,10,30,0.90)),
            url("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Porto_de_Santos.jpg/1280px-Porto_de_Santos.jpg");
        background-size: cover;
        background-position: center top;
        border-radius: 20px;
        padding: 50px 40px 40px 40px;
        margin-bottom: 20px;
        border: 1px solid rgba(100,181,246,0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.6);
    }

    .hero-title {
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #64B5F6, #42A5F5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
    }

    .hero-subtitle {
        color: #B3D9F7;
        font-size: 18px;
        margin-top: 10px;
        font-weight: 300;
        letter-spacing: 1px;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(100,181,246,0.2);
        border: 1px solid rgba(100,181,246,0.5);
        color: #64B5F6;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 4px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .metric-card {
        background: linear-gradient(135deg,
            rgba(30,58,95,0.85),
            rgba(45,90,142,0.85));
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(61,122,181,0.6);
        text-align: center;
        margin: 5px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #64B5F6;
    }

    .metric-label {
        font-size: 13px;
        color: #90CAF9;
        margin-top: 5px;
    }

    .content-section {
        background: rgba(10,14,30,0.75);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(45,90,142,0.4);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }

    .info-box {
        background: rgba(30,58,95,0.7);
        padding: 14px;
        border-radius: 10px;
        font-size: 13px;
        color: #90CAF9;
        border: 1px solid rgba(61,122,181,0.3);
        backdrop-filter: blur(5px);
    }

    .porto-tag {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30,58,95,0.8);
        border: 1px solid rgba(100,181,246,0.4);
        border-radius: 25px;
        padding: 5px 14px;
        font-size: 12px;
        color: #64B5F6;
        letter-spacing: 1px;
    }

    .custo-card {
        background: linear-gradient(135deg,
            rgba(20,40,80,0.9),
            rgba(30,60,100,0.9));
        padding: 18px;
        border-radius: 12px;
        border-left: 4px solid #64B5F6;
        margin: 8px 0;
        backdrop-filter: blur(10px);
    }

    .custo-card-green {
        border-left: 4px solid #44cc88 !important;
    }

    .custo-card-yellow {
        border-left: 4px solid #ffcc44 !important;
    }

    .custo-card-red {
        border-left: 4px solid #ff4444 !important;
    }

    .total-card {
        background: linear-gradient(135deg, #1E88E5, #1565C0);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(30,136,229,0.4);
        margin: 15px 0;
    }

    div[data-testid="stSidebarContent"] {
        background: linear-gradient(180deg,
            rgba(10,20,40,0.97) 0%,
            rgba(15,30,60,0.97) 100%);
        border-right: 1px solid rgba(45,90,142,0.5);
    }

    .stSelectbox label,
    .stSlider label,
    .stNumberInput label,
    .stTextInput label {
        color: #90CAF9 !important;
    }

    hr { border-color: rgba(45,90,142,0.4) !important; }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10,14,30,0.8);
        border-radius: 12px;
        padding: 5px;
        gap: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(30,58,95,0.6);
        border-radius: 8px;
        color: #90CAF9;
        font-weight: 600;
        padding: 10px 20px;
        border: 1px solid rgba(61,122,181,0.3);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E88E5, #1565C0) !important;
        color: white !important;
    }
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
    "📦 Container 20ft":    Container("20ft",    589,  235, 239, 28200),
    "📦 Container 40ft":    Container("40ft",    1203, 235, 239, 26700),
    "📦 Container 40ft HC": Container("40ft HC", 1203, 235, 269, 26580),
}

CAIXAS = {
    "🔴 Pequena (30×20×15cm)": Caixa("Pequena", 30,  20, 15, 2.5,
                                      "rgba(255,100,100,0.7)", "#ff4444"),
    "🔵 Média (50×40×30cm)":   Caixa("Média",   50,  40, 30, 8.0,
                                      "rgba(100,180,255,0.7)", "#4488ff"),
    "🟢 Grande (80×60×50cm)":  Caixa("Grande",  80,  60, 50, 20.0,
                                      "rgba(100,220,150,0.7)", "#44cc88"),
    "🟡 XL (100×80×70cm)":    Caixa("XL",      100, 80, 70, 35.0,
                                      "rgba(255,220,100,0.7)", "#ffcc44"),
    "🟣 Custom":               Caixa("Custom",  40,  30, 25, 5.0,
                                      "rgba(200,100,255,0.7)", "#cc44ff"),
}

# Taxas portuárias fictícias (baseadas em valores reais aproximados)
TAXAS_PORTUARIAS = {
    "THC - Terminal Handling Charge": {"20ft": 650, "40ft": 850, "40ft HC": 900},
    "BL Fee - Bill of Lading":        {"20ft": 150, "40ft": 150, "40ft HC": 150},
    "ISPS - Segurança Portuária":     {"20ft": 45,  "40ft": 55,  "40ft HC": 55 },
    "Capatazia":                      {"20ft": 380, "40ft": 520, "40ft HC": 560},
    "Liberação do Container":         {"20ft": 220, "40ft": 280, "40ft HC": 280},
}

# Alíquotas de impostos (fictícias para demonstração)
ALIQUOTAS_NCM = {
    "Eletrônicos":          {"II": 14.0, "IPI": 10.0, "PIS": 2.1, "COFINS": 9.65},
    "Vestuário":            {"II": 20.0, "IPI": 0.0,  "PIS": 2.1, "COFINS": 9.65},
    "Alimentos":            {"II": 10.0, "IPI": 0.0,  "PIS": 2.1, "COFINS": 9.65},
    "Máquinas/Equipamentos":{"II": 12.0, "IPI": 5.0,  "PIS": 2.1, "COFINS": 9.65},
    "Químicos":             {"II": 8.0,  "IPI": 0.0,  "PIS": 2.1, "COFINS": 9.65},
    "Automóveis":           {"II": 35.0, "IPI": 25.0, "PIS": 2.1, "COFINS": 9.65},
    "Personalizado":        {"II": 0.0,  "IPI": 0.0,  "PIS": 2.1, "COFINS": 9.65},
}


# ─────────────────────────────
# FUNÇÕES - CONTAINER 3D
# ─────────────────────────────
def criar_caixa_3d(x, y, z, dx, dy, dz, cor, cor_borda, opacidade=0.75):
    vx = [x,    x+dx, x+dx, x,    x,    x+dx, x+dx, x   ]
    vy = [y,    y,    y+dy, y+dy, y,    y,    y+dy, y+dy ]
    vz = [z,    z,    z,    z,    z+dz, z+dz, z+dz, z+dz ]
    i_idx = [0,0,0,0,4,4,3,3,1,1,2,2]
    j_idx = [1,2,4,5,5,6,7,6,2,5,3,6]
    k_idx = [2,3,5,6,6,7,6,2,5,6,6,7]

    mesh = go.Mesh3d(
        x=vx, y=vy, z=vz,
        i=i_idx, j=j_idx, k=k_idx,
        color=cor, opacity=opacidade,
        flatshading=True,
        lighting=dict(ambient=0.6, diffuse=0.9,
                      specular=0.3, roughness=0.5, fresnel=0.2),
        lightposition=dict(x=1000, y=1000, z=1000),
        showscale=False, hoverinfo='skip'
    )

    arestas = [(0,1),(1,2),(2,3),(3,0),
               (4,5),(5,6),(6,7),(7,4),
               (0,4),(1,5),(2,6),(3,7)]
    ex, ey, ez = [], [], []
    for (a, b) in arestas:
        ex += [vx[a], vx[b], None]
        ey += [vy[a], vy[b], None]
        ez += [vz[a], vz[b], None]

    bordas = go.Scatter3d(
        x=ex, y=ey, z=ez, mode='lines',
        line=dict(color=cor_borda, width=2),
        hoverinfo='skip', showlegend=False
    )
    return mesh, bordas


def criar_container_wireframe(container: Container):
    c = container
    traces = []
    faces = go.Mesh3d(
        x=[0,c.comp,c.comp,0,     0,     c.comp,c.comp,0    ],
        y=[0,0,     c.larg,c.larg,0,     0,     c.larg,c.larg],
        z=[0,0,     0,     0,     c.alt, c.alt, c.alt, c.alt ],
        i=[0,0,0,0,4,4], j=[1,2,4,5,5,6], k=[2,3,5,6,6,7],
        opacity=0.08, color='#64B5F6',
        flatshading=True, showscale=False,
        hoverinfo='skip', name='Container'
    )
    traces.append(faces)

    vx=[0,c.comp,c.comp,0,     0,     c.comp,c.comp,0    ]
    vy=[0,0,     c.larg,c.larg,0,     0,     c.larg,c.larg]
    vz=[0,0,     0,     0,     c.alt, c.alt, c.alt, c.alt ]
    arestas=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
             (0,4),(1,5),(2,6),(3,7)]
    ex,ey,ez=[],[],[]
    for (a,b) in arestas:
        ex+=[vx[a],vx[b],None]
        ey+=[vy[a],vy[b],None]
        ez+=[vz[a],vz[b],None]

    traces.append(go.Scatter3d(
        x=ex,y=ey,z=ez,mode='lines',
        line=dict(color='#64B5F6',width=3),
        name='Container',hoverinfo='skip'
    ))
    return traces


def calcular_e_plotar(container, caixa, percentual=100):
    qtd_c = int(container.comp / caixa.comp)
    qtd_l = int(container.larg / caixa.larg)
    qtd_a = int(container.alt  / caixa.alt )
    total_vol   = qtd_c * qtd_l * qtd_a
    max_peso    = int(container.peso_max / caixa.peso)
    total_real  = min(total_vol, max_peso)
    qtd_mostrar = int(total_real * percentual / 100)

    all_traces = []
    all_traces.extend(criar_container_wireframe(container))

    count = 0
    for az in range(qtd_a):
        for al in range(qtd_l):
            for ac in range(qtd_c):
                if count >= qtd_mostrar:
                    break
                x = ac * caixa.comp
                y = al * caixa.larg
                z = az * caixa.alt
                opacidade = max(0.5, 0.85 - (az * 0.04))
                mesh, bordas = criar_caixa_3d(
                    x,y,z,
                    caixa.comp,caixa.larg,caixa.alt,
                    caixa.cor,caixa.cor_borda,opacidade
                )
                all_traces.append(mesh)
                all_traces.append(bordas)
                count += 1
            if count >= qtd_mostrar: break
        if count >= qtd_mostrar: break

    fig = go.Figure(data=all_traces)
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title=dict(text='Comprimento (cm)',font=dict(color='#90CAF9')),
                backgroundcolor='rgba(5,10,30,0.8)',
                gridcolor='rgba(45,90,142,0.5)',
                showbackground=True, zerolinecolor='#2d5a8e',
                tickfont=dict(color='#90CAF9')
            ),
            yaxis=dict(
                title=dict(text='Largura (cm)',font=dict(color='#90CAF9')),
                backgroundcolor='rgba(5,10,30,0.8)',
                gridcolor='rgba(45,90,142,0.5)',
                showbackground=True, zerolinecolor='#2d5a8e',
                tickfont=dict(color='#90CAF9')
            ),
            zaxis=dict(
                title=dict(text='Altura (cm)',font=dict(color='#90CAF9')),
                backgroundcolor='rgba(5,10,30,0.8)',
                gridcolor='rgba(45,90,142,0.5)',
                showbackground=True, zerolinecolor='#2d5a8e',
                tickfont=dict(color='#90CAF9')
            ),
            bgcolor='rgba(5,10,30,0.85)',
            camera=dict(eye=dict(x=1.8,y=-1.8,z=1.2),
                        up=dict(x=0,y=0,z=1)),
            aspectmode='data'
        ),
        paper_bgcolor='rgba(5,10,30,0.5)',
        plot_bgcolor='rgba(5,10,30,0.5)',
        margin=dict(l=0,r=0,t=0,b=0),
        height=600, showlegend=False
    )

    vol_pct  = (total_real * caixa.comp * caixa.larg * caixa.alt) / \
               (container.comp * container.larg * container.alt) * 100
    peso_pct = (total_real * caixa.peso / container.peso_max) * 100

    return fig, {
        'total': total_real, 'mostradas': qtd_mostrar,
        'qtd_c': qtd_c, 'qtd_l': qtd_l, 'qtd_a': qtd_a,
        'peso_total': total_real * caixa.peso,
        'vol_pct': vol_pct, 'peso_pct': peso_pct,
        'limitador': 'Peso ⚖️' if max_peso < total_vol else 'Volume 📦'
    }


# ─────────────────────────────
# FUNÇÕES - PRICING
# ─────────────────────────────
def get_cambio_usd():
    """Tenta buscar câmbio real do Banco Central"""
    try:
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        resp = requests.get(url, timeout=3)
        data = resp.json()
        return float(data['USDBRL']['bid'])
    except:
        return 5.05  # fallback fictício


def calcular_impostos(valor_cif_usd, cambio, categoria, icms_estado=18.0):
    """
    Calcula impostos de importação em cascata
    Fórmula correta conforme legislação brasileira
    """
    aliq = ALIQUOTAS_NCM[categoria]
    valor_cif_brl = valor_cif_usd * cambio

    # AFRMM - 25% do frete marítimo (simplificado como 8% do CIF)
    afrmm = valor_cif_brl * 0.08

    # Base II
    base_ii = valor_cif_brl
    ii = base_ii * (aliq["II"] / 100)

    # Base IPI = CIF + II
    base_ipi = valor_cif_brl + ii
    ipi = base_ipi * (aliq["IPI"] / 100)

    # PIS e COFINS
    pis    = valor_cif_brl * (aliq["PIS"]    / 100)
    cofins = valor_cif_brl * (aliq["COFINS"] / 100)

    # ICMS = calculado "por dentro"
    # ICMS = (CIF + II + IPI + PIS + COFINS + AFRMM) / (1 - aliq_icms) * aliq_icms
    soma_antes_icms = valor_cif_brl + ii + ipi + pis + cofins + afrmm
    icms = soma_antes_icms / (1 - icms_estado/100) * (icms_estado/100)

    # Siscomex
    siscomex = 214.50

    total_impostos = ii + ipi + pis + cofins + icms + afrmm + siscomex
    total_geral    = valor_cif_brl + total_impostos

    return {
        "valor_cif_brl":  valor_cif_brl,
        "II":             ii,
        "IPI":            ipi,
        "PIS":            pis,
        "COFINS":         cofins,
        "ICMS":           icms,
        "AFRMM":          afrmm,
        "Siscomex":       siscomex,
        "total_impostos": total_impostos,
        "total_geral":    total_geral,
        "aliquotas":      aliq,
        "icms_estado":    icms_estado,
    }


# ─────────────────────────────
# HERO BANNER
# ─────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
        <div>
            <div class='porto-tag'>⚓ Porto de Santos — SP, Brasil</div>
            <h1 class='hero-title' style='margin-top:14px;'>
                🚢 Porto Pricing Tool
            </h1>
            <p class='hero-subtitle'>
                Plataforma completa de otimização de carga e precificação portuária
            </p>
            <div style='margin-top:15px;'>
                <span class='hero-badge'>📦 3D Container</span>
                <span class='hero-badge'>💰 Custos & Fretes</span>
                <span class='hero-badge'>🛃 Impostos</span>
                <span class='hero-badge'>📊 Cenários</span>
                <span class='hero-badge'>📄 Relatório</span>
            </div>
        </div>
        <div style='font-size:70px;opacity:0.5;'>🚢</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────
# ABAS PRINCIPAIS
# ─────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📦 Container 3D",
    "💰 Custos & Fretes",
    "🛃 Impostos",
    "📊 Simulador de Cenários",
    "📄 Relatório Final"
])


# ═══════════════════════════════════════════
# ABA 1 — CONTAINER 3D (código original)
# ═══════════════════════════════════════════
with tab1:

    col_main, col_side = st.columns([3, 1])

    with col_side:
        st.markdown("<h3 style='color:#64B5F6;'>⚙️ Configurações</h3>",
                    unsafe_allow_html=True)

        container_nome = st.selectbox("🚢 Tipo de Container",
                                      list(CONTAINERS.keys()), key="t1_cont")
        container = CONTAINERS[container_nome]

        caixa_nome = st.selectbox("📦 Tipo de Caixa",
                                  list(CAIXAS.keys()), key="t1_caixa")
        caixa = CAIXAS[caixa_nome]

        if "Custom" in caixa_nome:
            st.markdown("#### 🔧 Dimensões")
            c_comp = st.slider("Comprimento (cm)", 10, 200, 40, key="cc")
            c_larg = st.slider("Largura (cm)",     10, 200, 30, key="cl")
            c_alt  = st.slider("Altura (cm)",      10, 200, 25, key="ca")
            c_peso = st.slider("Peso (kg)",         1, 500,  5, key="cp")
            caixa  = Caixa("Custom", c_comp, c_larg, c_alt, c_peso,
                            "rgba(200,100,255,0.7)", "#cc44ff")

        percentual = st.slider("🔄 Percentual de Carga",
                               0, 100, 100, 5, key="t1_perc",
                               help="Simule diferentes níveis de preenchimento")

        st.markdown("---")
        st.markdown(f"""
        <div class='info-box'>
            <b>📐 Container:</b> {container.tipo}<br>
            {container.comp}×{container.larg}×{container.alt} cm<br>
            Vol: {container.comp*container.larg*container.alt/1e6:.1f} m³<br>
            Carga Máx: {container.peso_max:,} kg
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='info-box' style='margin-top:10px;'>
            <b>📦 Caixa:</b> {caixa.nome}<br>
            {caixa.comp}×{caixa.larg}×{caixa.alt} cm<br>
            Vol: {caixa.comp*caixa.larg*caixa.alt/1e6:.4f} m³<br>
            Peso: {caixa.peso} kg
        </div>
        """, unsafe_allow_html=True)

    with col_main:
        fig, stats = calcular_e_plotar(container, caixa, percentual)

        # Métricas
        m1, m2, m3, m4, m5 = st.columns(5)
        for col, icon, val, label in [
            (m1, "📦", stats['total'],           "Total Caixas"),
            (m2, "✅", stats['mostradas'],        "Carregadas"),
            (m3, "📐", f"{stats['vol_pct']:.1f}%","Vol. Utilizado"),
            (m4, "⚖️", f"{stats['peso_total']:,.0f}","Peso (kg)"),
            (m5, "🎯", stats['limitador'],        "Limitante"),
        ]:
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size:22px;'>{icon}</div>
                    <div class='metric-value'>{val}</div>
                    <div class='metric-label'>{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <p style='color:#90CAF9;font-size:13px;'>
        💡 <b>Dica:</b> Arraste para rotacionar | Scroll para zoom | Duplo clique para resetar
        </p>""", unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True)

        # Barras de progresso
        p1, p2 = st.columns(2)
        with p1:
            st.markdown("<p style='color:#90CAF9;'>📦 Volume Utilizado</p>",
                        unsafe_allow_html=True)
            st.progress(min(stats['vol_pct']/100, 1.0))
            st.markdown(f"<b style='color:#64B5F6;'>{stats['vol_pct']:.1f}%</b>",
                        unsafe_allow_html=True)
        with p2:
            st.markdown("<p style='color:#90CAF9;'>⚖️ Peso Utilizado</p>",
                        unsafe_allow_html=True)
            st.progress(min(stats['peso_pct']/100, 1.0))
            st.markdown(f"<b style='color:#64B5F6;'>{stats['peso_pct']:.1f}%</b>",
                        unsafe_allow_html=True)

        # Arranjo espacial
        st.markdown("---")
        st.markdown("<h4 style='color:#64B5F6;'>📐 Arranjo Espacial</h4>",
                    unsafe_allow_html=True)
        a1, a2, a3 = st.columns(3)
        for col, icon, val, label in [
            (a1, "↔️", stats['qtd_c'], "Colunas"),
            (a2, "↕️", stats['qtd_l'], "Fileiras"),
            (a3, "🔝", stats['qtd_a'], "Camadas"),
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
    st.markdown("<h2 style='color:#64B5F6;'>💰 Calculadora de Custos & Fretes</h2>",
                unsafe_allow_html=True)

    # Câmbio
    cambio_atual = get_cambio_usd()
    c1, c2 = st.columns([2,1])
    with c1:
        st.markdown(f"""
        <div class='info-box'>
            💱 <b>Câmbio USD/BRL em tempo real:</b>
            <span style='color:#64B5F6; font-size:20px; font-weight:bold;'>
            R$ {cambio_atual:.4f}
            </span>
            &nbsp;&nbsp;
            <span style='color:#90CAF9; font-size:12px;'>
            (via AwesomeAPI / Banco Central)
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_form, col_result = st.columns([1, 1])

    with col_form:

        st.markdown("<h4 style='color:#64B5F6;'>🚢 Dados do Embarque</h4>",
                    unsafe_allow_html=True)

        tipo_op = st.selectbox("Tipo de Operação",
                               ["Importação", "Exportação"], key="t2_op")

        cont_tipo = st.selectbox("Tipo de Container",
                                 ["20ft", "40ft", "40ft HC"], key="t2_cont")

        qtd_containers = st.number_input("Quantidade de Containers",
                                         min_value=1, value=1, key="t2_qtd")

        origem = st.text_input("Porto de Origem", "Shanghai, China", key="t2_orig")
        destino = st.text_input("Porto de Destino", "Santos, Brasil", key="t2_dest")

        st.markdown("---")
        st.markdown("<h4 style='color:#64B5F6;'>💵 Valores (USD)</h4>",
                    unsafe_allow_html=True)

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
            min_value=0.0, max_value=3.0,
            value=0.3, step=0.05, key="t2_seg"
        )

        st.markdown("---")
        st.markdown("<h4 style='color:#64B5F6;'>🚛 Logística Interna</h4>",
                    unsafe_allow_html=True)

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
            min_value=1.0, value=cambio_atual,
            format="%.4f", key="t2_cambio"
        )

    with col_result:

        st.markdown("<h4 style='color:#64B5F6;'>📊 Resumo de Custos</h4>",
                    unsafe_allow_html=True)

        # Cálculos
        seguro_usd    = valor_mercadoria * (seguro_pct / 100)
        valor_cif_usd = valor_mercadoria + frete_maritimo + seguro_usd
        valor_cif_brl = valor_cif_usd * cambio_usado

        # Taxas portuárias
        taxas_dict = TAXAS_PORTUARIAS
        total_taxas_usd = sum(
            v[cont_tipo] for v in taxas_dict.values()
        ) * qtd_containers
        total_taxas_brl = total_taxas_usd * cambio_usado

        # Armazenagem escalonada (fictícia)
        if armazenagem_dias <= 5:
            armazenagem_brl = armazenagem_dias * 180
        elif armazenagem_dias <= 10:
            armazenagem_brl = 5*180 + (armazenagem_dias-5) * 280
        else:
            armazenagem_brl = 5*180 + 5*280 + (armazenagem_dias-10) * 420

        armazenagem_brl *= qtd_containers

        # Total geral
        total_brl = (valor_cif_brl + total_taxas_brl +
                     armazenagem_brl + frete_rodoviario + despachante)

        # Cards de custos
        itens = [
            ("🌊 Frete Marítimo", frete_maritimo * cambio_usado,
             f"USD {frete_maritimo:,.2f} × {cambio_usado:.4f}", "custo-card"),
            ("🛡️ Seguro de Carga", seguro_usd * cambio_usado,
             f"{seguro_pct}% sobre mercadoria", "custo-card"),
            ("🏭 Taxas Portuárias", total_taxas_brl,
             f"THC + BL + ISPS + Capatazia × {qtd_containers} cont.", "custo-card-yellow"),
            ("🏗️ Armazenagem", armazenagem_brl,
             f"{armazenagem_dias} dias (escalonado)", "custo-card-yellow"),
            ("🚛 Frete Rodoviário", frete_rodoviario,
             "Porto → Destino final", "custo-card-green"),
            ("📋 Despachante", despachante,
             "Serviços aduaneiros", "custo-card-green"),
        ]

        for nome, valor, detalhe, classe in itens:
            st.markdown(f"""
            <div class='custo-card {classe}'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <b style='color:#E8F4FD;'>{nome}</b><br>
                        <small style='color:#90CAF9;'>{detalhe}</small>
                    </div>
                    <div style='font-size:20px;font-weight:bold;color:#64B5F6;'>
                        R$ {valor:,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Total
        st.markdown(f"""
        <div class='total-card'>
            <p style='color:#B3D9F7;margin:0;font-size:14px;'>CUSTO TOTAL DA OPERAÇÃO</p>
            <h1 style='color:white;margin:8px 0;font-size:44px;'>
                R$ {total_brl:,.2f}
            </h1>
            <p style='color:#90CAF9;margin:0;font-size:13px;'>
                ≈ USD {total_brl/cambio_usado:,.2f} | 
                R$ {total_brl/qtd_containers:,.2f} por container
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Detalhamento taxas portuárias
        with st.expander("📋 Detalhamento Taxas Portuárias"):
            for taxa, valores in taxas_dict.items():
                val_taxa = valores[cont_tipo] * cambio_usado * qtd_containers
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;
                            padding:8px;border-bottom:1px solid rgba(45,90,142,0.3);'>
                    <span style='color:#90CAF9;'>{taxa}</span>
                    <span style='color:#64B5F6;font-weight:bold;'>
                        R$ {val_taxa:,.2f}
                    </span>
                </div>""", unsafe_allow_html=True)

        # Salvar na session
        if st.button("💾 Salvar Cotação", key="t2_save"):
            if 'cotacoes' not in st.session_state:
                st.session_state.cotacoes = []
            st.session_state.cotacoes.append({
                'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'origem': origem,
                'destino': destino,
                'container': cont_tipo,
                'qtd': qtd_containers,
                'total_brl': total_brl,
                'cambio': cambio_usado,
            })
            st.success("✅ Cotação salva com sucesso!")


# ═══════════════════════════════════════════
# ABA 3 — IMPOSTOS
# ═══════════════════════════════════════════
with tab3:
    st.markdown("<h2 style='color:#64B5F6;'>🛃 Simulador de Impostos de Importação</h2>",
                unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box' style='margin-bottom:20px;'>
        ℹ️ Cálculo em <b>cascata</b> conforme legislação brasileira:
        II → IPI → PIS/COFINS → ICMS (por dentro) → AFRMM → Siscomex
    </div>
    """, unsafe_allow_html=True)

    col_imp1, col_imp2 = st.columns([1, 1])

    with col_imp1:
        st.markdown("<h4 style='color:#64B5F6;'>📦 Dados da Mercadoria</h4>",
                    unsafe_allow_html=True)

        categoria = st.selectbox("Categoria da Mercadoria",
                                 list(ALIQUOTAS_NCM.keys()), key="t3_cat")

        if categoria == "Personalizado":
            st.markdown("#### ⚙️ Alíquotas Personalizadas (%)")
            ii_custom   = st.number_input("II (%)",     0.0, 100.0, 0.0, key="ii_c")
            ipi_custom  = st.number_input("IPI (%)",    0.0, 100.0, 0.0, key="ipi_c")
            ALIQUOTAS_NCM["Personalizado"]["II"]  = ii_custom
            ALIQUOTAS_NCM["Personalizado"]["IPI"] = ipi_custom

        valor_cif_imp = st.number_input(
            "Valor CIF (USD)",
            min_value=0.0, value=50000.0,
            format="%.2f", key="t3_cif",
            help="Cost + Insurance + Freight"
        )

        cambio_imp = st.number_input(
            "Câmbio USD/BRL",
            min_value=1.0, value=cambio_atual,
            format="%.4f", key="t3_cambio"
        )

        icms_estado = st.selectbox(
            "Estado de Destino (ICMS)",
            options=[
                ("SP - São Paulo",    18.0),
                ("RJ - Rio de Janeiro", 20.0),
                ("MG - Minas Gerais", 18.0),
                ("SC - Santa Catarina", 17.0),
                ("RS - Rio Grande do Sul", 17.0),
                ("PR - Paraná",       12.0),
                ("BA - Bahia",        19.0),
                ("Outro",             17.0),
            ],
            format_func=lambda x: x[0],
            key="t3_icms"
        )
        aliq_icms = icms_estado[1]

        # Mostrar alíquotas da categoria
        aliq = ALIQUOTAS_NCM[categoria]
        st.markdown(f"""
        <div class='info-box' style='margin-top:15px;'>
            <b>📊 Alíquotas — {categoria}:</b><br>
            II: {aliq['II']}% &nbsp;|&nbsp;
            IPI: {aliq['IPI']}% &nbsp;|&nbsp;
            PIS: {aliq['PIS']}% &nbsp;|&nbsp;
            COFINS: {aliq['COFINS']}% &nbsp;|&nbsp;
            ICMS: {aliq_icms}%
        </div>
        """, unsafe_allow_html=True)

    with col_imp2:
        st.markdown("<h4 style='color:#64B5F6;'>📊 Resultado dos Impostos</h4>",
                    unsafe_allow_html=True)

        imp = calcular_impostos(
            valor_cif_imp, cambio_imp, categoria, aliq_icms
        )

        impostos_items = [
            ("🏛️ II — Imposto de Importação",
             imp["II"], aliq["II"]),
            ("🏭 IPI — Imposto sobre Produto",
             imp["IPI"], aliq["IPI"]),
            ("📊 PIS Importação",
             imp["PIS"], aliq["PIS"]),
            ("📊 COFINS Importação",
             imp["COFINS"], aliq["COFINS"]),
            ("🏙️ ICMS Importação",
             imp["ICMS"], aliq_icms),
            ("⚓ AFRMM — Marinha Mercante",
             imp["AFRMM"], 8.0),
            ("💻 Siscomex",
             imp["Siscomex"], 0.0),
        ]

        for nome, valor, aliquota in impostos_items:
            pct_label = f"({aliquota}%)" if aliquota > 0 else "(fixo)"
            st.markdown(f"""
            <div class='custo-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <b style='color:#E8F4FD;font-size:14px;'>{nome}</b>
                        <small style='color:#90CAF9;'> {pct_label}</small>
                    </div>
                    <b style='color:#64B5F6;font-size:18px;'>
                        R$ {valor:,.2f}
                    </b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Total impostos
        st.markdown(f"""
        <div class='total-card' style='margin-top:15px;'>
            <p style='color:#B3D9F7;margin:0;font-size:13px;'>
                TOTAL DE IMPOSTOS
            </p>
            <h2 style='color:#ff6b6b;margin:6px 0;'>
                R$ {imp['total_impostos']:,.2f}
            </h2>
            <p style='color:#B3D9F7;margin:0;font-size:13px;'>
                VALOR TOTAL NACIONALIZADO
            </p>
            <h1 style='color:white;margin:6px 0;font-size:38px;'>
                R$ {imp['total_geral']:,.2f}
            </h1>
            <p style='color:#90CAF9;margin:0;font-size:12px;'>
                Carga tributária: 
                {(imp['total_impostos']/imp['valor_cif_brl'])*100:.1f}% 
                sobre o valor CIF
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico de impostos
    st.markdown("---")
    st.markdown("<h4 style='color:#64B5F6;'>📊 Composição Tributária</h4>",
                unsafe_allow_html=True)

    g1, g2 = st.columns(2)

    with g1:
        labels = ["II","IPI","PIS","COFINS","ICMS","AFRMM","Siscomex"]
        values = [imp["II"], imp["IPI"], imp["PIS"],
                  imp["COFINS"], imp["ICMS"], imp["AFRMM"], imp["Siscomex"]]
        colors = ["#ff4444","#ffcc44","#44cc88",
                  "#4488ff","#cc44ff","#ff8844","#44ccff"]

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, values=values,
            marker=dict(colors=colors),
            hole=0.45,
            textinfo='label+percent',
            textfont=dict(color='white', size=12)
        )])
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#90CAF9'),
            height=380,
            showlegend=False,
            margin=dict(l=0,r=0,t=10,b=0)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with g2:
        fig_bar = go.Figure(data=[go.Bar(
            x=labels, y=values,
            marker=dict(color=colors, opacity=0.85),
            text=[f"R$ {v:,.0f}" for v in values],
            textposition='outside',
            textfont=dict(color='#90CAF9', size=11)
        )])
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#90CAF9'),
            height=380,
            xaxis=dict(gridcolor='rgba(45,90,142,0.3)'),
            yaxis=dict(gridcolor='rgba(45,90,142,0.3)'),
            margin=dict(l=0,r=0,t=10,b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ═══════════════════════════════════════════
# ABA 4 — SIMULADOR DE CENÁRIOS
# ═══════════════════════════════════════════
with tab4:
    st.markdown("<h2 style='color:#64B5F6;'>📊 Simulador de Cenários</h2>",
                unsafe_allow_html=True)

    sc1, sc2 = st.columns([1, 2])

    with sc1:
        st.markdown("<h4 style='color:#64B5F6;'>⚙️ Parâmetros Base</h4>",
                    unsafe_allow_html=True)

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
            "Categoria",
            list(ALIQUOTAS_NCM.keys()), key="sc_cat"
        )

        st.markdown("---")
        st.markdown("<h4 style='color:#64B5F6;'>💱 Variação Cambial</h4>",
                    unsafe_allow_html=True)

        cambio_min = st.number_input("Câmbio Mínimo", 3.0, 10.0,
                                     4.0, 0.10, key="sc_cmin")
        cambio_max = st.number_input("Câmbio Máximo", 3.0, 15.0,
                                     7.0, 0.10, key="sc_cmax")

        st.markdown("---")
        st.markdown("<h4 style='color:#64B5F6;'>📦 Variação de Volume</h4>",
                    unsafe_allow_html=True)

        cont_min = st.number_input("Mín. Containers", 1, 50, 1, key="sc_cmin2")
        cont_max = st.number_input("Máx. Containers", 1, 50, 10, key="sc_cmax2")

    with sc2:
        # Cenário 1: Impacto do câmbio
        st.markdown("<h4 style='color:#64B5F6;'>💱 Impacto do Câmbio no Custo Total</h4>",
                    unsafe_allow_html=True)

        cambios = np.linspace(cambio_min, cambio_max, 30)
        custos_cambio = []

        for c in cambios:
            imp_c = calcular_impostos(
                val_base + frete_base, c, cat_base
            )
            custo_total = (imp_c['total_geral'] +
                           3500 + 2800)  # frete rodov + despachante
            custos_cambio.append(custo_total)

        fig_cambio = go.Figure()
        fig_cambio.add_trace(go.Scatter(
            x=cambios, y=custos_cambio,
            mode='lines+markers',
            line=dict(color='#64B5F6', width=3),
            marker=dict(size=6, color='#64B5F6'),
            fill='tozeroy',
            fillcolor='rgba(100,181,246,0.1)',
            name='Custo Total'
        ))
        fig_cambio.add_vline(
            x=cambio_atual, line_dash="dash",
            line_color="#ffcc44",
            annotation_text=f"Atual: R${cambio_atual:.2f}",
            annotation_font_color="#ffcc44"
        )
        fig_cambio.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#90CAF9'),
            height=300,
            xaxis=dict(
                title='Câmbio USD/BRL',
                gridcolor='rgba(45,90,142,0.3)',
                color='#90CAF9'
            ),
            yaxis=dict(
                title='Custo Total (R$)',
                gridcolor='rgba(45,90,142,0.3)',
                color='#90CAF9'
            ),
            margin=dict(l=0,r=0,t=10,b=0)
        )
        st.plotly_chart(fig_cambio, use_container_width=True)

        # Cenário 2: Volume de containers
        st.markdown("<h4 style='color:#64B5F6;'>📦 Economia de Escala por Volume</h4>",
                    unsafe_allow_html=True)

        qtds = list(range(int(cont_min), int(cont_max)+1))
        custo_unit = []
        custo_total_list = []

        for q in qtds:
            taxas_q = sum(
                v["20ft"] for v in TAXAS_PORTUARIAS.values()
            ) * q * cambio_atual
            imp_q   = calcular_impostos(
                val_base + frete_base, cambio_atual, cat_base
            )
            total_q = (imp_q['total_geral'] + taxas_q +
                       3500*q + 2800)
            custo_unit.append(total_q / q)
            custo_total_list.append(total_q)

        fig_vol = go.Figure()
        fig_vol.add_trace(go.Bar(
            x=qtds, y=custo_total_list,
            name='Custo Total',
            marker_color='rgba(100,181,246,0.6)',
            yaxis='y'
        ))
        fig_vol.add_trace(go.Scatter(
            x=qtds, y=custo_unit,
            name='Custo Unitário',
            mode='lines+markers',
            line=dict(color='#ffcc44', width=3),
            marker=dict(size=7),
            yaxis='y2'
        ))
        fig_vol.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#90CAF9'),
            height=300,
            xaxis=dict(
                title='Quantidade de Containers',
                gridcolor='rgba(45,90,142,0.3)',
                color='#90CAF9'
            ),
            yaxis=dict(
                title='Custo Total (R$)',
                gridcolor='rgba(45,90,142,0.3)',
                color='#90CAF9'
            ),
            yaxis2=dict(
                title='Custo Unitário (R$)',
                overlaying='y', side='right',
                color='#ffcc44'
            ),
            legend=dict(
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='#90CAF9')
            ),
            margin=dict(l=0,r=0,t=10,b=0)
        )
        st.plotly_chart(fig_vol, use_container_width=True)


# ═══════════════════════════════════════════
# ABA 5 — RELATÓRIO FINAL
# ═══════════════════════════════════════════
with tab5:
    st.markdown("<h2 style='color:#64B5F6;'>📄 Relatório Final da Operação</h2>",
                unsafe_allow_html=True)

    # Dados do relatório
    st.markdown("<h4 style='color:#64B5F6;'>📝 Identificação da Operação</h4>",
                unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    with r1:
        ref_numero = st.text_input("Nº da Proposta", "PP-2024-001", key="r_num")
        cliente    = st.text_input("Cliente",         "Empresa ABC Ltda", key="r_cli")
    with r2:
        data_prop  = st.date_input("Data",  date.today(), key="r_data")
        responsavel = st.text_input("Responsável", "João Silva", key="r_resp")
    with r3:
        validade   = st.number_input("Validade (dias)", 1, 90, 15, key="r_val")
        moeda      = st.selectbox("Moeda do Relatório",
                                  ["BRL (R$)", "USD ($)"], key="r_moeda")

    st.markdown("---")

    # Buscar dados das outras abas via session_state ou recomputar
    # Recomputamos com valores padrão para o relatório
    cambio_rel  = cambio_atual
    val_rel     = 50000.0
    frete_rel   = 2500.0
    seg_rel     = val_rel * 0.003
    cif_rel     = val_rel + frete_rel + seg_rel
    imp_rel     = calcular_impostos(cif_rel, cambio_rel, "Eletrônicos", 18.0)
    taxas_rel   = sum(v["20ft"] for v in TAXAS_PORTUARIAS.values()) * cambio_rel
    frod_rel    = 3500.0
    desp_rel    = 2800.0
    total_rel   = imp_rel['total_geral'] + taxas_rel + frod_rel + desp_rel

    # Cabeçalho do relatório
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(20,40,80,0.95),rgba(10,20,50,0.95));
                border-radius:15px; padding:30px;
                border:1px solid rgba(100,181,246,0.4);
                box-shadow: 0 8px 25px rgba(0,0,0,0.4);'>

        <div style='display:flex;justify-content:space-between;align-items:center;
                    border-bottom:1px solid rgba(100,181,246,0.3);padding-bottom:20px;
                    margin-bottom:20px;'>
            <div>
                <div style='font-size:28px;'>🚢 Porto Pricing Tool</div>
                <div style='color:#90CAF9;font-size:13px;margin-top:4px;'>
                    ⚓ Porto de Santos — SP, Brasil
                </div>
            </div>
            <div style='text-align:right;'>
                <div style='color:#64B5F6;font-size:20px;font-weight:bold;'>
                    {ref_numero}
                </div>
                <div style='color:#90CAF9;font-size:13px;'>
                    {data_prop.strftime("%d/%m/%Y")}
                </div>
                <div style='color:#90CAF9;font-size:13px;'>
                    Válido por {validade} dias
                </div>
            </div>
        </div>

        <div style='display:grid;grid-template-columns:1fr 1fr;gap:20px;'>

            <div>
                <p style='color:#64B5F6;font-weight:bold;margin-bottom:8px;'>
                    👤 CLIENTE
                </p>
                <p style='color:#E8F4FD;font-size:18px;margin:0;'>{cliente}</p>
                <p style='color:#90CAF9;font-size:13px;'>
                    Responsável: {responsavel}
                </p>
            </div>

            <div>
                <p style='color:#64B5F6;font-weight:bold;margin-bottom:8px;'>
                    🚢 OPERAÇÃO
                </p>
                <p style='color:#E8F4FD;margin:0;'>
                    Importação | Container 20ft
                </p>
                <p style='color:#90CAF9;font-size:13px;'>
                    Shanghai → Santos, Brasil
                </p>
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabela de custos
    st.markdown("<h4 style='color:#64B5F6;'>💰 Composição de Custos</h4>",
                unsafe_allow_html=True)

    dados_tabela = {
        "Item": [
            "Valor da Mercadoria (CIF)",
            "Imposto de Importação (II)",
            "IPI",
            "PIS Importação",
            "COFINS Importação",
            "ICMS Importação",
            "AFRMM",
            "Siscomex",
            "Taxas Portuárias",
            "Frete Rodoviário",
            "Despachante Aduaneiro",
        ],
        "Valor (R$)": [
            imp_rel['valor_cif_brl'],
            imp_rel['II'],
            imp_rel['IPI'],
            imp_rel['PIS'],
            imp_rel['COFINS'],
            imp_rel['ICMS'],
            imp_rel['AFRMM'],
            imp_rel['Siscomex'],
            taxas_rel,
            frod_rel,
            desp_rel,
        ],
        "Categoria": [
            "Mercadoria", "Imposto", "Imposto",
            "Imposto", "Imposto", "Imposto",
            "Taxa", "Taxa", "Taxa Portuária",
            "Logística", "Serviço",
        ]
    }

    df = pd.DataFrame(dados_tabela)
    df["Valor (R$)"] = df["Valor (R$)"].apply(lambda x: f"R$ {x:,.2f}")
    df["% do Total"] = [
        f"{v/total_rel*100:.1f}%"
        for v in dados_tabela["Valor (R$)"]
    ]

    st.dataframe(
        df, use_container_width=True,
        hide_index=True,
        column_config={
            "Item":       st.column_config.TextColumn("📋 Item"),
            "Valor (R$)": st.column_config.TextColumn("💰 Valor (R$)"),
            "Categoria":  st.column_config.TextColumn("🏷️ Categoria"),
            "% do Total": st.column_config.TextColumn("📊 % do Total"),
        }
    )

    # Total final destacado
    st.markdown(f"""
    <div class='total-card'>
        <p style='color:#B3D9F7;margin:0;font-size:14px;letter-spacing:2px;'>
            VALOR TOTAL DA OPERAÇÃO
        </p>
        <h1 style='color:white;margin:10px 0;font-size:52px;font-weight:900;'>
            R$ {total_rel:,.2f}
        </h1>
        <p style='color:#90CAF9;margin:0;font-size:14px;'>
            ≈ USD {total_rel/cambio_rel:,.2f} &nbsp;|&nbsp;
            Câmbio: R$ {cambio_rel:.4f} &nbsp;|&nbsp;
            Data: {date.today().strftime("%d/%m/%Y")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Histórico de cotações
    st.markdown("---")
    st.markdown("<h4 style='color:#64B5F6;'>📜 Histórico de Cotações Salvas</h4>",
                unsafe_allow_html=True)

    if 'cotacoes' in st.session_state and st.session_state.cotacoes:
        df_hist = pd.DataFrame(st.session_state.cotacoes)
        df_hist['total_brl'] = df_hist['total_brl'].apply(
            lambda x: f"R$ {x:,.2f}"
        )
        st.dataframe(df_hist, use_container_width=True, hide_index=True)
        if st.button("🗑️ Limpar Histórico", key="r_clear"):
            st.session_state.cotacoes = []
            st.rerun()
    else:
        st.markdown("""
        <div class='info-box' style='text-align:center;'>
            📭 Nenhuma cotação salva ainda.<br>
            <small>Vá na aba <b>💰 Custos & Fretes</b> e clique em
            <b>💾 Salvar Cotação</b></small>
        </div>
        """, unsafe_allow_html=True)

    # Rodapé do relatório
    st.markdown(f"""
    <div style='text-align:center;margin-top:20px;padding:20px;
                background:rgba(10,14,30,0.6);border-radius:12px;
                border:1px solid rgba(45,90,142,0.3);'>
        <p style='color:#64B5F6;margin:0;font-size:13px;'>
            ⚠️ <b>Aviso:</b> Valores calculados com base em dados fictícios/aproximados.
            Consulte sempre um despachante aduaneiro habilitado.
        </p>
        <p style='color:#2d5a8e;margin:8px 0 0 0;font-size:12px;'>
            🚢 Porto Pricing Tool | ⚓ Porto de Santos, SP |
            Desenvolvido com Streamlit + Plotly 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)
