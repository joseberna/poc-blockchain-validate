# 🧊 Blockchain Forensic Dashboard v4.0

### 🛡️ Proyecto: Detección de Manipulación y Auditoría Forense
**Talento Tech - Módulo de Seguridad Blockchain**

Este proyecto es una aplicación web interactiva diseñada para visualizar, auditar y simular ataques en una red Blockchain siguiendo el estándar de estructura de **Bitcoin (INESEM)**. Desarrollada con un enfoque en **Growth Hacking** y **UX Premium**, permite a desarrolladores y auditores comprender la inmutabilidad criptográfica a través de la experimentación directa.

---

## 👥 Equipo de Desarrollo
- 👨‍💻 **Jose Berna** (Lead Fullstack & Blockchain Dev)
- 👩‍💻 **Nilcen Patricia** (Blockchain Auditor & QA)
- 👨‍💻 **Esteban Moncada** (UX/UI & Frontend Engineer)

---

## 🌟 Características Principales

- **Estructura Estándar Bitcoin:** Visualización de bloques con Header, Merkle Root, Nonce y Lista de Transacciones.
- **Bloque Génesis Distinguido:** Identificación visual única (Gold Glow) del primer bloque de la cadena.
- **Simulador de Ataques Shadow:** Permite alterar montos en bloques pasados y observar el "Efecto Dominó" que rompe la inmutabilidad.
- **Trust Score dinámico:** Indicador de confianza en tiempo real que cae al detectar inconsistencias de red.
- **Interfaz Zero-Scroll:** Dashboard responsivo de pantalla completa con visor horizontal suave.
- **Certificado de Integridad:** Exportación de reportes de auditoría en formato PDF con firma digital del último hash.
- **Modo Tutor Permanente:** Explicaciones contextuales integradas para facilitar el aprendizaje de conceptos como Hashing y Merkle Trees.

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** [Python 3.x](https://www.python.org/)
- **Web App Framework:** [Streamlit](https://streamlit.io/)
- **Lógica Criptográfica:** hashlib (SHA-256)
- **Reportes:** FPDF (Generación de certificados)
- **UI/UX:** HTML5 / CSS3 (Componentes personalizados Web3)

---

## 🚀 Guía de Instalación y Ejecución

Sigue estos pasos para poner a correr el dashboard en tu máquina local:

### 1. Clonar o acceder a la carpeta del proyecto
```bash
cd poc-caso5_visual
```

### 2. Crear y activar un entorno virtual (Recomendado)
```bash
python3 -m venv venv
source venv/bin/activate  # En Mac/Linux
# venv\Scripts\activate   # En Windows
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Lanzar la Aplicación
```bash
streamlit run interfaz_visual.py
```

---

## 📂 Estructura del Código

- `logica_blockchain.py`: Contiene las clases `Block`, `Transaction` y `Blockchain`. Maneja el minado (PoW), el cálculo de Merkle Roots y la validación de integridad.
- `interfaz_visual.py`: El cerebro de la interfaz de usuario. Renderiza los bloques usando componentes HTML inyectados y gestiona el flujo de estados.
- `config_estilos.css`: Hoja de estilos premium que define la identidad visual Web3 (colores, sombras, badges y animaciones de red).
- `requirements.txt`: Lista de librerías necesarias para el funcionamiento óptimo del sistema.

---

## 🕵️ Flujo Sugerido de Auditoría
1. **Minado:** Añade un par de bloques para construir historial.
2. **Observación:** Revisa cómo el `Previous Hash` de un bloque coincide con el `Header Hash` del anterior.
3. **Ataque:** Selecciona un bloque del pasado y altera su monto. Observa cómo la red se torna **Roja** (Falla de Integridad).
4. **Verificación:** Lee el panel forense para entender por qué la cadena se ha fracturado matemáticamente.
5. **Reinicio:** Presiona "Reiniciar Red Genesis" para volver a un estado de confianza total.

---
© 2026 - Proyecto Educativo para Talento Tech.
