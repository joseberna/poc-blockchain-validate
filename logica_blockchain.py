import hashlib
import time
import random
from typing import List, Dict, Any

class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()
        self.fee = round(random.uniform(0.0001, 0.005), 5)
        self.txid = self.calculate_txid()

    def calculate_txid(self) -> str:
        """Hash único de la transacción (TXID)."""
        content = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self):
        return {
            "txid": self.txid[:16],
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "fee": self.fee,
            "summary": f"{self.sender[:5]}.. ➜ {self.receiver[:5]}.."
        }

class Block:
    def __init__(self, transactions: List[Transaction], previous_hash: str, index: int, difficulty: int):
        self.index = index
        self.height = 780000 + index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.difficulty = difficulty
        self.nonce = 0
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()
        
        # Métricas Reales v10.5 (Calculadas de la data real)
        count = len(transactions)
        self.tx_count = count
        if count > 0:
            self.median_fee = round(sum(tx.fee for tx in transactions) / count, 1)
            self.size_mb = round(count * 0.25, 2) # Estimación real por TX
            self.weight_kwu = int(self.size_mb * 4000)
            self.fee_ranges = [tx.fee for tx in transactions]
            while len(self.fee_ranges) < 5: self.fee_ranges.append(random.randint(1, 10))
        else:
            self.median_fee = 0.0
            self.size_mb = 0.01
            self.weight_kwu = 40
            self.fee_ranges = [0, 0, 0, 0, 0]

    def calculate_merkle_root(self) -> str:
        """
        INGENIERÍA CRIPTOGRÁFICA: MERKLE ROOT
        El Merkle Root es el hash resumen de todas las transacciones del bloque. 
        Si una sola transacción cambia (incluso un decimal), el Merkle Root cambia radicalmente (Efecto Avalancha).
        Esto permite verificar la integridad del 'Body' sin procesar toda la data.
        """
        if not self.transactions:
            return "0" * 64
        tx_hashes = [hashlib.sha256(str(tx.to_dict()).encode()).hexdigest() for tx in self.transactions]
        return hashlib.sha256("".join(tx_hashes).encode()).hexdigest()

    def calculate_hash(self) -> str:
        """
        INGENIERÍA CRIPTOGRÁFICA: BLOCK HEADER HASH
        Representa la 'huella digital' del bloque. Vincula:
        1. Index & Timestamp: Orden Cronológico.
        2. Previous Hash: Enlace Criptográfico (Inmutabilidad).
        3. Merkle Root: Integridad del contenido de transacciones.
        4. Nonce: El factor aleatorio para el Proof of Work.
        Cualquier cambio en estos campos invalida el Hash del bloque.
        """
        header_string = f"{self.index}{self.timestamp}{self.previous_hash}{self.merkle_root}{self.nonce}"
        return hashlib.sha256(header_string.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty: int):
        """
        INGENIERÍA CRIPTOGRÁFICA: PROOF OF WORK (PoW)
        Garantiza el consenso y la dificultad de ataque. 
        El minero debe encontrar un Nonce tal que el Hash del Header comience con 'N' ceros.
        Esto consume recursos (Tiempo/CPU), haciendo que un ataque sea económicamente inviable.
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def mine_block_step(self, difficulty: int, batch_size: int = 100):
        """Versión para animación: mina en lotes y devuelve si terminó."""
        target = "0" * difficulty
        for _ in range(batch_size):
            if self.hash[:difficulty] == target:
                return True
            self.nonce += 1
            self.hash = self.calculate_hash()
        return False

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "merkle_root": self.merkle_root,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.mempool: List[Transaction] = []
        self.difficulty = difficulty
        self.status_message = ""
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_tx = [Transaction("SYSTEM", "NETWORK", 0.0)]
        genesis_block = Block(genesis_tx, "0" * 64, 0, self.difficulty)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, sender: str, receiver: str, amount: float):
        self.mempool.append(Transaction(sender, receiver, amount))

    def add_block_from_mempool(self) -> Block:
        if not self.mempool:
            return None
        latest = self.get_latest_block()
        new_block = Block(self.mempool, latest.hash, latest.index + 1, self.difficulty)
        # El minado se manejará desde la interfaz para la animación
        self.chain.append(new_block)
        self.mempool = []
        return new_block

    def add_block(self, transactions: List[Transaction]) -> Block:
        """Añade un nuevo bloque minado a la cadena."""
        previous_block = self.chain[-1]
        new_block = Block(transactions, previous_block.hash, len(self.chain), self.difficulty)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        errors = []
        is_valid = True
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Verificación de Merkle Root (Integridad de datos)
            if current.merkle_root != current.calculate_merkle_root():
                errors.append({
                    "block": current.index,
                    "type": "Merkle Root Invalido",
                    "msg": "El Merkle Root no coincide con las transacciones. Integridad comprometida."
                })
                is_valid = False

            # Verificación de Hash actual (Prueba de Trabajo)
            if current.hash != current.calculate_hash():
                errors.append({
                    "block": current.index,
                    "type": "Hash Invalido",
                    "msg": f"El Hash del Header del bloque {current.index} no es válido."
                })
                is_valid = False

            # Verificación de secuencia (Link Criptográfico)
            if current.previous_hash != previous.hash:
                errors.append({
                    "block": current.index,
                    "type": "Enlace Roto",
                    "msg": f"El bloque {current.index} apunta a un hash previo incorrecto."
                })
                is_valid = False

        return is_valid, errors

    def inject_malicious_data(self, index: int, new_amount: float):
        if index <= 0 or index >= len(self.chain): return
        target = self.chain[index]
        if target.transactions:
            target.transactions[0].amount = new_amount
            # Hack: El atacante debe recalcular el Merkle Root primero
            target.merkle_root = target.calculate_merkle_root()
            # Y el propio Hash del header
            target.hash = target.calculate_hash()

    def repair_chain(self):
        """
        Repara la cadena recalculando el PoW de cada bloque que tenga un enlace roto o hash inválido.
        Esto demuestra el costo computacional del ataque.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            # Si el enlace está roto o el hash es inválido (por ataque previo o cambio en el anterior)
            if current.previous_hash != previous.hash or current.hash != current.calculate_hash():
                current.previous_hash = previous.hash
                # IMPORTANTE: Al cambiar previous_hash, el Merkle Root se mantiene (si no se editó la tx)
                # pero el Block Hash de este bloque cambia completamente.
                current.mine_block(self.difficulty)
        return True

    def reset_chain(self):
        self.chain = []
        self.create_genesis_block()
        return True
