
import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from  dataclasses import dataclass

# Configuração da página
st.set_page_config(
    page_title="🚢 Container 3D Optimizer",
    page_icon="🚢",
    layout="wide"
)
# CSS customizado com banner do Porto de Santos
st.markdown("""
<style>
    /* Background com imagem do Porto de Santos */
    .stApp {
        background-image: 
            linear-gradient(
                rgba(5, 10, 30, 0.82), 
                rgba(5, 10, 30, 0.82)
            ),
            url("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Porto_de_Santos.jpg/1280px-Porto_de_Santos.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }

    /* Header hero com imagem mais visível */
    .hero-banner {
        background-image: 
            linear-gradient(
                rgba(5, 10, 30, 0.55), 
                rgba(5, 10, 30, 0.90)
            ),
            url("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Porto_de_Santos.jpg/1280px-Porto_de_Santos.jpg");
        background-size: cover;
        background-position: center top;
        border-radius: 20px;
        padding: 60px 40px 50px 40px;
        margin-bottom: 20px;
        border: 1px solid rgba(100, 181, 246, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
    }

    /* Título principal */
    .hero-title {
        font-size: 56px;
        font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #64B5F6, #42A5F5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: none;
        line-height: 1.1;
    }

    .hero-subtitle {
        color: #B3D9F7;
        font-size: 20px;
        margin-top: 12px;
        font-weight: 300;
        letter-spacing: 1px;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(100, 181, 246, 0.2);
        border: 1px solid rgba(100, 181, 246, 0.5);
        color: #64B5F6;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 13px;
        margin-top: 15px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, 
            rgba(30, 58, 95, 0.85), 
            rgba(45, 90, 142, 0.85));
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(61, 122, 181, 0.6);
        text-align: center;
        margin: 5px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #64B5F6;
    }

    .metric-label {
        font-size: 13px;
        color: #90CAF9;
        margin-top: 5px;
    }

    /* Sidebar */
    div[data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, 
            rgba(10, 20, 40, 0.97) 0%, 
            rgba(15, 30, 60, 0.97) 100%);
        border-right: 1px solid rgba(45, 90, 142, 0.5);
        backdrop-filter: blur(20px);
    }

    /* Labels da sidebar */
    .stSelectbox label, 
    .stSlider label, 
    .stMultiSelect label {
        color: #90CAF9 !important;
    }

    /* Seção de conteúdo */
    .content-section {
        background: rgba(10, 14, 30, 0.75);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(45, 90, 142, 0.4);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }

    /* Divider customizado */
    hr {
        border-color: rgba(45, 90, 142, 0.4) !important;
    }

    /* Barra de progresso */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1E88E5, #64B5F6) !important;
    }

    /* Textos gerais */
    h1, h2, h3, h4 { 
        color: #E8F4FD !important; 
    }

    p, span, div {
        color: #B3D9F7;
    }

    /* Info boxes */
    .info-box {
        background: rgba(30, 58, 95, 0.7);
        padding: 14px;
        border-radius: 10px;
        font-size: 13px;
        color: #90CAF9;
        border: 1px solid rgba(61, 122, 181, 0.3);
        backdrop-filter: blur(5px);
    }

    /* Watermark Porto de Santos */
    .porto-tag {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 58, 95, 0.8);
        border: 1px solid rgba(100, 181, 246, 0.4);
        border-radius: 25px;
        padding: 6px 16px;
        font-size: 12px;
        color: #64B5F6;
        letter-spacing: 1px;
        backdrop-filter: blur(5px);
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


# ─────────────────────────────
# FUNÇÕES
# ─────────────────────────────

def criar_caixa_3d(x, y, z, dx, dy, dz, cor, cor_borda, opacidade=0.75):
    """Cria uma caixa 3D com faces e bordas"""

    vx = [x,    x+dx, x+dx, x,    x,    x+dx, x+dx, x   ]
    vy = [y,    y,    y+dy, y+dy, y,    y,    y+dy, y+dy ]
    vz = [z,    z,    z,    z,    z+dz, z+dz, z+dz, z+dz ]

    i_idx = [0, 0, 0, 0, 4, 4, 3, 3, 1, 1, 2, 2]
    j_idx = [1, 2, 4, 5, 5, 6, 7, 6, 2, 5, 3, 6]
    k_idx = [2, 3, 5, 6, 6, 7, 6, 2, 5, 6, 6, 7]

    mesh = go.Mesh3d(
        x=vx, y=vy, z=vz,
        i=i_idx, j=j_idx, k=k_idx,
        color=cor,
        opacity=opacidade,
        flatshading=True,
        lighting=dict(
            ambient=0.6,
            diffuse=0.9,
            specular=0.3,
            roughness=0.5,
            fresnel=0.2
        ),
        lightposition=dict(x=1000, y=1000, z=1000),
        showscale=False,
        hoverinfo='skip'
    )

    arestas = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]

    edge_x, edge_y, edge_z = [], [], []
    for (a, b) in arestas:
        edge_x += [vx[a], vx[b], None]
        edge_y += [vy[a], vy[b], None]
        edge_z += [vz[a], vz[b], None]

    bordas = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color=cor_borda, width=2),
        hoverinfo='skip',
        showlegend=False
    )

    return mesh, bordas


def criar_container_wireframe(container: Container):
    """Cria wireframe translúcido do container"""
    c = container
    traces = []

    faces = go.Mesh3d(
        x=[0, c.comp, c.comp, 0,      0,      c.comp, c.comp, 0     ],
        y=[0, 0,      c.larg, c.larg, 0,      0,      c.larg, c.larg],
        z=[0, 0,      0,      0,      c.alt,  c.alt,  c.alt,  c.alt ],
        i=[0, 0, 0, 0, 4, 4],
        j=[1, 2, 4, 5, 5, 6],
        k=[2, 3, 5, 6, 6, 7],
        opacity=0.08,
        color='#64B5F6',
        flatshading=True,
        showscale=False,
        hoverinfo='skip',
        name='Container'
    )
    traces.append(faces)

    vx = [0, c.comp, c.comp, 0,      0,      c.comp, c.comp, 0     ]
    vy = [0, 0,      c.larg, c.larg, 0,      0,      c.larg, c.larg]
    vz = [0, 0,      0,      0,      c.alt,  c.alt,  c.alt,  c.alt ]

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

    arestas_trace = go.Scatter3d(
        x=ex, y=ey, z=ez,
        mode='lines',
        line=dict(color='#64B5F6', width=3),
        name='Container',
        hoverinfo='skip'
    )
    traces.append(arestas_trace)

    return traces


def calcular_e_plotar(container: Container, caixa: Caixa, percentual: int = 100):
    """Calcula e cria a visualização 3D"""

    qtd_c = int(container.comp / caixa.comp)
    qtd_l = int(container.larg / caixa.larg)
    qtd_a = int(container.alt  / caixa.alt )

    total_vol  = qtd_c * qtd_l * qtd_a
    max_peso   = int(container.peso_max / caixa.peso)
    total_real = min(total_vol, max_peso)
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
                    x, y, z,
                    caixa.comp, caixa.larg, caixa.alt,
                    caixa.cor, caixa.cor_borda, opacidade
                )
                all_traces.append(mesh)
                all_traces.append(bordas)
                count += 1
            if count >= qtd_mostrar:
                break
        if count >= qtd_mostrar:
            break

    fig = go.Figure(data=all_traces)
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
                tickfont=dict(color='#90CAF9'),
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
                tickfont=dict(color='#90CAF9'),
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
                tickfont=dict(color='#90CAF9'),
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

    vol_pct  = (total_real * caixa.comp * caixa.larg * caixa.alt) / \
               (container.comp * container.larg * container.alt) * 100
    peso_pct = (total_real * caixa.peso / container.peso_max) * 100

    stats = {
        'total':      total_real,
        'mostradas':  qtd_mostrar,
        'qtd_c':      qtd_c,
        'qtd_l':      qtd_l,
        'qtd_a':      qtd_a,
        'peso_total': total_real * caixa.peso,
        'vol_pct':    vol_pct,
        'peso_pct':   peso_pct,
        'limitador':  'Peso ⚖️' if max_peso < total_vol else 'Volume 📦'
    }

    return fig, stats


# ─────────────────────────────
# INTERFACE
# ─────────────────────────────

# ─── HERO BANNER com Porto de Santos ───
st.markdown("""
<div class='hero-banner'>
    <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
        <div>
            <div class='porto-tag'>⚓ Porto de Santos — SP, Brasil</div>
            <h1 class='hero-title' style='margin-top:16px;'>
                🚢 Container 3D Optimizer
            </h1>
            <p class='hero-subtitle'>
                Sistema inteligente de otimização e visualização de carga em containers
            </p>
            <div style='display:flex; gap:12px; margin-top:20px; flex-wrap:wrap;'>
                <span class='hero-badge'>📦 Multi-container</span>
                <span class='hero-badge'>🎯 Visualização 3D</span>
                <span class='hero-badge'>⚖️ Controle de Peso</span>
                <span class='hero-badge'>📊 Análise em Tempo Real</span>
            </div>
        </div>
        <div style='text-align:right; color:#64B5F6; font-size:80px; opacity:0.6;'>
            🚢
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Sidebar ───
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0 5px 0;'>
        <div style='font-size:40px;'>🚢</div>
        <h2 style='color:#64B5F6; margin:5px 0;'>Configurações</h2>
        <div class='porto-tag' style='font-size:11px;'>Porto de Santos</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    container_nome = st.selectbox("🚢 Tipo de Container", list(CONTAINERS.keys()))
    container = CONTAINERS[container_nome]

    st.markdown("---")

    caixa_nome = st.selectbox("📦 Tipo de Caixa", list(CAIXAS.keys()))
    caixa = CAIXAS[caixa_nome]

    if "Custom" in caixa_nome:
        st.markdown("#### 🔧 Dimensões Personalizadas")
        c_comp = st.slider("Comprimento (cm)", 10, 200, 40)
        c_larg = st.slider("Largura (cm)",     10, 200, 30)
        c_alt  = st.slider("Altura (cm)",      10, 200, 25)
        c_peso = st.slider("Peso (kg)",         1, 500,  5)
        caixa  = Caixa("Custom", c_comp, c_larg, c_alt, c_peso,
                        "rgba(200,100,255,0.7)", "#cc44ff")

    st.markdown("---")

    percentual = st.slider(
        "🔄 Percentual de Carga",
        min_value=0, max_value=100, value=100, step=5,
        help="Arraste para simular diferentes níveis de preenchimento"
    )

    st.markdown("---")

    st.markdown("<h4 style='color:#64B5F6;'>📐 Container</h4>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class='info-box'>
        <b>Tipo:</b> {container.tipo}<br>
        <b>Dimensões:</b> {container.comp}×{container.larg}×{container.alt} cm<br>
        <b>Volume:</b> {container.comp * container.larg * container.alt / 1e6:.1f} m³<br>
        <b>Carga Máx:</b> {container.peso_max:,} kg
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='color:#64B5F6; margin-top:12px;'>📦 Caixa</h4>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class='info-box'>
        <b>Tipo:</b> {caixa.nome}<br>
        <b>Dimensões:</b> {caixa.comp}×{caixa.larg}×{caixa.alt} cm<br>
        <b>Volume:</b> {caixa.comp * caixa.larg * caixa.alt / 1e6:.4f} m³<br>
        <b>Peso:</b> {caixa.peso} kg
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <p style='text-align:center; color:#2d5a8e; font-size:11px;'>
        ⚓ Porto de Santos, SP<br>
        🚢 Maior porto da América Latina
    </p>
    """, unsafe_allow_html=True)


# ─── Calcular ───
fig, stats = calcular_e_plotar(container, caixa, percentual)


# ─── Métricas ───
st.markdown("""
<div class='content-section'>
    <h2 style='color:#64B5F6; margin-top:0;'>📊 Resultados da Otimização</h2>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='font-size:28px;'>📦</div>
        <div class='metric-value'>{stats['total']}</div>
        <div class='metric-label'>Total de Caixas</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='font-size:28px;'>✅</div>
        <div class='metric-value'>{stats['mostradas']}</div>
        <div class='metric-label'>Caixas Carregadas</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='font-size:28px;'>📐</div>
        <div class='metric-value'>{stats['vol_pct']:.1f}%</div>
        <div class='metric-label'>Volume Utilizado</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='font-size:28px;'>⚖️</div>
        <div class='metric-value'>{stats['peso_total']:,.0f}</div>
        <div class='metric-label'>Peso Total (kg)</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='font-size:28px;'>🎯</div>
        <div class='metric-value'>{stats['limitador']}</div>
        <div class='metric-label'>Fator Limitante</div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")


# ─── Gráfico 3D ───
st.markdown("""
<div class='content-section'>
    <h2 style='color:#64B5F6; margin-top:0;'>🎯 Visualização 3D do Container</h2>
    <p style='color:#90CAF9; font-size:14px; margin-bottom:10px;'>
        💡 <b>Dica:</b> Arraste para rotacionar 
        | Scroll para zoom 
        | Duplo clique para resetar a câmera
    </p>
</div>
""", unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")


# ─── Barras de progresso ───
st.markdown("""
<div class='content-section'>
    <h3 style='color:#64B5F6; margin-top:0;'>📈 Utilização do Container</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<p style='color:#90CAF9;'>📦 Utilização de Volume</p>",
                unsafe_allow_html=True)
    st.progress(min(stats['vol_pct'] / 100, 1.0))
    st.markdown(
        f"<p style='color:#64B5F6; font-size:22px; font-weight:bold;'>"
        f"{stats['vol_pct']:.1f}%</p>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown("<p style='color:#90CAF9;'>⚖️ Utilização de Peso</p>",
                unsafe_allow_html=True)
    st.progress(min(stats['peso_pct'] / 100, 1.0))
    st.markdown(
        f"<p style='color:#64B5F6; font-size:22px; font-weight:bold;'>"
        f"{stats['peso_pct']:.1f}%</p>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")


# ─── Arranjo Espacial ───
st.markdown("""
<div class='content-section'>
    <h3 style='color:#64B5F6; margin-top:0;'>📐 Arranjo Espacial das Caixas</h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='font-size:24px;'>↔️</div>
        <div class='metric-value'>{stats['qtd_c']}</div>
        <div class='metric-label'>Colunas (Comprimento)</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='font-size:24px;'>↕️</div>
        <div class='metric-value'>{stats['qtd_l']}</div>
        <div class='metric-label'>Fileiras (Largura)</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div style='font-size:24px;'>🔝</div>
        <div class='metric-value'>{stats['qtd_a']}</div>
        <div class='metric-label'>Camadas (Altura)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ─── Footer ───
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding: 20px;
            background: rgba(10,14,30,0.6); 
            border-radius: 15px;
            border: 1px solid rgba(45,90,142,0.3);'>
    <div style='font-size:32px; margin-bottom:8px;'>⚓</div>
    <p style='color:#64B5F6; font-size:15px; margin:0; font-weight:bold;'>
        Porto de Santos — São Paulo, Brasil
    </p>
    <p style='color:#2d5a8e; font-size:12px; margin:5px 0 0 0;'>
        🚢 Maior porto da América Latina &nbsp;|&nbsp; 
        Container 3D Optimizer &nbsp;|&nbsp; 
        Desenvolvido com Streamlit + Plotly 🚀
    </p>
</div>
""", unsafe_allow_html=True)
