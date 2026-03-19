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

# Configuración Maverick v10.6 "The Forensic Gold"
st.set_page_config(
    page_title="Blockchain Forensic v10.6", 
    page_icon="🛡️", 
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
    # Datos iniciales realistas
    st.session_state.blockchain.add_block([Transaction("Exchange_Alpha", "Vault_01", 325.4)])
    st.session_state.blockchain.add_block([Transaction("Vault_01", "Miner_X", 12.8)])

if "mining_mode" not in st.session_state: st.session_state.mining_mode = False
if "fly_animation" not in st.session_state: st.session_state.fly_animation = False
if "success_anim" not in st.session_state: st.session_state.success_anim = None

bc = st.session_state.blockchain

# --- VALIDATION ENGINE ---
is_valid, errors = bc.is_chain_valid()
trust_val = 100 if is_valid else max(0, 100 - (len(errors) * 33))
status_color = "#21ba45" if is_valid else "#ef4444"

# --- SIDEBAR (Master Audit Panel) ---
st.sidebar.markdown(f"<h1 style='color:#539bf5; font-size:1.8rem; text-align:center;'>🛡️ FORENSIC <span style='color:white;'>v10.6</span></h1>", unsafe_allow_html=True)

# Audit Console
st.sidebar.markdown(f"""
<div style='background: #181b2a; border-left: 5px solid {status_color}; padding: 15px; border-radius: 4px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);'>
    <div style='font-size: 10px; color: #adbac7; letter-spacing: 1px;'>GLOBAL_AUDIT_STREAM</div>
    <div style='font-size: 14px; font-weight: bold; color: {status_color};'>{'INTEGRITY_VERIFIED' if is_valid else 'PROTOCOL_FAILURE'}</div>
    <div style='font-size: 10px; opacity:0.6; margin-top:5px;'>Chain Proof: {trust_val}% Reliable</div>
</div>
""", unsafe_allow_html=True)

if not is_valid:
    with st.sidebar.container():
        st.markdown("<div style='color:#ef4444; font-size:11px; margin-bottom:10px;'>🚨 AUDIT LOG (Where it broke):</div>", unsafe_allow_html=True)
        for err in errors:
            st.markdown(f"<div style='background:rgba(239,68,68,0.1); padding:8px; border-radius:4px; font-size:9px; margin-bottom:5px;'>❌ {err}</div>", unsafe_allow_html=True)

with st.sidebar.expander("📝 NEW TRANSACTION (MEMPOOL)", expanded=True):
    m_sender = st.sidebar.text_input("Origin Key", value=f"Addr_{random.randint(100,999)}")
    m_receiver = st.sidebar.text_input("Target Key", value=f"Addr_{random.randint(100,999)}")
    m_amount = st.sidebar.number_input("BTC", min_value=0.01, value=5.0, format="%.3f")
    if st.sidebar.button("➕ Inject into Cluster", use_container_width=True, help="Envía una transacción a la sala de espera (Mempool) para que los mineros la procesen."):
        bc.add_transaction(m_sender, m_receiver, m_amount)
        st.rerun()

if bc.mempool:
    if st.sidebar.button("⛏️ SEAL & MINE NEXT BLOCK", type="primary", use_container_width=True, help="Inicia la minería de Prueba de Trabajo (PoW) para sellar criptográficamente el bloque y añadirlo a la cadena."):
        st.session_state.fly_animation = True
        st.rerun()

with st.sidebar.expander("😈 ATTACK LAB (SIMULATE HACK)", expanded=is_valid==False):
    if len(bc.chain) > 0:
        att_idx = st.selectbox("Victim Block Index:", options=[b.index for b in bc.chain])
        att_val = st.number_input("Tampered Amount (BTC):", value=7777.0)
        if st.button("🚀 EXECUTE HIJACK", use_container_width=True, help="Simula una alteración maliciosa de los datos del bloque seleccionado. Esto romperá el Hash y la integridad de la red."):
            bc.inject_malicious_data(att_idx, att_val)
            st.rerun()

if not is_valid and st.sidebar.button("🔧 RESTORE 51% CONSENSUS", use_container_width=True, help="Aplica un ataque del 51% (re-minado) para corregir los hashes rotos y forzar un nuevo consenso en la red."):
    bc.repair_chain()
    st.rerun()

if st.sidebar.button("🗑️ RESET SIMULATION", use_container_width=True, help="Borra toda la historia de bloques y reinicia el sistema al Bloque Génesis."):
    st.session_state.blockchain = Blockchain(difficulty=2)
    st.rerun()

# --- MASTER RENDERER V10.6 ---

def get_block_v106(b, is_mempool=False, is_mining=False, m_nonce=0):
    theme_class = "mempool-block" if is_mempool else "mined-block"
    
    # Forensic Check
    real_hash = b.calculate_hash()
    is_hacked = (not is_mempool and not is_mining and b.hash != real_hash)
    if is_hacked: theme_class += " hacked-block"
    
    # Data Actual
    tx = b.transactions[0] if b.transactions else None
    tx_text = f"TX: {tx.sender[:8]}.. ➜ {tx.receiver[:8]}.." if tx else "BLOQUE GÉNESIS / RECOMPENSA"
    tx_btc = f"{tx.amount:,.3f} BTC" if tx else "0.00 BTC"
    
    fly_class = "flying" if st.session_state.fly_animation and is_mempool else ""
    
    # Tooltips Definiciones
    tt_height = "HEIGHT (Altura): El índice numérico del bloque. Determina su posición exacta en la línea de tiempo inmutable."
    tt_btc = "AMOUNT (Monto): Suma total de los activos transferidos en este bloque, derivados de las transacciones reales en la mempool."
    tt_fee = "AVG FEES (Comisión): Promedio de incentivos pagados por los usuarios para que el minero procese este bloque rápidamente."
    tt_stats = "STATS: Número de transacciones (TXs) y el tamaño físico del bloque en disco (MB)."
    tt_nonce = f"NONCE: Número único que los mineros cambian trillones de veces para encontrar un Hash válido que cumpla la dificultad: {b.difficulty} ceros iniciales."

    # Forensic Detail UI
    forensic_ui = ""
    if is_hacked:
        forensic_ui = f"""
        <div class="forensic-box" title="INTEGRITY FAILURE: Los datos internos (transacciones) fueron alterados manualmente. Al cambiar los datos, el Merkle Root cambio, invalidando el Hash del bloque inicial.">
            <div style="color:#ef4444; font-weight:bold; font-size:10px;">🚨 BREACH DETECTED</div>
            <div style="font-size:7px; margin-top:5px; color:#adbac7;">
                <b>HASH GUARDADO:</b> {b.hash[:16]}...<br>
                <b>HASH CALCULADO:</b> {real_hash[:16]}...<br>
                <span style="color:#ef4444;">Estatus: INCONSISTENTE</span>
            </div>
            <div style="font-size:7px; color:#ef4444; margin-top:5px; padding-top:4px; border-top:1px solid rgba(239, 68, 68, 0.3);">
                Causa: Alteración de Monto en Transacción #0.
            </div>
        </div>
        """
        
    return f"""
    <div class="block-box {theme_class} {fly_class}">
        <div class="box-header" title="{tt_height}">#{b.height if not is_mempool else 'PROYECTADO'}</div>
        <div class="box-btc" title="{tt_btc}">{tx_btc}</div>
        <div class="box-data" style="font-size:8px; opacity:0.8; text-align:center; margin-bottom:10px;">{tx_text}</div>
        <div class="box-fee" title="{tt_fee}">{b.median_fee} sat/vB</div>
        <div class="box-stats" title="{tt_stats}">
            {b.tx_count} TXs | {b.size_mb} MB
        </div>
        <div style="font-size:7px; color:#adbac7; margin-top:10px; text-align:center; font-family:monospace;" title="{tt_nonce}">NONCE: {m_nonce if is_mining else b.nonce}</div>
        {forensic_ui}
    </div>
    """

def render_v106_master(m_idx=None, m_nonce=0):
    # Futuro (Mempool)
    future_blocks = ""
    if bc.mempool:
        dummy = bc.chain[-1]
        future_blocks += get_block_v106(dummy, is_mempool=True)
    
    # Pasado (Mined)
    past_blocks = ""
    for b in reversed(bc.chain):
        is_mining = (b.index == m_idx)
        past_blocks += get_block_v106(b, is_mining=is_mining, m_nonce=m_nonce)
        
    # Tooltips Definiciones Charts
    exp_goggles = "Mempool Goggles™: Cada píxel es una transacción real. El color indica el Fee (Verde=Bajo, Naranja=Alto). Nota cómo fluctúan con la congestión de la red."
    exp_diff = "Difficulty Adjustment: Cuántos ceros debe tener el Hash al inicio para ser válido. Se ajusta automáticamente para mantener el bloque cada ~10 minutos."
    exp_memory = f"Memory Usage: Memoria RAM del nodo para almacenar transacciones pendientes (mempool). Actualmente: {100 + len(bc.mempool)*5} MB / 300 MB."
    
    # Goggles Generation
    pixels = ""
    for _ in range(200):
        opacity = random.uniform(0.1, 0.8)
        color = "#21ba45" if opacity < 0.6 else "#f59e0b"
        pixels += f'<div class="goggle-pixel" style="background:{color}; opacity:{opacity};" title="TX Status: Pending | Fee Level: {random.randint(1,100)} sat/vB"></div>'
    
    full_html = f"""
    <style>{css_content}</style>
    <div class="main-renderer">
        <div class="timeline-container">
            <div class="mempool-timeline">{future_blocks}</div>
            <div class="separator-pillar" title="UMBRAL DE INMUTABILIDAD: Las transacciones que cruzan esta línea son selladas criptográficamente por los mineros y se vuelven inalterables."></div>
            <div class="chain-timeline">{past_blocks}</div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-card" title="{exp_goggles}">
                <div class="chart-title">Mempool Goggles™ ⓘ</div>
                <div class="goggles-grid">{pixels}</div>
            </div>
            <div class="chart-card" title="{exp_diff}">
                <div class="chart-title">Difficulty Adjustment ⓘ</div>
                <div style="font-size: 24px; color: #21ba45; font-weight: bold;">+ 7.58 %</div>
                <div style="margin-top:20px; background: #2d333b; height: 10px; border-radius: 5px; overflow:hidden;">
                    <div style="width: 75%; background: linear-gradient(to right, #21ba45, #9a49f2); height: 100%;"></div>
                </div>
            </div>
            <div class="chart-card" title="{exp_memory}">
                <div class="chart-title">Memory Usage ⓘ</div>
                <div style="font-size: 24px; color: #f59e0b; font-weight: bold;">{100 + len(bc.mempool)*5} MB/300MB</div>
                <div style="margin-top:20px; background: #2d333b; height: 6px; border-radius: 3px;">
                    <div style="width: {(100 + len(bc.mempool)*5)/3}%; background: #f59e0b; height: 100%;"></div>
                </div>
            </div>
        </div>
    </div>
    """
    with st.container():
        components.html(full_html, height=850, scrolling=True)

# Main Sequences Logic
placeholder = st.empty()

if st.session_state.fly_animation:
    with placeholder: render_v106_master()
    time.sleep(1.0)
    st.session_state.fly_animation = False
    st.session_state.mining_mode = True
    bc.add_block_from_mempool()
    st.rerun()

elif st.session_state.mining_mode:
    block = bc.chain[-1]
    for _ in range(12):
        block.mine_block_step(bc.difficulty, batch_size=40)
        with placeholder: render_v106_master(m_idx=block.index, m_nonce=random.randint(1000, 99999))
        time.sleep(0.08)
    block.mine_block(bc.difficulty)
    st.session_state.mining_mode = False
    st.rerun()

else:
    with placeholder: render_v106_master()

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size: 0.7rem; opacity: 0.5; text-align:center;'>BLOCKCHAIN MASTER v10.6 | FORENSIC AUDIT<br>Expert Level Security Simulator</div>", unsafe_allow_html=True)
