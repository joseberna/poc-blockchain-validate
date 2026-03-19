import os
import sys
import logging
import time

logging.getLogger("BlockchainCore").setLevel(logging.CRITICAL)
logging.getLogger("BlockchainSecurity").setLevel(logging.CRITICAL)

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich import box
import questionary

from core import Blockchain, Transaction
from security import BlockchainAuditor

console = Console()

def display_master_concept(title: str, content: str):
    """Muestra la capa didáctica (Modo Tutor)."""
    console.print(Panel(
        f"[italic white]{content}[/italic white]",
        title=f"💡 [bold yellow]Concepto Master: {title}[/bold yellow]",
        border_style="yellow",
        box=box.ROUNDED
    ))

def display_network_state(blockchain: Blockchain, is_valid: bool = True, show_concept: bool = True):
    """Renderiza la vista estilo Dashboard."""
    if is_valid:
        title = "🛡️  DASHBOARD DE RED: [bold green]ACTIVO Y SEGURO[/bold green] (Integridad Validada)"
        b_style = "green"
    else:
        title = "🚨 DASHBOARD DE RED: [bold red]SISTEMA COMPROMETIDO[/bold red] (Manipulación Detectada)"
        b_style = "red"
        
    table = Table(title=title, show_header=True, header_style=f"bold {b_style}", border_style=b_style, expand=True)
    table.add_column("Index", style="cyan", justify="center")
    table.add_column("Tx Count", justify="center")
    table.add_column("Nonce (PoW)", style="blue", justify="center")
    table.add_column("Previous Hash", style="magenta")
    table.add_column("Block Hash (Signature)", style="yellow")
    
    for block in blockchain.chain:
        prev_h = f"{block.previous_hash[:10]}...{block.previous_hash[-10:]}" if len(block.previous_hash) > 20 else block.previous_hash
        curr_h = f"{block.hash[:10]}...{block.hash[-10:]}"
            
        table.add_row(
            str(block.index),
            str(len(block.data.transactions)),
            str(block.nonce),
            prev_h,
            curr_h
        )
        
    console.print(table)
    if show_concept:
        display_master_concept(
            "El Bloque Génesis e Inmutabilidad", 
            "El bloque 0 es el 'Génesis', anclado matemáticamente a un hash anterior de ceros. Cada bloque posterior depende directamente del hash del bloque anterior. Un cambio mínimo en la historia ('Efecto Dominó') invalida todos los hashes subsiguientes."
        )

def generate_certificate():
    """Genera un certificado ASCII."""
    cert = """[bold green]
=========================================================
  🛡️  CERTIFICADO DE INTEGRIDAD DE RED BLOCKCHAIN 🛡️   
=========================================================
      
           .,,,.                  
         ,;;;;;;;.         La red actual ha sido  
        ;;;;;;;;;;;        auditada y certificada 
        ;;;'   `';;        como 100% INMUTABLE.   
        ;;;     ;;;             
        `;;;,,,;;;'        Fecha Validada: {date}
         `';;;;;;'         Estado: AUDITORÍA APROBADA
      
    Firma Digital: 0xSecureChainProofVerifier99182
=========================================================[/bold green]
"""
    console.print(cert.replace("{date}", time.strftime("%Y-%m-%d %H:%M:%S")))

def run_dashboard():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]🧑‍💻 INTERACTIVE FORENSIC AUDIT DASHBOARD - CASO 5[/bold cyan]\n"
        "[italic deep_sky_blue]Herramienta de Auditoría y Simulación de Ataques en Cadena de Bloques[/italic deep_sky_blue]",
        border_style="cyan"
    ))
    
    # Dificultad manejable para que el PoW no se demore mucho en la simulación
    blockchain = Blockchain(difficulty=3)
    
    # Bloques iniciales para que el usuario no empiece vacio
    with console.status("[bold green]Generando historial inicial de la Blockchain...[/bold green]"):
        blockchain.add_block([
            Transaction(sender="Client_Alice", receiver="Node_Bob", amount=250.0),
        ])
        blockchain.add_block([
            Transaction(sender="DevTeam", receiver="Exchange_Binance", amount=1000.0),
        ])
        blockchain.add_block([
            Transaction(sender="Exchange_Binance", receiver="User_Charlie", amount=75.5),
        ])
    
    while True:
        console.print("\n")
        try:
            choice = questionary.select(
                "¿Qué acción deseas realizar en la Blockchain?",
                choices=[
                    "1. 📊 Visualizar Red Actual (Estado de salud)",
                    "2. ⛏️ Minar Nuevo Bloque (Transacción manual)",
                    "3. 😈 Lanzar Ataque Dirigido",
                    "4. 🔍 Ejecutar Auditoría Forense",
                    "5. 🔧 Reparar Cadena de Bloques (Demostrar PoW Cost)",
                    "6. 📜 Exportar Reporte de Transparencia (JSON)",
                    "7. 🎓 Generar API Certificado de Integridad y Salir"
                ]
            ).ask()
        except KeyboardInterrupt:
            break
            
        if not choice:
            break
            
        if choice.startswith("1"):
            console.clear()
            is_valid, _ = BlockchainAuditor.is_chain_valid(blockchain)
            display_network_state(blockchain, is_valid)
            
        elif choice.startswith("2"):
            console.clear()
            sender = questionary.text("Sender:").ask()
            receiver = questionary.text("Receiver:").ask()
            amount_str = questionary.text("Amount:").ask()
            
            try:
                amount = float(amount_str)
            except ValueError:
                console.print("[red]El monto debe ser numérico.[/red]")
                continue
                
            with console.status("[yellow]Minando bloque (Calculando PoW)...[/yellow]"):
                block = blockchain.add_block([Transaction(sender=sender, receiver=receiver, amount=amount)])
            
            console.print(f"[green]✔ Bloque #{block.index} minado correctamente con Nonce: {block.nonce}[/green]")
            display_master_concept("Proof of Work (PoW)", "Añadir un bloque requiere encontrar un 'Nonce' que, combinado con los datos del bloque, resulte en un hash con una cantidad específica de ceros iniciales. Esto hace que reescribir la historia sea computacionalmente muy costoso.")
            
        elif choice.startswith("3"):
            console.clear()
            blocks = [str(b.index) for b in blockchain.chain if b.index > 0]
            if not blocks:
                console.print("[red]No hay suficientes bloques para atacar.[/red]")
                continue
                
            block_idx_str = questionary.select("Elige el bloque a atacar:", choices=blocks).ask()
            if not block_idx_str:
                continue
            block_idx = int(block_idx_str)
            amount = questionary.text("Ingresa la cantidad falsa (monto a inyectar):").ask()
            
            try:
                hx_amount = float(amount)
            except:
                hx_amount = 99999.0
            
            console.print(f"[bold red]► Inyectando {hx_amount} en el Bloque #{block_idx}...[/bold red]")
            BlockchainAuditor.inject_malicious_data(
                blockchain,
                block_index=block_idx,
                malicious_transactions=[Transaction(sender="Atacante", receiver="WalletSecreta", amount=hx_amount)],
                sophisticated=True
            )
            console.print("[red]✔ Ataque Completado. El Hash del propio bloque fue recalculado, pero el enlace hacia delante se corrompió.[/red]")
            display_master_concept("El Efecto Dominó", "Aunque el atacante recalculó el hash del bloque secuestrado para hacerlo 'válido' individualmente, el bloque siguiente aún conserva en su memoria 'previous_hash' el valor viejo. El vínculo está roto, invalidando todo lo que le sigue.")
            is_valid, _ = BlockchainAuditor.is_chain_valid(blockchain)
            display_network_state(blockchain, is_valid=False, show_concept=False)
            
        elif choice.startswith("4"):
            console.clear()
            console.print("[bold yellow]► Iniciando Auditoría Forense Criptográfica...[/bold yellow]")
            is_valid, errors = BlockchainAuditor.is_chain_valid(blockchain)
            time.sleep(1)
            
            if is_valid:
                console.print("[bold green]✔ Ninguna alteración detectada. La cadena de bloques es inmutable.[/bold green]")
                display_network_state(blockchain, True, show_concept=False)
            else:
                for err in errors:
                    console.print(Panel(
                        f"Detalle: {err['details']}\n\n[bold magenta]Esperado (pointer):[/bold magenta] {err.get('expected_previous_hash', err.get('expected_hash'))}\n[bold yellow]Actual (calculado):[/bold yellow] {err.get('actual_previous_block_hash', err.get('actual_hash'))}",
                        title=f"🚨 [bold bright_red]VULNERABILIDAD IDENTIFICADA: {err['type']} (En Bloque #{err['block_index']})[/bold bright_red]", 
                        border_style="red"
                    ))
                display_master_concept("Detección de Intervención", "La auditoría re-calcula cada bloque y revisa los punteros previous_hash. Es matemáticamente imposible que un bloque se valide si un predecesor fue modificado.")

        elif choice.startswith("5"):
            console.clear()
            is_valid, errors = BlockchainAuditor.is_chain_valid(blockchain)
            if is_valid:
                console.print("[yellow]La cadena ya está íntegra, no hay nada que reparar.[/yellow]")
            else:
                block_idx = min([e["block_index"] for e in errors]) if errors else 1
                console.print(f"[bold yellow]► Reparando Cadena desde el Bloque #{block_idx}... (Calculando PoW para toda la bifurcación)[/bold yellow]")
                
                with console.status("[cyan]Reminando todos los bloques afectados para forzar Consenso...[/cyan]"):
                    # Reparar la secuencia desde el bloque con incosistencia de enlaces
                    blockchain.repair_chain(block_idx)
                
                console.print("[bold green]✔ Cadena sincronizada y reparada localmente.[/bold green]")
                display_master_concept("El Costo del Ataque del 51%", "Para que un atacante convenza a la red de su versión alterada, tendría que re-minar (calcular PoW) del bloque alterado y DE TODOS LOS BLOQUES POSTERIORES más rápido que el resto de la red. En criptomonedas populares, esto requiere un poder computacional insuperable.")
                display_network_state(blockchain, is_valid=True, show_concept=False)

        elif choice.startswith("6"):
            console.clear()
            is_valid, errors = BlockchainAuditor.is_chain_valid(blockchain)
            report_file = os.path.join(os.path.dirname(__file__), "transparency_report.json")
            path = BlockchainAuditor.generate_proof_of_transparency(blockchain, is_valid, errors, filename=report_file)
            console.print(f"[bold green]✔ Reporte inmutable exportado exitosamente a: {path}[/bold green]")
            display_master_concept("Proof of Transparency (PoT)", "Exportar el estado inmutable en JSON permite a oráculos, auditores externos y dashboards web (Growth Hacking) verificar la autenticidad y reportar transparencia real hacia los usuarios.")

        elif choice.startswith("7"):
            console.clear()
            is_valid, _ = BlockchainAuditor.is_chain_valid(blockchain)
            if is_valid:
                generate_certificate()
            else:
                console.print("[bold red]❌ No se puede generar un certificado con una cadena comprometida.\nDebes ejecutar una reparación (Opción 5) o auditar antes de certificar.[/bold red]")
            break

if __name__ == "__main__":
    run_dashboard()
