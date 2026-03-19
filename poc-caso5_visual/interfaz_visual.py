import streamlit as st
import os
import time
import json
import base64
import random
import hashlib
from datetime import datetime

# Importar lógica
from logica_blockchain import Blockchain, Transaction
import streamlit.components.v1 as components

# Configuración Máxima Web3: FULL SCREEN & NO SCROLL
st.set_page_config(
    page_title="Blockchain Forensic v7.5 - Onboarding", 
    page_icon="💎", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- LOAD STYLES ---
def get_css_content(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()
    return ""

css_content = get_css_content("config_estilos.css")

# --- INITIALIZATION ---
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain(difficulty=2)
    st.session_state.blockchain.add_block([Transaction("C_Alice", "C_Bob", 25.0)])
    st.session_state.blockchain.add_block([Transaction("Ex_Binance", "User_77", 4.9)])

if "mining_mode" not in st.session_state: st.session_state.mining_mode = False
if "fly_animation" not in st.session_state: st.session_state.fly_animation = False
if "tutor_mode" not in st.session_state: st.session_state.tutor_mode = True
if "success_anim" not in st.session_state: st.session_state.success_anim = None
if "tour_active" not in st.session_state: st.session_state.tour_active = False
if "tour_step" not in st.session_state: st.session_state.tour_step = 0

bc = st.session_state.blockchain

# --- VALIDATION ---
is_valid, errors = bc.is_chain_valid()
trust_score = 100 if is_valid else max(0, 100 - (len(errors) * 25))
status_color = "#57ab5a" if is_valid else "#e5534b"
status_text = "🛡️ RED ÍNTEGRA" if is_valid else "🚨 RED CORRUPTA"

# --- SIDEBAR (PANEL MAESTRO) ---
trust_angle = -90 + (trust_score / 100 * 180)

st.sidebar.markdown(f"""
<div id="tour-step-1" style='text-align:center; display:flex; flex-direction:column; align-items:center; width:100%;'>
    <h1 style='color: {status_color}; font-size:1.4rem; margin-bottom:10px; width:100%;'>💎 Forensic Red v7.0</h1>
    <div class="gauge-container {'is-broken' if not is_valid else ''}" style="margin: 0 auto;">
        <div class="gauge-arc"></div>
        <div class="gauge-mask"></div>
        <div class="gauge-needle" style="transform: rotate({trust_angle}deg);"></div>
        <div class="broken-glass"></div>
        <div style="position: absolute; bottom: 5px; font-weight: 800; font-size: 14px; color: {status_color}; text-shadow: 0 0 10px rgba(0,0,0,0.5); width:100%;">{trust_score}% TRUST</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Tour Controls
if st.sidebar.button("🚀 Iniciar Tour Guiado", use_container_width=True):
    st.session_state.tour_active = True
    st.session_state.tour_step = 0
    st.rerun()

st.session_state.tutor_mode = st.sidebar.toggle("🎓 Modo Tutor", value=st.session_state.tutor_mode)

# Mempool Controls
with st.sidebar.expander("📥 Central de Mempool", expanded=True):
    m_sender = st.text_input("Emisor", value=f"User_{random.randint(10,99)}")
    m_receiver = st.text_input("Receptor", value=f"Node_{random.randint(100,999)}")
    m_amount = st.number_input("BTC", min_value=0.1, value=12.5)
    if st.button("➕ Lanzar a Mempool", use_container_width=True):
        bc.add_transaction(m_sender, m_receiver, m_amount)
        st.rerun()
    
    if bc.mempool:
        if st.button("⛏️ Iniciar Minado PoW", type="primary", use_container_width=True):
            st.session_state.fly_animation = True
            st.rerun()

# Reporting
if st.sidebar.button("📜 Generar Reporte", use_container_width=True):
    st.toast("Reporte generado con hash de transparencia.")

# Forensic Lab (Attack)
with st.sidebar.container(): 
    st.markdown('<div id="tour-step-6"></div>', unsafe_allow_html=True)
    with st.expander("😈 Forensic Lab: Ataque Directo", expanded=is_valid == False):
        if len(bc.chain) > 1:
            att_idx = st.selectbox("Bloque Víctima:", options=[b.index for b in bc.chain if b.index > 0])
            att_val = st.number_input("Alterar Monto (HACK):", value=999.0)
            if st.button("🚀 Secuestrar Nodo", use_container_width=True):
                bc.inject_malicious_data(att_idx, att_val)
                st.rerun()

# Reset
if st.sidebar.button("🗑️ Reiniciar Ecosistema", use_container_width=True):
    st.session_state.blockchain = Blockchain(difficulty=2)
    st.session_state.tour_active = False
    st.rerun()

# --- GFX ENGINE FUNCTIONS ---

def get_mempool_live_html(mempool, animating=False):
    if not mempool and not animating: return ""
    hex_html = ""
    for i, tx in enumerate(mempool):
        priority = "priority-high" if tx.amount > 10 else ""
        fly_class = "mempool-fly" if animating else ""
        modal_id = f"modal_{i}"
        hex_html += f"""
        <div class="tx-hex {priority} {fly_class}" onclick="document.getElementById('{modal_id}').style.display='flex'">
            <div style="font-size: 8px; color: white; display:flex; align-items:center; justify-content:center; height:100%;">{tx.amount}</div>
        </div>
        """
    return f'<div id="tour-target-mempool" class="mempool-area"><h4><div id="tour-step-2"></div>🧊 SALA DE ESPERA (MEMPOOL LIVE)</h4><div class="mempool-grid">{hex_html}</div></div>'

def get_mining_hash_visual(hash_str, difficulty):
    target = "0" * difficulty
    colored_hash = ""
    for i, char in enumerate(hash_str):
        if i < difficulty and char == '0': colored_hash += f'<span style="color:#57ab5a; font-weight:bold;">{char}</span>'
        else: colored_hash += f'<span style="opacity:0.6;">{char}</span>'
    return colored_hash

def get_blockchain_v7_html(blockchain, mining_idx=None, mining_nonce=0, mining_hash=""):
    blocks_html = ""
    for i, b in enumerate(blockchain.chain):
        is_genesis = (b.index == 0)
        is_mining = (b.index == mining_idx)
        valid_local = True
        broken_link = False
        if i > 0:
            prev = blockchain.chain[i-1]
            if b.merkle_root != b.calculate_merkle_root() or b.hash != b.calculate_hash() or b.previous_hash != prev.hash:
                valid_local = False
                if b.previous_hash != prev.hash: broken_link = True
        
        theme_class = "is-valid" if valid_local else "is-invalid"
        if is_genesis: theme_class = "is-genesis"
        if is_mining: theme_class += " mining-active"
        
        seal_html = '<div class="golden-seal">🏆</div>' if st.session_state.success_anim == b.index else ""
        p_hash_disp = b.previous_hash[:16] + "..." if i > 0 else "0" * 16
        m_root_disp = b.merkle_root[:16] + "..."
        b_hash_disp = b.hash[:16] + "..."
        if is_mining: b_hash_disp = get_mining_hash_visual(mining_hash[:22], blockchain.difficulty)

        node_html = f"""
        <div class="block-node {theme_class}">
            {seal_html}
            <div class="header-box">
                {('<div class="genesis-badge">GÉNESIS</div>' if is_genesis else '')}
                <div class="block-id">BLOQUE #{b.index}</div>
                <div class="nonce-badge">NONCE: {mining_nonce if is_mining else b.nonce}</div>
                <div class="header-field"><span class="field-label">Previous Hash</span><span class="field-value">{p_hash_disp}</span></div>
                <div class="header-field"><span class="field-label">Merkle Root</span><span class="field-value">{m_root_disp}</span></div>
                <div class="header-field" style="border-width:2px; border-color: {status_color if valid_local else 'rgba(0,0,0,0.5)'} !important; background: rgba(0,0,0,0.5);">
                    <span class="field-label">Huella Digital (Hash)</span><span class="field-value" style="color:#ffffff !important;">{b_hash_disp}</span>
                </div>
            </div>
            <div class="tx-box" style="background:rgba(83,155,245,0.05); border-radius:12px; border:1px solid rgba(83,155,245,0.1); margin-top:10px;">
                <div style="font-size: 11px;"><b>DATOS:</b> {b.transactions[0].sender if b.transactions else "Root"}</div>
            </div>
            {('<div class="block-link"></div>' if i < len(blockchain.chain)-1 else '')}
            {('<div class="broken-link-icon" style="right:-65px; top:45%; position:absolute;">🔗❌</div>' if broken_link else '')}
        </div>
        """
        blocks_html += node_html
    return f'<div id="tour-step-5" class="viz-area">{blocks_html}</div>'

# --- ONBOARDING TOUR ENGINE ---

def render_onboarding_layer():
    if not st.session_state.tour_active: return ""
    
    steps = [
        {"target": "#tour-step-1", "title": "🛡️ Panel Maestro", "content": "Bienvenido al centro de mando. Aquí monitoreamos el Trust Score de la red."},
        {"target": "#tour-step-2", "title": "🧊 Mempool Live", "content": "Esta es la sala de espera. Aquí llegan las transacciones antes de ser procesadas."},
        {"target": "div[data-testid='stExpander']", "title": "📥 Mempool Ops", "content": "Desde aquí actúas como usuario. Crea transacciones enviando BTC."},
        {"target": "button[kind='primary']", "title": "⛏️ Prueba de Trabajo", "content": "Aquí ocurre la magia del PoW. Minar un bloque requiere poder computacional."},
        {"target": "#tour-step-5", "title": "🔗 Visor de Cadena", "content": "Observa los eslabones inmutables protegidos por criptografía."},
        {"target": "#tour-step-6", "title": "😈 Forensic Lab", "content": "¡El laboratorio de hacking! Intenta secuestrar un bloque y verás el efecto dominó."},
        {"target": "button:contains('Reporte')", "title": "📜 Transparencia", "content": "Finalmente, genera tu reporte de auditoría inmutable."}
    ]
    
    curr = st.session_state.tour_step
    if curr >= len(steps): 
        st.session_state.tour_active = False
        st.rerun()
        return ""
    
    step = steps[curr]
    
    # Spotlight JS logic
    js_spotlight = f"""
    <script>
        const observer = new MutationObserver((mutations) => {{
            const el = window.parent.document.querySelector("{step['target']}");
            if (el) {{
                window.parent.document.querySelectorAll('.tour-highlight').forEach(x => x.classList.remove('tour-highlight'));
                el.classList.add('tour-highlight');
                observer.disconnect();
            }}
        }});
        observer.observe(window.parent.document.body, {{ childList: true, subtree: true }});
    </script>
    """
    
    # Modal UI
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 🚀 Tour: {step['title']}")
    st.sidebar.info(step['content'])
    
    col1, col2 = st.sidebar.columns(2)
    if col1.button("⬅️ Atrás", disabled=curr==0, use_container_width=True):
        st.session_state.tour_step -= 1
        st.rerun()
    if col2.button("➡️ Siguiente" if curr < len(steps)-1 else "🏁 Finalizar", use_container_width=True, type="primary"):
        st.session_state.tour_step += 1
        st.rerun()
    
    if st.sidebar.button("❌ Omitir Tour", use_container_width=True):
        st.session_state.tour_active = False
        st.rerun()

    return js_spotlight

# --- RENDER FLOW ---

viz_placeholder = st.empty()

def render_frame(m_anim=False, m_idx=None, m_nonce=0, m_hash=""):
    tour_script = render_onboarding_layer()
    full_html = f"""
    <style>{css_content}</style>
    <div class="main-renderer">
        {get_mempool_live_html(bc.mempool, m_anim)}
        {get_blockchain_v7_html(bc, m_idx, m_nonce, m_hash)}
    </div>
    {tour_script}
    """
    with viz_placeholder:
        components.html(full_html, height=850, scrolling=True)

# Main Sequences
if st.session_state.fly_animation:
    render_frame(m_anim=True)
    time.sleep(1.2)
    st.session_state.fly_animation = False
    st.session_state.mining_mode = True
    bc.add_block_from_mempool()
    st.rerun()

elif st.session_state.mining_mode:
    block = bc.chain[-1]
    for _ in range(25):
        block.mine_block_step(bc.difficulty, batch_size=40)
        render_frame(m_idx=block.index, m_nonce=random.randint(1000, 99999), m_hash=block.hash)
        time.sleep(0.05)
    block.mine_block(bc.difficulty)
    st.session_state.success_anim = block.index
    st.session_state.mining_mode = False
    render_frame(m_idx=block.index, m_nonce=block.nonce, m_hash=block.hash)
    time.sleep(1.2)
    st.session_state.success_anim = None
    st.rerun()

else:
    render_frame()

st.markdown("<div style='position: fixed; bottom: 10px; right: 20px; font-size: 0.7rem; opacity: 0.4;'>Blockchain UX Architect v7.5 | Onboarding Mode</div>", unsafe_allow_html=True)
