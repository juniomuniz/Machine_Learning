import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
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
            linear-gradient(rgba(5,10,30,0.82),rgba(5,10,30,0.82)),
            url("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Porto_de_Santos.jpg/1280px-Porto_de_Santos.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    .hero-banner {
        background-image:
            linear-gradient(rgba(5,10,30,0.60),rgba(5,10,30,0.92)),
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
        background: linear-gradient(90deg,#ffffff,#64B5F6,#42A5F5);
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
        margin: 4px 4px 4px 0;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .metric-card {
        background: linear-gradient(135deg,
            rgba(30,58,95,0.85),
            rgba(45,90,142,0.85));
        padding: 18px;
        border-radius: 15px;
        border: 1px solid rgba(61,122,181,0.6);
        text-align: center;
        margin: 5px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-value {
        font-size: 30px;
        font-weight: bold;
        color: #64B5F6;
    }
    .metric-label {
        font-size: 12px;
        color: #90CAF9;
        margin-top: 5px;
    }
    .info-box {
        background: rgba(30,58,95,0.7);
        padding: 14px;
        border-radius: 10px;
        font-size: 13px;
        color: #90CAF9;
        border: 1px solid rgba(61,122,181,0.3);
        backdrop-filter: blur(5px);
        margin-bottom: 8px;
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
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #64B5F6;
        margin: 8px 0;
        backdrop-filter: blur(10px);
    }
    .custo-card-green  { border-left: 4px solid #44cc88 !important; }
    .custo-card-yellow { border-left: 4px solid #ffcc44 !important; }
    .custo-card-red    { border-left: 4px solid #ff4444 !important; }
    .total-card {
        background: linear-gradient(135deg,#1E88E5,#1565C0);
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
        background: linear-gradient(135deg,#1E88E5,#1565C0) !important;
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
    "🔴 Pequena (30×20×15cm)": Caixa("Pequena", 30,  20, 15,  2.5,
                                      "rgba(255,100,100,0.8)", "#ff4444"),
    "🔵 Média (50×40×30cm)":   Caixa("Média",   50,  40, 30,  8.0,
                                      "rgba(100,180,255,0.8)", "#4488ff"),
    "🟢 Grande (80×60×50cm)":  Caixa("Grande",  80,  60, 50, 20.0,
                                      "rgba(100,220,150,0.8)", "#44cc88"),
    "🟡 XL (100×80×70cm)":    Caixa("XL",      100, 80, 70, 35.0,
                                      "rgba(255,220,100,0.8)", "#ffcc44"),
    "🟣 Custom":               Caixa("Custom",   40, 30,  25,  5.0,
                                      "rgba(200,100,255,0.8)", "#cc44ff"),
}

TAXAS_PORTUARIAS = {
    "THC - Terminal Handling Charge": {"20ft": 650,  "40ft": 850,  "40ft HC": 900},
    "BL Fee - Bill of Lading":        {"20ft": 150,  "40ft": 150,  "40ft HC": 150},
    "ISPS - Segurança Portuária":     {"20ft":  45,  "40ft":  55,  "40ft HC":  55},
    "Capatazia":                      {"20ft": 380,  "40ft": 520,  "40ft HC": 560},
    "Liberação do Container":         {"20ft": 220,  "40ft": 280,  "40ft HC": 280},
}

ALIQUOTAS_NCM = {
    "Eletrônicos":           {"II": 14.0, "IPI": 10.0, "PIS": 2.1, "COFINS": 9.65},
    "Vestuário":             {"II": 20.0, "IPI":  0.0, "PIS": 2.1, "COFINS": 9.65},
    "Alimentos":             {"II": 10.0, "IPI":  0.0, "PIS": 2.1, "COFINS": 9.65},
    "Máquinas/Equipamentos": {"II": 12.0, "IPI":  5.0, "PIS": 2.1, "COFINS": 9.65},
    "Químicos":              {"II":  8.0, "IPI":  0.0, "PIS": 2.1, "COFINS": 9.65},
    "Automóveis":            {"II": 35.0, "IPI": 25.0, "PIS": 2.1, "COFINS": 9.65},
    "Personalizado":         {"II":  0.0, "IPI":  0.0, "PIS": 2.1, "COFINS": 9.65},
}


# ─────────────────────────────
# FUNÇÕES 3D OTIMIZADAS
# ─────────────────────────────
def criar_container_wireframe(container):
    """Wireframe do container — apenas linhas"""
    c = container
    vx = [0, c.comp, c.comp, 0,     0,     c.comp, c.comp, 0    ]
    vy = [0, 0,      c.larg, c.larg,0,     0,      c.larg, c.larg]
    vz = [0, 0,      0,      0,     c.alt, c.alt,  c.alt,  c.alt ]

    arestas = [(0,1),(1,2),(2,3),(3,0),
               (4,5),(5,6),(6,7),(7,4),
               (0,4),(1,5),(2,6),(3,7)]
    ex, ey, ez = [], [], []
    for (a, b) in arestas:
        ex += [vx[a], vx[b], None]
        ey += [vy[a], vy[b], None]
        ez += [vz[a], vz[b], None]

    return go.Scatter3d(
        x=ex, y=ey, z=ez,
        mode='lines',
        line=dict(color='#64B5F6', width=3),
        name='Container',
        hoverinfo='skip'
    )


@st.cache_data
def calcular_e_plotar(
    cont_tipo, cont_comp, cont_larg, cont_alt, cont_peso_max,
    cx_nome, cx_comp, cx_larg, cx_alt, cx_peso,
    cx_cor, cx_cor_borda, percentual
):
    """
    ✅ OTIMIZADO:
    - Todas as caixas em apenas 3 traces totais
    - Cache automático do Streamlit
    - Container sempre 100% preenchido corretamente
    """
    container = Container(cont_tipo, cont_comp,
                          cont_larg, cont_alt, cont_peso_max)

    # Quantas caixas cabem por dimensão
    qtd_c = int(cont_comp / cx_comp)
    qtd_l = int(cont_larg / cx_larg)
    qtd_a = int(cont_alt  / cx_alt )

    total_vol   = qtd_c * qtd_l * qtd_a
    max_peso    = int(cont_peso_max / cx_peso)

    # ✅ Total real limitado apenas por volume e peso
    total_real  = min(total_vol, max_peso)
    qtd_mostrar = int(total_real * percentual / 100)

    # ─── Listas unificadas ───
    all_x, all_y, all_z = [], [], []
    all_i, all_j, all_k = [], [], []
    edge_x, edge_y, edge_z = [], [], []

    arestas = [(0,1),(1,2),(2,3),(3,0),
               (4,5),(5,6),(6,7),(7,4),
               (0,4),(1,5),(2,6),(3,7)]

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

                vx = [x,    x+dx, x+dx, x,
                      x,    x+dx, x+dx, x   ]
                vy = [y,    y,    y+dy, y+dy,
                      y,    y,    y+dy, y+dy ]
                vz = [z,    z,    z,    z,
                      z+dz, z+dz, z+dz, z+dz ]

                all_x.extend(vx)
                all_y.extend(vy)
                all_z.extend(vz)

                i_l = [0,0,0,0,4,4,3,3,1,1,2,2]
                j_l = [1,2,4,5,5,6,7,6,2,5,3,6]
                k_l = [2,3,5,6,6,7,6,2,5,6,6,7]

                all_i.extend([i+offset for i in i_l])
                all_j.extend([j+offset for j in j_l])
                all_k.extend([k+offset for k in k_l])

                for (a, b) in arestas:
                    edge_x += [vx[a], vx[b], None]
                    edge_y += [vy[a], vy[b], None]
                    edge_z += [vz[a], vz[b], None]

                count += 1

            if count >= qtd_mostrar: break
        if count >= qtd_mostrar: break

    # ─── Montar figura ───
    traces = []

    # Trace 1 — wireframe do container
    traces.append(criar_container_wireframe(container))

    # Trace 2 — TODAS as caixas em 1 único Mesh3d
    if all_x:
        traces.append(go.Mesh3d(
            x=all_x, y=all_y, z=all_z,
            i=all_i, j=all_j, k=all_k,
            color=cx_cor,
            opacity=0.85,
            flatshading=True,
            lighting=dict(
                ambient=0.7,
                diffuse=0.9,
                specular=0.2,
                roughness=0.5,
                fresnel=0.1
            ),
            lightposition=dict(x=1000, y=1000, z=1500),
            showscale=False,
            hoverinfo='skip',
            name='Caixas'
        ))

    # Trace 3 — bordas unificadas em 1 único Scatter3d
    if edge_x:
        traces.append(go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color=cx_cor_borda, width=1),
            hoverinfo='skip',
            showlegend=False,
            name='Bordas'
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title=dict(
                    text='Comprimento (cm)',
                    font=dict(color='#90CAF9')
                ),
                backgroundcolor='rgba(5,10,30,0.8)',
                gridcolor='rgba(45,90,142,0.5)',
                showbackground=True,
                zerolinecolor='#2d5a8e',
                tickfont=dict(color='#90CAF9')
            ),
            yaxis=dict(
                title=dict(
                    text='Largura (cm)',
                    font=dict(color='#90CAF9')
                ),
                backgroundcolor='rgba(5,10,30,0.8)',
                gridcolor='rgba(45,90,142,0.5)',
                showbackground=True,
                zerolinecolor='#2d5a8e',
                tickfont=dict(color='#90CAF9')
            ),
            zaxis=dict(
                title=dict(
                    text='Altura (cm)',
                    font=dict(color='#90CAF9')
                ),
                backgroundcolor='rgba(5,10,30,0.8)',
                gridcolor='rgba(45,90,142,0.5)',
                showbackground=True,
                zerolinecolor='#2d5a8e',
                tickfont=dict(color='#90CAF9')
            ),
            bgcolor='rgba(5,10,30,0.85)',
            camera=dict(
                eye=dict(x=1.8, y=-1.8, z=1.2),
                up=dict(x=0, y=0, z=1)
            ),
            aspectmode='data'
        ),
        paper_bgcolor='rgba(5,10,30,0.5)',
        plot_bgcolor='rgba(5,10,30,0.5)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        showlegend=False
    )

    vol_pct  = (total_real * cx_comp * cx_larg * cx_alt) / \
               (cont_comp * cont_larg * cont_alt) * 100
    peso_pct = (total_real * cx_peso / cont_peso_max) * 100

    stats = {
        'total':      total_real,
        'mostradas':  qtd_mostrar,
        'qtd_c':      qtd_c,
        'qtd_l':      qtd_l,
        'qtd_a':      qtd_a,
        'peso_total': total_real * cx_peso,
        'vol_pct':    vol_pct,
        'peso_pct':   peso_pct,
        'limitador':  'Peso ⚖️' if max_peso < total_vol
                       else 'Volume 📦'
    }

    return fig, stats


# ─────────────────────────────
# FUNÇÕES — PRICING
# ─────────────────────────────
def get_cambio_usd():
    try:
        url  = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        resp = requests.get(url, timeout=3)
        data = resp.json()
        return float(data['USDBRL']['bid'])
    except:
        return 5.05


def calcular_impostos(valor_cif_usd, cambio,
                      categoria, icms_estado=18.0):
    aliq          = ALIQUOTAS_NCM[categoria]
    valor_cif_brl = valor_cif_usd * cambio
    afrmm         = valor_cif_brl * 0.08
    ii            = valor_cif_brl  * (aliq["II"]     / 100)
    base_ipi      = valor_cif_brl + ii
    ipi           = base_ipi       * (aliq["IPI"]    / 100)
    pis           = valor_cif_brl  * (aliq["PIS"]    / 100)
    cofins        = valor_cif_brl  * (aliq["COFINS"] / 100)
    soma_antes    = valor_cif_brl + ii + ipi + pis + cofins + afrmm
    icms          = soma_antes / (1 - icms_estado/100) * (icms_estado/100)
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


# ─────────────────────────────
# CÂMBIO
# ─────────────────────────────
cambio_atual = get_cambio_usd()


# ════════════════════════════════════════════
# HERO BANNER — limpo sem SVG
# ════════════════════════════════════════════
st.markdown(f"""
<div class='hero-banner'>
    <div style='display:flex;
                justify-content:space-between;
                align-items:center;'>
        <div>
            <div class='porto-tag'>⚓ Porto de Santos — SP, Brasil</div>
            <h1 class='hero-title' style='margin-top:14px;'>
                🚢 Porto Pricing Tool
            </h1>
            <p class='hero-subtitle'>
                Plataforma completa de otimização de carga
                e precificação portuária
            </p>
            <div style='margin-top:15px;'>
                <span class='hero-badge'>📦 3D Container</span>
                <span class='hero-badge'>💰 Custos & Fretes</span>
                <span class='hero-badge'>🛃 Impostos</span>
                <span class='hero-badge'>📊 Cenários</span>
                <span class='hero-badge'>📄 Relatório</span>
            </div>
            <div style='margin-top:18px;'>
                <div class='info-box'
                     style='display:inline-block;
                            padding:8px 16px;'>
                    💱 Câmbio USD/BRL em tempo real:
                    <b style='color:#64B5F6;font-size:18px;'>
                        R$ {cambio_atual:.4f}
                    </b>
                    &nbsp;
                    <span style='color:#90CAF9;font-size:11px;'>
                        via Banco Central
                    </span>
                </div>
            </div>
        </div>
        <div style='font-size:100px;opacity:0.15;
                    padding-right:20px;'>
            🚢
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# ABAS
# ════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📦  Container 3D",
    "💰  Custos & Fretes",
    "🛃  Impostos",
    "📊  Simulador de Cenários",
    "📄  Relatório Final",
])


# ═══════════════════════════════════════════
# ABA 1 — CONTAINER 3D
# ═══════════════════════════════════════════
with tab1:
    col_main, col_side = st.columns([3, 1])

    with col_side:
        st.markdown(
            "<h3 style='color:#64B5F6;'>⚙️ Configurações</h3>",
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
            st.markdown("#### 🔧 Dimensões")
            c_comp = st.slider("Comprimento (cm)",
                               10, 200, 40, key="cc")
            c_larg = st.slider("Largura (cm)",
                               10, 200, 30, key="cl")
            c_alt  = st.slider("Altura (cm)",
                               10, 200, 25, key="ca")
            c_peso = st.slider("Peso (kg)",
                                1, 500,  5, key="cp")
            caixa  = Caixa("Custom",
                            c_comp, c_larg, c_alt, c_peso,
                            "rgba(200,100,255,0.8)", "#cc44ff")

        percentual = st.slider(
            "🔄 Percentual de Carga",
            0, 100, 100, 5,
            key="t1_perc",
            help="Simule diferentes níveis de preenchimento"
        )

        st.markdown("---")

        st.markdown(f"""
        <div class='info-box'>
            <b>📐 Container:</b> {container.tipo}<br>
            {container.comp}×{container.larg}×{container.alt} cm<br>
            Vol: {container.comp*container.larg*container.alt/1e6:.1f} m³<br>
            Carga Máx: {container.peso_max:,} kg
        </div>
        <div class='info-box'>
            <b>📦 Caixa:</b> {caixa.nome}<br>
            {caixa.comp}×{caixa.larg}×{caixa.alt} cm<br>
            Vol: {caixa.comp*caixa.larg*caixa.alt/1e6:.4f} m³<br>
            Peso: {caixa.peso} kg
        </div>
        """, unsafe_allow_html=True)

    with col_main:

        # ✅ Chamar com cache — sem limite artificial
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

        # Métricas
        m1,m2,m3,m4,m5 = st.columns(5)
        for col, icon, val, label in [
            (m1,"📦", stats['total'],
             "Total Caixas"),
            (m2,"✅", stats['mostradas'],
             "Carregadas"),
            (m3,"📐", f"{stats['vol_pct']:.1f}%",
             "Vol. Utilizado"),
            (m4,"⚖️", f"{stats['peso_total']:,.0f}",
             "Peso (kg)"),
            (m5,"🎯", stats['limitador'],
             "Limitante"),
        ]:
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size:22px;'>{icon}</div>
                    <div class='metric-value'>{val}</div>
                    <div class='metric-label'>{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <p style='color:#90CAF9;font-size:13px;margin-top:10px;'>
        💡 <b>Dica:</b> Arraste para rotacionar
        | Scroll para zoom
        | Duplo clique para resetar
        </p>""", unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True)

        # Barras de progresso
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(
                "<p style='color:#90CAF9;'>📦 Volume Utilizado</p>",
                unsafe_allow_html=True
            )
            st.progress(min(stats['vol_pct']/100, 1.0))
            st.markdown(
                f"<b style='color:#64B5F6;'>"
                f"{stats['vol_pct']:.1f}%</b>",
                unsafe_allow_html=True
            )
        with p2:
            st.markdown(
                "<p style='color:#90CAF9;'>⚖️ Peso Utilizado</p>",
                unsafe_allow_html=True
            )
            st.progress(min(stats['peso_pct']/100, 1.0))
            st.markdown(
                f"<b style='color:#64B5F6;'>"
                f"{stats['peso_pct']:.1f}%</b>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown(
            "<h4 style='color:#64B5F6;'>📐 Arranjo Espacial</h4>",
            unsafe_allow_html=True
        )
        a1,a2,a3 = st.columns(3)
        for col, icon, val, label in [
            (a1,"↔️", stats['qtd_c'], "Colunas (Comprimento)"),
            (a2,"↕️", stats['qtd_l'], "Fileiras (Largura)"),
            (a3,"🔝", stats['qtd_a'], "Camadas (Altura)"),
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
        "<h2 style='color:#64B5F6;'>💰 Calculadora de Custos & Fretes</h2>",
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class='info-box'>
        💱 <b>Câmbio USD/BRL em tempo real:</b>
        <span style='color:#64B5F6;font-size:20px;font-weight:bold;'>
            R$ {cambio_atual:.4f}
        </span>
        &nbsp;
        <span style='color:#90CAF9;font-size:12px;'>
            (via AwesomeAPI / Banco Central)
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    col_form, col_result = st.columns([1, 1])

    with col_form:
        st.markdown(
            "<h4 style='color:#64B5F6;'>🚢 Dados do Embarque</h4>",
            unsafe_allow_html=True
        )
        tipo_op = st.selectbox(
            "Tipo de Operação",
            ["Importação","Exportação"], key="t2_op"
        )
        cont_tipo = st.selectbox(
            "Tipo de Container",
            ["20ft","40ft","40ft HC"], key="t2_cont"
        )
        qtd_containers = st.number_input(
            "Quantidade de Containers",
            min_value=1, value=1, key="t2_qtd"
        )
        origem  = st.text_input(
            "Porto de Origem", "Shanghai, China", key="t2_orig"
        )
        destino = st.text_input(
            "Porto de Destino", "Santos, Brasil", key="t2_dest"
        )

        st.markdown("---")
        st.markdown(
            "<h4 style='color:#64B5F6;'>💵 Valores (USD)</h4>",
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

        st.markdown("---")
        st.markdown(
            "<h4 style='color:#64B5F6;'>🚛 Logística Interna</h4>",
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
            min_value=1.0, value=cambio_atual,
            format="%.4f", key="t2_cambio"
        )

    with col_result:
        st.markdown(
            "<h4 style='color:#64B5F6;'>📊 Resumo de Custos</h4>",
            unsafe_allow_html=True
        )

        seguro_usd    = valor_mercadoria * (seguro_pct / 100)
        valor_cif_usd = valor_mercadoria + frete_maritimo + seguro_usd
        valor_cif_brl = valor_cif_usd * cambio_usado

        total_taxas_brl = sum(
            v[cont_tipo] for v in TAXAS_PORTUARIAS.values()
        ) * qtd_containers * cambio_usado

        if armazenagem_dias <= 5:
            arm_brl = armazenagem_dias * 180
        elif armazenagem_dias <= 10:
            arm_brl = 5*180 + (armazenagem_dias-5) * 280
        else:
            arm_brl = 5*180 + 5*280 + (armazenagem_dias-10) * 420
        arm_brl *= qtd_containers

        total_brl = (valor_cif_brl + total_taxas_brl +
                     arm_brl + frete_rodoviario + despachante)

        itens = [
            ("🌊 Frete Marítimo",
             frete_maritimo * cambio_usado,
             f"USD {frete_maritimo:,.2f} × {cambio_usado:.4f}",
             "custo-card"),
            ("🛡️ Seguro de Carga",
             seguro_usd * cambio_usado,
             f"{seguro_pct}% sobre mercadoria",
             "custo-card"),
            ("🏭 Taxas Portuárias",
             total_taxas_brl,
             f"THC+BL+ISPS+Capatazia × {qtd_containers} cont.",
             "custo-card-yellow"),
            ("🏗️ Armazenagem",
             arm_brl,
             f"{armazenagem_dias} dias (escalonado)",
             "custo-card-yellow"),
            ("🚛 Frete Rodoviário",
             frete_rodoviario,
             "Porto → Destino final",
             "custo-card-green"),
            ("📋 Despachante",
             despachante,
             "Serviços aduaneiros",
             "custo-card-green"),
        ]

        for nome, valor, detalhe, classe in itens:
            st.markdown(f"""
            <div class='custo-card {classe}'>
                <div style='display:flex;
                            justify-content:space-between;
                            align-items:center;'>
                    <div>
                        <b style='color:#E8F4FD;'>{nome}</b><br>
                        <small style='color:#90CAF9;'>
                            {detalhe}
                        </small>
                    </div>
                    <div style='font-size:20px;
                                font-weight:bold;
                                color:#64B5F6;'>
                        R$ {valor:,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='total-card'>
            <p style='color:#B3D9F7;margin:0;font-size:14px;'>
                CUSTO TOTAL DA OPERAÇÃO
            </p>
            <h1 style='color:white;margin:8px 0;font-size:42px;'>
                R$ {total_brl:,.2f}
            </h1>
            <p style='color:#90CAF9;margin:0;font-size:13px;'>
                ≈ USD {total_brl/cambio_usado:,.2f} &nbsp;|&nbsp;
                R$ {total_brl/qtd_containers:,.2f} por container
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 Detalhamento Taxas Portuárias"):
            for taxa, valores in TAXAS_PORTUARIAS.items():
                val_t = (valores[cont_tipo]
                         * cambio_usado * qtd_containers)
                st.markdown(f"""
                <div style='display:flex;
                            justify-content:space-between;
                            padding:8px;
                            border-bottom:1px solid
                            rgba(45,90,142,0.3);'>
                    <span style='color:#90CAF9;'>{taxa}</span>
                    <span style='color:#64B5F6;font-weight:bold;'>
                        R$ {val_t:,.2f}
                    </span>
                </div>""", unsafe_allow_html=True)

        if st.button("💾 Salvar Cotação", key="t2_save"):
            if 'cotacoes' not in st.session_state:
                st.session_state.cotacoes = []
            st.session_state.cotacoes.append({
                'Data':       datetime.now().strftime(
                                  "%d/%m/%Y %H:%M"),
                'Origem':     origem,
                'Destino':    destino,
                'Container':  cont_tipo,
                'Qtd':        qtd_containers,
                'Total (R$)': f"R$ {total_brl:,.2f}",
                'Câmbio':     f"{cambio_usado:.4f}",
            })
            st.success("✅ Cotação salva com sucesso!")


# ═══════════════════════════════════════════
# ABA 3 — IMPOSTOS
# ═══════════════════════════════════════════
with tab3:
    st.markdown(
        "<h2 style='color:#64B5F6;'>"
        "🛃 Simulador de Impostos de Importação</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='info-box' style='margin-bottom:20px;'>
        ℹ️ Cálculo em <b>cascata</b> conforme legislação brasileira:<br>
        II → IPI → PIS/COFINS → ICMS (por dentro) → AFRMM → Siscomex
    </div>
    """, unsafe_allow_html=True)

    col_imp1, col_imp2 = st.columns([1, 1])

    with col_imp1:
        st.markdown(
            "<h4 style='color:#64B5F6;'>📦 Dados da Mercadoria</h4>",
            unsafe_allow_html=True
        )

        categoria = st.selectbox(
            "Categoria",
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
            min_value=1.0, value=cambio_atual,
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
            II: {aliq['II']}% &nbsp;|&nbsp;
            IPI: {aliq['IPI']}% &nbsp;|&nbsp;
            PIS: {aliq['PIS']}% &nbsp;|&nbsp;
            COFINS: {aliq['COFINS']}% &nbsp;|&nbsp;
            ICMS: {aliq_icms}%
        </div>
        """, unsafe_allow_html=True)

    with col_imp2:
        st.markdown(
            "<h4 style='color:#64B5F6;'>📊 Resultado dos Impostos</h4>",
            unsafe_allow_html=True
        )

        imp = calcular_impostos(
            valor_cif_imp, cambio_imp, categoria, aliq_icms
        )

        impostos_items = [
            ("🏛️ II — Imposto de Importação",
             imp["II"],       aliq["II"]),
            ("🏭 IPI — Imposto sobre Produto",
             imp["IPI"],      aliq["IPI"]),
            ("📊 PIS Importação",
             imp["PIS"],      aliq["PIS"]),
            ("📊 COFINS Importação",
             imp["COFINS"],   aliq["COFINS"]),
            ("🏙️ ICMS Importação",
             imp["ICMS"],     aliq_icms),
            ("⚓ AFRMM — Marinha Mercante",
             imp["AFRMM"],    8.0),
            ("💻 Siscomex",
             imp["Siscomex"], 0.0),
        ]

        for nome, valor, aliquota in impostos_items:
            pct = f"({aliquota}%)" if aliquota > 0 else "(fixo)"
            st.markdown(f"""
            <div class='custo-card'>
                <div style='display:flex;
                            justify-content:space-between;
                            align-items:center;'>
                    <div>
                        <b style='color:#E8F4FD;font-size:14px;'>
                            {nome}
                        </b>
                        <small style='color:#90CAF9;'> {pct}</small>
                    </div>
                    <b style='color:#64B5F6;font-size:18px;'>
                        R$ {valor:,.2f}
                    </b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='total-card' style='margin-top:15px;'>
            <p style='color:#B3D9F7;margin:0;font-size:13px;'>
                TOTAL DE IMPOSTOS
            </p>
            <h2 style='color:#ff6b6b;margin:6px 0;'>
                R$ {imp['total_impostos']:,.2f}
            </h2>
            <p style='color:#B3D9F7;margin:4px 0 0 0;font-size:13px;'>
                VALOR TOTAL NACIONALIZADO
            </p>
            <h1 style='color:white;margin:6px 0;font-size:36px;'>
                R$ {imp['total_geral']:,.2f}
            </h1>
            <p style='color:#90CAF9;margin:0;font-size:12px;'>
                Carga tributária:
                {(imp['total_impostos']/imp['valor_cif_brl'])*100:.1f}%
                sobre o valor CIF
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Gráficos
    st.markdown("---")
    st.markdown(
        "<h4 style='color:#64B5F6;'>📊 Composição Tributária</h4>",
        unsafe_allow_html=True
    )

    labels = ["II","IPI","PIS","COFINS",
              "ICMS","AFRMM","Siscomex"]
    values = [imp["II"],  imp["IPI"],  imp["PIS"],
              imp["COFINS"],imp["ICMS"],imp["AFRMM"],
              imp["Siscomex"]]
    colors = ["#ff4444","#ffcc44","#44cc88",
              "#4488ff","#cc44ff","#ff8844","#44ccff"]

    g1, g2 = st.columns(2)
    with g1:
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
            height=360, showlegend=False,
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
            height=360,
            xaxis=dict(gridcolor='rgba(45,90,142,0.3)'),
            yaxis=dict(gridcolor='rgba(45,90,142,0.3)'),
            margin=dict(l=0,r=0,t=10,b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ═══════════════════════════════════════════
# ABA 4 — SIMULADOR DE CENÁRIOS
# ═══════════════════════════════════════════
with tab4:
    st.markdown(
        "<h2 style='color:#64B5F6;'>📊 Simulador de Cenários</h2>",
        unsafe_allow_html=True
    )

    sc1, sc2 = st.columns([1, 2])

    with sc1:
        st.markdown(
            "<h4 style='color:#64B5F6;'>⚙️ Parâmetros Base</h4>",
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
            "Categoria",
            list(ALIQUOTAS_NCM.keys()), key="sc_cat"
        )

        st.markdown("---")
        st.markdown(
            "<h4 style='color:#64B5F6;'>💱 Variação Cambial</h4>",
            unsafe_allow_html=True
        )
        cambio_min = st.number_input(
            "Câmbio Mínimo", 3.0, 10.0, 4.0, 0.10,
            key="sc_cmin"
        )
        cambio_max = st.number_input(
            "Câmbio Máximo", 3.0, 15.0, 7.0, 0.10,
            key="sc_cmax"
        )

        st.markdown("---")
        st.markdown(
            "<h4 style='color:#64B5F6;'>📦 Variação de Volume</h4>",
            unsafe_allow_html=True
        )
        cont_min = st.number_input(
            "Mín. Containers", 1, 50,  1, key="sc_vmin"
        )
        cont_max = st.number_input(
            "Máx. Containers", 1, 50, 10, key="sc_vmax"
        )

    with sc2:
        # Gráfico 1 — impacto do câmbio
        st.markdown(
            "<h4 style='color:#64B5F6;'>"
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
                imp_c['total_geral'] + 3500 + 2800
            )

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
            font=dict(color='#90CAF9'), height=280,
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

        # Gráfico 2 — economia de escala
        st.markdown(
            "<h4 style='color:#64B5F6;'>"
            "📦 Economia de Escala por Volume</h4>",
            unsafe_allow_html=True
        )

        qtds           = list(range(int(cont_min),
                                    int(cont_max)+1))
        custo_unit     = []
        custo_tot_list = []

        for q in qtds:
            taxas_q = sum(
                v["20ft"] for v in TAXAS_PORTUARIAS.values()
            ) * q * cambio_atual
            imp_q   = calcular_impostos(
                val_base + frete_base, cambio_atual, cat_base
            )
            total_q = (imp_q['total_geral']
                       + taxas_q + 3500*q + 2800)
            custo_unit.append(total_q / q)
            custo_tot_list.append(total_q)

        fig_vol = go.Figure()
        fig_vol.add_trace(go.Bar(
            x=qtds, y=custo_tot_list,
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
            font=dict(color='#90CAF9'), height=280,
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
    st.markdown(
        "<h2 style='color:#64B5F6;'>📄 Relatório Final da Operação</h2>",
        unsafe_allow_html=True
    )

    r1, r2, r3 = st.columns(3)
    with r1:
        ref_numero  = st.text_input(
            "Nº da Proposta", "PP-2024-001", key="r_num"
        )
        cliente     = st.text_input(
            "Cliente", "Empresa ABC Ltda", key="r_cli"
        )
    with r2:
        data_prop   = st.date_input(
            "Data", date.today(), key="r_data"
        )
        responsavel = st.text_input(
            "Responsável", "João Silva", key="r_resp"
        )
    with r3:
        validade = st.number_input(
            "Validade (dias)", 1, 90, 15, key="r_val"
        )

    st.markdown("---")

    # Recomputar para relatório
    cambio_rel = cambio_atual
    val_rel    = 50000.0
    frete_rel  = 2500.0
    seg_rel    = val_rel * 0.003
    cif_rel    = val_rel + frete_rel + seg_rel
    imp_rel    = calcular_impostos(
        cif_rel, cambio_rel, "Eletrônicos", 18.0
    )
    taxas_rel  = sum(
        v["20ft"] for v in TAXAS_PORTUARIAS.values()
    ) * cambio_rel
    frod_rel   = 3500.0
    desp_rel   = 2800.0
    total_rel  = (imp_rel['total_geral']
                  + taxas_rel + frod_rel + desp_rel)

    # Cabeçalho do relatório
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,
                    rgba(20,40,80,0.95),
                    rgba(10,20,50,0.95));
                border-radius:15px;padding:30px;
                border:1px solid rgba(100,181,246,0.4);
                box-shadow:0 8px 25px rgba(0,0,0,0.4);
                margin-bottom:20px;'>

        <div style='display:flex;
                    justify-content:space-between;
                    align-items:center;
                    border-bottom:1px solid rgba(100,181,246,0.3);
                    padding-bottom:20px;margin-bottom:20px;'>
            <div>
                <div style='font-size:30px;'>🚢</div>
                <div style='font-size:22px;font-weight:bold;
                            color:#E8F4FD;margin-top:6px;'>
                    Porto Pricing Tool
                </div>
                <div style='color:#90CAF9;font-size:13px;
                            margin-top:4px;'>
                    ⚓ Porto de Santos — SP, Brasil
                </div>
            </div>
            <div style='text-align:right;'>
                <div style='color:#64B5F6;font-size:22px;
                            font-weight:bold;'>
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

        <div style='display:grid;
                    grid-template-columns:1fr 1fr;gap:20px;'>
            <div>
                <p style='color:#64B5F6;font-weight:bold;
                          margin-bottom:6px;'>👤 CLIENTE</p>
                <p style='color:#E8F4FD;font-size:18px;margin:0;'>
                    {cliente}
                </p>
                <p style='color:#90CAF9;font-size:13px;'>
                    Responsável: {responsavel}
                </p>
            </div>
            <div>
                <p style='color:#64B5F6;font-weight:bold;
                          margin-bottom:6px;'>🚢 OPERAÇÃO</p>
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

    # Tabela de custos
    st.markdown(
        "<h4 style='color:#64B5F6;'>💰 Composição de Custos</h4>",
        unsafe_allow_html=True
    )

    valores_brutos = [
        imp_rel['valor_cif_brl'],
        imp_rel['II'],    imp_rel['IPI'],
        imp_rel['PIS'],   imp_rel['COFINS'],
        imp_rel['ICMS'],  imp_rel['AFRMM'],
        imp_rel['Siscomex'],
        taxas_rel, frod_rel, desp_rel,
    ]

    df = pd.DataFrame({
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
            f"R$ {v:,.2f}" for v in valores_brutos
        ],
        "Categoria": [
            "Mercadoria","Imposto","Imposto",
            "Imposto","Imposto","Imposto",
            "Taxa","Taxa","Taxa Portuária",
            "Logística","Serviço",
        ],
        "% do Total": [
            f"{v/total_rel*100:.1f}%"
            for v in valores_brutos
        ],
    })

    st.dataframe(
        df, use_container_width=True, hide_index=True,
        column_config={
            "Item":       st.column_config.TextColumn("📋 Item"),
            "Valor (R$)": st.column_config.TextColumn("💰 Valor"),
            "Categoria":  st.column_config.TextColumn("🏷️ Categoria"),
            "% do Total": st.column_config.TextColumn("📊 % Total"),
        }
    )

    # Total final
    st.markdown(f"""
    <div class='total-card'>
        <p style='color:#B3D9F7;margin:0;font-size:14px;
                  letter-spacing:2px;'>
            VALOR TOTAL DA OPERAÇÃO
        </p>
        <h1 style='color:white;margin:10px 0;
                   font-size:50px;font-weight:900;'>
            R$ {total_rel:,.2f}
        </h1>
        <p style='color:#90CAF9;margin:0;font-size:14px;'>
            ≈ USD {total_rel/cambio_rel:,.2f} &nbsp;|&nbsp;
            Câmbio: R$ {cambio_rel:.4f} &nbsp;|&nbsp;
            Data: {date.today().strftime("%d/%m/%Y")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Histórico
    st.markdown("---")
    st.markdown(
        "<h4 style='color:#64B5F6;'>📜 Histórico de Cotações</h4>",
        unsafe_allow_html=True
    )

    if ('cotacoes' in st.session_state
            and st.session_state.cotacoes):
        df_hist = pd.DataFrame(st.session_state.cotacoes)
        st.dataframe(
            df_hist, use_container_width=True, hide_index=True
        )
        if st.button("🗑️ Limpar Histórico", key="r_clear"):
            st.session_state.cotacoes = []
            st.rerun()
    else:
        st.markdown("""
        <div class='info-box' style='text-align:center;'>
            📭 Nenhuma cotação salva ainda.<br>
            <small>Vá em <b>💰 Custos & Fretes</b>
            e clique em <b>💾 Salvar Cotação</b></small>
        </div>
        """, unsafe_allow_html=True)