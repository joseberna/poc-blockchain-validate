import hashlib
import time
import logging
from typing import List, Any, Dict
from pydantic import BaseModel, Field

# Configuración del logger para seguir estándares profesionales
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BlockchainCore")

class Transaction(BaseModel):
    """
    Modelo para representar una transacción básica en la blockchain usando Pydantic.
    Garantiza la validación de tipos y estructura de los datos.
    """
    sender: str
    receiver: str
    amount: float

class BlockData(BaseModel):
    """Modelo para encapsular los datos de un bloque, permitiendo validación estructural."""
    transactions: List[Transaction] = Field(default_factory=list)

class Block:
    """Clase que representa un bloque inmutable en la blockchain."""
    
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str):
        """
        Inicializa un nuevo bloque.
        
        Args:
            index (int): Posición temporal (altura) del bloque en la cadena.
            transactions (List[Transaction]): Lista de transacciones incluidas.
            previous_hash (str): Hash criptográfico del bloque anterior para mantener la integridad en cadena.
        """
        self.index: int = index
        self.timestamp: float = time.time()
        self.data: BlockData = BlockData(transactions=transactions)
        self.previous_hash: str = previous_hash
        self.nonce: int = 0
        self.hash: str = self.calculate_hash()
        
    def calculate_hash(self) -> str:
        """
        Calcula el hash SHA-256 del bloque basado en su contenido actual.
        
        Returns:
            str: Hash criptográfico de longitud fija (SHA-256) en formato hexadecimal.
        """
        # Se normaliza la estructura del modelo Pydantic a JSON para que sea serializable y determinista
        data_json = self.data.model_dump_json()
        block_string = f"{self.index}{self.timestamp}{data_json}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """
        Realiza Prueba de Trabajo (PoW) buscando un hash que empiece con 'N' ceros.
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el bloque en un diccionario para la serialización del reporte de auditoría."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data.model_dump(),
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

class Blockchain:
    """Gestor principal de la estructura de datos distribuida (Blockchain)."""
    
    def __init__(self, difficulty: int = 2):
        """Inicializa la blockchain creando el bloque génesis por defecto."""
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.create_genesis_block()
        logger.info("Sistema Blockchain inicializado. Bloque génesis anclado.")
        
    def create_genesis_block(self) -> None:
        """Crea y encola el primer bloque (génesis) de la historia de la cadena."""
        genesis_transactions = [Transaction(sender="0x00_ROOT", receiver="0x00_SYS", amount=0.0)]
        genesis_block = Block(0, genesis_transactions, "0" * 64)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        
    def get_latest_block(self) -> Block:
        """Obtiene el último bloque asegurado en la red."""
        return self.chain[-1]
        
    def add_block(self, transactions: List[Transaction]) -> Block:
        """
        Añade un nuevo bloque asegurado criptográficamente a la cadena.
        
        Args:
            transactions (List[Transaction]): Lista de nuevas transacciones a registrar y minar.
            
        Returns:
            Block: La instancia del nuevo bloque generado y asegurado.
        """
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            transactions=transactions,
            previous_hash=previous_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        logger.info(f"Bloque #{new_block.index} minado/añadido correctamente. Hash: {new_block.hash[:12]}...")
        return new_block
    
    def repair_chain(self, start_index: int) -> None:
        """
        Repara la cadena recalculando el PoW de cada bloque comprometido y arreglando los enlaces rotos.
        """
        for i in range(start_index, len(self.chain)):
            block = self.chain[i]
            if i > 0:
                block.previous_hash = self.chain[i - 1].hash
            block.mine_block(self.difficulty)
            logger.info(f"Bloque #{block.index} re-minado con éxito. Nuevo Hash: {block.hash[:12]}...")
