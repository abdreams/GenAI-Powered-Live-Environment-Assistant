"""
Database Manager - Handles all database connections and queries
Manages connection pooling, transactions, and query execution
"""
import logging
import time
from typing import Dict, List, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations"""
    
    MAX_CONNECTIONS = 10
    CONNECTION_TIMEOUT = 30
    LOCK_TIMEOUT = 10
    
    def __init__(self):
        self.connection_pool = []
        self.active_connections = 0
        logger.info("DatabaseManager initialized with max connections: {self.MAX_CONNECTIONS}")
    
    @contextmanager
    def get_connection(self):
        """Get a database connection from the pool"""
        start_time = time.time()
        
        # Wait for available connection
        while self.active_connections >= self.MAX_CONNECTIONS:
            if time.time() - start_time > self.CONNECTION_TIMEOUT:
                logger.error("Connection pool exhausted - timeout waiting for connection")
                raise Exception("Connection pool exhausted")
            time.sleep(0.1)
        
        self.active_connections += 1
        logger.debug(f"Connection acquired. Active connections: {self.active_connections}")
        
        try:
            # Simulate connection object
            conn = {"id": self.active_connections, "timestamp": time.time()}
            yield conn
        finally:
            self.active_connections -= 1
            logger.debug(f"Connection released. Active connections: {self.active_connections}")
    
    def get_account_balance(self, account_number: str) -> float:
        """Get the current balance for an account"""
        logger.debug(f"Fetching balance for account {account_number}")
        
        with self.get_connection() as conn:
            # Simulate query
            query = f"SELECT balance FROM accounts WHERE account_number = '{account_number}' FOR UPDATE"
            logger.debug(f"Executing query: {query}")
            
            # Simulate some processing time
            time.sleep(0.01)
            
            # Return dummy balance
            return 50000.0
    
    def update_account_balance(self, account_number: str, new_balance: float) -> bool:
        """Update account balance"""
        logger.debug(f"Updating balance for account {account_number} to {new_balance}")
        
        with self.get_connection() as conn:
            # Simulate query with row locking
            query = f"UPDATE accounts SET balance = {new_balance} WHERE account_number = '{account_number}'"
            logger.debug(f"Executing query: {query}")
            
            # Simulate some processing time
            time.sleep(0.01)
            
            return True
    
    def execute_transaction(self, queries: List[str], isolation_level: str = "READ_COMMITTED") -> bool:
        """
        Execute multiple queries in a transaction
        
        Args:
            queries: List of SQL queries to execute
            isolation_level: Transaction isolation level
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Starting transaction with {len(queries)} queries, isolation={isolation_level}")
        
        with self.get_connection() as conn:
            try:
                # Begin transaction
                logger.debug("BEGIN TRANSACTION")
                
                for i, query in enumerate(queries):
                    logger.debug(f"Executing query {i+1}/{len(queries)}: {query[:100]}...")
                    
                    # Simulate lock acquisition
                    lock_start = time.time()
                    acquired = self._acquire_lock(query, timeout=self.LOCK_TIMEOUT)
                    
                    if not acquired:
                        elapsed = time.time() - lock_start
                        logger.error(f"Lock timeout after {elapsed:.2f}s for query: {query[:100]}")
                        raise Exception(f"Lock acquisition timeout on query {i+1}")
                    
                    # Simulate query execution
                    time.sleep(0.01)
                    
                    # Release lock
                    self._release_lock(query)
                
                # Commit transaction
                logger.debug("COMMIT TRANSACTION")
                logger.info("Transaction completed successfully")
                return True
                
            except Exception as e:
                logger.error(f"Transaction failed: {str(e)}", exc_info=True)
                logger.debug("ROLLBACK TRANSACTION")
                raise
    
    def _acquire_lock(self, query: str, timeout: int) -> bool:
        """Simulate lock acquisition with potential deadlock"""
        # Simulate lock contention
        if "UPDATE accounts" in query:
            # 20% chance of lock timeout
            import random
            if random.random() < 0.2:
                time.sleep(timeout + 0.1)
                return False
        return True
    
    def _release_lock(self, query: str):
        """Release acquired locks"""
        logger.debug("Lock released")
    
    def get_payment_by_id(self, payment_id: str) -> Optional[Dict]:
        """Retrieve payment details by ID"""
        logger.debug(f"Fetching payment details for {payment_id}")
        
        with self.get_connection() as conn:
            query = f"SELECT * FROM payments WHERE payment_id = '{payment_id}'"
            logger.debug(f"Executing query: {query}")
            
            # Return dummy payment data
            return {
                "payment_id": payment_id,
                "status": "SUCCESS",
                "amount": 1000.0,
                "account_from": "ACC001",
                "account_to": "ACC002"
            }
    
    def log_transaction(self, payment_id: str, status: str, details: Dict) -> bool:
        """Log transaction to audit table"""
        logger.debug(f"Logging transaction {payment_id} with status {status}")
        
        with self.get_connection() as conn:
            query = f"""
            INSERT INTO transaction_log (payment_id, status, timestamp, details)
            VALUES ('{payment_id}', '{status}', NOW(), '{str(details)}')
            """
            logger.debug(f"Executing query: {query[:100]}...")
            
            return True
