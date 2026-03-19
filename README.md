# 💎 Blockchain Forensic Core & GUI v7.5 (Platinum Standard)

![Blockchain Banner](https://img.shields.io/badge/Status-Secured-brightgreen)
![Python 3.14+](https://img.shields.io/badge/Python-3.14%2B-blue)
![Streamlit 1.30+](https://img.shields.io/badge/Streamlit-1.30%2B-red)

Repositorio oficial del **Simulador Forense de Cadenas de Bloques (Caso 5)**. Una herramienta avanzada diseñada para la educación en ciberseguridad blockchain, auditoría de integridad y simulación de ataques de red.

---

### 🚀 Características de Élite

#### 1. 🏗️ Estructura Bitcoin Standard
Implementación de una verdadera arquitectura de bloques con **Header, Content y Footer**. Soporta hashing SHA-256 distribuido y validación de punteros `previous_hash`.

#### 2. 🧊 Mempool Live (Bitcoin Space)
Visualización interactiva de transacciones no confirmadas.
- **Hexagons 3D**: Cada transacción es un hexágono pulsante con prioridad por monto (Fees).
- **Detalle Forensic**: Al hacer clic, se abre una ventana modal con el TXID, Sender, Receiver y monto.
- **Vortex Flight**: Animación cinemática de las transacciones volando desde la Mempool hacia el nuevo bloque durante el minado.

#### 3. ⛏️ Hyper-Realistic PoW Visualizer
- **Slot Machine Loop**: El Nonce se calcula con una animación de cambio ultra-rápida.
- **Hash Progress Bar**: Los caracteres del hash cambian a verde conforme se acercan a la dificultad configurada.
- **Golden Seal**: Sello visual de éxito (🏆) al encontrar el Nonce válido.

#### 4. 😈 Forensic Lab & Attack Simulator
- **Block Hijacking**: Capacidad de secuestrar cualquier bloque y alterar sus datos internos (Monto, Sender, etc.).
- **Detección Forense**: Visualizador de "Diferencia de Hash" carácter por carácter para detectar manipulaciones exactas.
- **Efecto Dominó**: Animación de ruptura física de eslabones al detectarse corrupción en la red.

#### 5. 🛡️ Trust Meter & 🎓 Modo Tutor
- **Dial Dinámico**: Aguja animada que mide la salud de la red en tiempo real.
- **Onboarding Spotlight**: Tour guiado interactivo que oscurece la pantalla y resalta los componentes principales mientras los explica con lenguaje sencillo.

---

### 🛠️ Tech Stack & Arquitectura

- **Backend**: Python 3.x (Pure Logic, Hashing, Object Orientation).
- **Frontend**: Streamlit + Custom CSS3/HTML5 (Animations, Transitions, Flexbox/Grid).
- **Criptografía**: SHA-256 nativo (hashlib).
- **Design System**: Carbon Dark UI with Forensic Red & Cyber Blue accents.

---

### 📦 Estructura de Archivos

- `core.py`: Lógica criptográfica central de la Blockchain.
- `security.py`: Motor de auditoría forense y simulación de ataques.
- `main.py`: Interfaz de terminal (CLI) para auditorías rápidas.
- `poc-caso5_visual/`:
  - `interfaz_visual.py`: El corazón del dashboard v7.5.
  - `config_estilos.css`: El motor de animaciones y diseño premium.
  - `logica_blockchain.py`: Extensión de la lógica central para el dashboard visual.

---

### ⚡ Instalación y Ejecución

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/joseberna/poc-blockchain-validate.git
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Lanzar Experiencia Visual GUI**:
   ```bash
   streamlit run poc-caso5_visual/interfaz_visual.py
   ```

5. **Lanzar Auditoría CLI (Terminal)**:
   ```bash
   python main.py
   ```

---

### 🎓 Educativo: ¿Qué estoy aprendiendo?

Este simulador enseña conceptos fundamentales para especialistas en seguridad:
- **Inmutabilidad**: ¿Por qué un cambio en el bloque 1 rompe el bloque 10?
- **Proof of Work**: El costo computacional de re-escribir la historia.
- **Merkle Roots**: Cómo asegurar miles de transacciones con un solo hash.
- **Mempool**: La jerarquía de prioridad en redes distribuidas.

---
*Desarrollado con ❤️ por el **Blockchain UI Architect v7.5** | Forensic Standard Solutions.*
