import logging
import json
from typing import List, Tuple, Any, Dict
from core import Blockchain, Transaction, BlockData

logger = logging.getLogger("BlockchainSecurity")

class BlockchainAuditor:
    """Motor analítico especializado en auditoría criptográfica interactiva y seguridad de inmutabilidad."""
    
    @staticmethod
    def is_chain_valid(blockchain: Blockchain) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Audita la inmutabilidad de la cadena, comprobando firmas (hashes) 
        y la consistencia secuencial de los enlaces entre bloques (previous_hash).
        
        Args:
            blockchain (Blockchain): La instancia de red blockchain local a verificar.
            
        Returns:
            Tuple[bool, List[Dict[str, Any]]]: Flag booleano del estado global (True si es válida), 
                                               y una lista descriptiva de cada incidente detectado.
        """
        errors = []
        is_valid = True
        
        for i in range(1, len(blockchain.chain)):
            current_block = blockchain.chain[i]
            previous_block = blockchain.chain[i - 1]
            
            # Verificación #1: Integridad interna del contenido del propio bloque
            calculated_hash = current_block.calculate_hash()
            if current_block.hash != calculated_hash:
                logger.error(f"¡BRECHA DE INTEGRIDAD! Contenido modificado detectado en Bloque #{current_block.index}.")
                logger.debug(f"  > Hash registrado: {current_block.hash}")
                logger.debug(f"  > Hash matemáticamente real: {calculated_hash}")
                errors.append({
                    "block_index": current_block.index,
                    "type": "invalid_content_hash",
                    "details": "El contenido (transacciones/tiempo) del bloque fue modificado post-minado.",
                    "expected_hash": current_block.hash,
                    "actual_hash": calculated_hash
                })
                is_valid = False
                
            # Verificación #2: Continuidad e inmutabilidad de la cadena cronológica (El verdadero eslabón)
            if current_block.previous_hash != previous_block.hash:
                logger.error(f"¡ENLACE DE CADENA ROTO! Ruptura de secuencia detectada en Bloque #{current_block.index}.")
                logger.debug(f"  > previous_hash apunta a: {current_block.previous_hash}")
                logger.debug(f"  > Posible mutación: El hash actual del Bloque #{previous_block.index} es {previous_block.hash}")
                errors.append({
                    "block_index": current_block.index,
                    "type": "broken_chain_link",
                    "details": "El bloque anterior fue manipulado (cambiando su firma), invalidando el eslabón.",
                    "expected_previous_hash": current_block.previous_hash,
                    "actual_previous_block_hash": previous_block.hash
                })
                is_valid = False
                
        if is_valid:
            logger.info("Auditoría Continua: RED SEGURA. Cohesión e Inmutabilidad al 100%.")
        else:
            logger.critical("Auditoría Continua: ¡REGLAS DE CONSENSO QUEBRANTADAS! Manipulación en curso identificada.")
            
        return is_valid, errors

    @staticmethod
    def inject_malicious_data(blockchain: Blockchain, block_index: int, malicious_transactions: List[Transaction], sophisticated: bool = False) -> None:
        """
        Simulador de Vector de Ataque: Secuestra y reescribe data sin validación de consenso.
        
        Args:
            blockchain (Blockchain): Objeto central blockchain en entorno controlado.
            block_index (int): El índice del bloque en el pasado objetivo del ataque.
            malicious_transactions (List[Transaction]): La carga/payload que reemplazará transacciones legítimas.
            sophisticated (bool): Modifica su funcionamiento. Si es False = rompe el hash del bloque.
                                  Si es True = recalcula el hash del bloque, logrando ocultar el cambio local,
                                  pero rompiendo ineludiblemente el `previous_hash` del bloque siguiente.
        """
        if block_index >= len(blockchain.chain) or block_index <= 0:
            logger.error("Ataque abortado: Índice de bloque fuera de límites o es el bloque inmutable génesis.")
            return

        target_block = blockchain.chain[block_index]
        logger.warning(f"INICIANDO ATAQUE ZERO-DAY: INFILTRACIÓN EN BLOQUE #{block_index}...")
        
        # Secuestro activo y sobrescritura de data de la cadena (Sin consenso P2P)
        target_block.data = BlockData(transactions=malicious_transactions)
        
        if sophisticated:
            logger.warning("Atacante refinado: Recalculando el propio hash del bloque para burlar un control básico de redundancia temporal.")
            target_block.hash = target_block.calculate_hash()
        else:
            logger.warning("Atacante estándar: Inyectando datos raw (dejando hash incongruente).")
            
        logger.critical(f"Ataque Completado. Transacciones del Bloque #{block_index} fueron sustituidas con éxito.")

    @staticmethod
    def generate_proof_of_transparency(blockchain: Blockchain, is_valid: bool, errors: List[Dict[str, Any]], filename: str = "transparency_report.json") -> str:
        """
        Genera el Snapshot en JSON para ser servido por una API - Metodología Proof of Transparency (PoT).
        Útil en Growth/Marketing de la plataforma Web3 como evidencia pública.
        
        Args:
            blockchain (Blockchain): La instancia de blockchain fuente de verdad.
            is_valid (bool): Estado global de seguridad tras la última auditoría.
            errors (List): Incidentes de violaciones capturados.
            filename (str): Nombre del endpoint o fichero de exposición.
            
        Returns:
            str: Ruta del fichero JSON exportado.
        """
        report = {
            "audit_meta": {
                "blockchain_network_status": "🟢 SECURE" if is_valid else "🔴 COMPROMISED",
                "total_blocks_audited": len(blockchain.chain),
                "incident_count": len(errors)
            },
            "incidents": errors,
            "public_ledger": [block.to_dict() for block in blockchain.chain]
        }
        
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
            
        logger.info(f"API Endpoint (PoT) exportado exitosamente en: {filename}")
        return filename
