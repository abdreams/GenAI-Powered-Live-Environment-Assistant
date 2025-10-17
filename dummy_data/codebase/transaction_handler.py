"""
Transaction Handler - Handles financial transaction logic
Manages atomic money transfers with proper rollback support
"""
import logging
from datetime import datetime
from typing import Dict
from database_manager import DatabaseManager

logger = logging.getLogger(__name__)


class TransactionHandler:
    """Handles financial transactions between accounts"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        logger.info("TransactionHandler initialized")
    
    def execute_transfer(self, payment_id: str, account_from: str, 
                        account_to: str, amount: float) -> Dict:
        """
        Execute a money transfer between two accounts atomically
        
        Args:
            payment_id: Unique payment identifier
            account_from: Source account
            account_to: Destination account
            amount: Transfer amount
            
        Returns:
            Dict with transaction result
        """
        logger.info(f"Executing transfer {payment_id}: ${amount} from {account_from} to {account_to}")
        
        try:
            # Get current balances
            balance_from = self.db_manager.get_account_balance(account_from)
            balance_to = self.db_manager.get_account_balance(account_to)
            
            logger.debug(f"Current balances - From: ${balance_from}, To: ${balance_to}")
            
            # Calculate new balances
            new_balance_from = balance_from - amount
            new_balance_to = balance_to + amount
            
            # Prepare transaction queries
            queries = [
                f"UPDATE accounts SET balance = {new_balance_from}, last_updated = NOW() WHERE account_number = '{account_from}'",
                f"UPDATE accounts SET balance = {new_balance_to}, last_updated = NOW() WHERE account_number = '{account_to}'",
                f"INSERT INTO payments (payment_id, account_from, account_to, amount, status, timestamp) VALUES ('{payment_id}', '{account_from}', '{account_to}', {amount}, 'SUCCESS', NOW())"
            ]
            
            # Execute transaction
            self.db_manager.execute_transaction(queries, isolation_level="SERIALIZABLE")
            
            # Log successful transaction
            self.db_manager.log_transaction(payment_id, "SUCCESS", {
                "account_from": account_from,
                "account_to": account_to,
                "amount": amount,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"Transfer {payment_id} completed successfully")
            
            return {
                "status": "SUCCESS",
                "payment_id": payment_id,
                "amount": amount,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Transfer {payment_id} failed: {str(e)}", exc_info=True)
            
            # Log failed transaction
            try:
                self.db_manager.log_transaction(payment_id, "FAILED", {
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
            except:
                logger.error("Failed to log transaction failure")
            
            return {
                "status": "FAILED",
                "payment_id": payment_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def verify_transaction(self, payment_id: str) -> bool:
        """Verify that a transaction was completed correctly"""
        logger.info(f"Verifying transaction {payment_id}")
        
        try:
            payment = self.db_manager.get_payment_by_id(payment_id)
            
            if not payment:
                logger.warning(f"Payment {payment_id} not found")
                return False
            
            if payment["status"] != "SUCCESS":
                logger.warning(f"Payment {payment_id} status is {payment['status']}")
                return False
            
            # Verify balances are correct
            balance_from = self.db_manager.get_account_balance(payment["account_from"])
            balance_to = self.db_manager.get_account_balance(payment["account_to"])
            
            logger.debug(f"Verified balances - From: ${balance_from}, To: ${balance_to}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error verifying transaction {payment_id}: {str(e)}")
            return False
    
    def handle_failed_transaction(self, payment_id: str, error: str):
        """Handle cleanup for failed transactions"""
        logger.warning(f"Handling failed transaction {payment_id}: {error}")
        
        try:
            # Update payment status
            self.db_manager.log_transaction(payment_id, "FAILED", {
                "error": error,
                "handled_at": datetime.now().isoformat()
            })
            
            # Send alert to monitoring system
            self._send_alert(payment_id, error)
            
        except Exception as e:
            logger.error(f"Error handling failed transaction: {str(e)}")
    
    def _send_alert(self, payment_id: str, error: str):
        """Send alert for failed transaction"""
        logger.warning(f"ALERT: Transaction {payment_id} failed - {error}")
