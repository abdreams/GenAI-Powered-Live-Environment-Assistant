"""
Payment Service - Core payment processing logic
Handles payment transactions, validations, and orchestration
"""
import logging
from datetime import datetime
from typing import Dict, Optional
from database_manager import DatabaseManager
from transaction_handler import TransactionHandler

logger = logging.getLogger(__name__)


class PaymentService:
    """Main service for processing payments"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.transaction_handler = TransactionHandler()
        logger.info("PaymentService initialized")
    
    def process_payment(self, payment_id: str, account_from: str, 
                       account_to: str, amount: float) -> Dict:
        """
        Process a payment transaction between two accounts
        
        Args:
            payment_id: Unique payment identifier
            account_from: Source account number
            account_to: Destination account number
            amount: Payment amount
            
        Returns:
            Dict with payment status and details
        """
        logger.info(f"Processing payment {payment_id}: ${amount} from {account_from} to {account_to}")
        
        try:
            # Validate payment
            if not self._validate_payment(account_from, account_to, amount):
                logger.error(f"Payment validation failed for {payment_id}")
                return {"status": "FAILED", "reason": "Validation failed"}
            
            # Check account balance
            balance = self.db_manager.get_account_balance(account_from)
            if balance < amount:
                logger.warning(f"Insufficient funds for payment {payment_id}")
                return {"status": "FAILED", "reason": "Insufficient funds"}
            
            # Process the transaction
            result = self.transaction_handler.execute_transfer(
                payment_id, account_from, account_to, amount
            )
            
            if result["status"] == "SUCCESS":
                logger.info(f"Payment {payment_id} completed successfully")
                self._send_notification(account_from, account_to, amount)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing payment {payment_id}: {str(e)}", exc_info=True)
            return {"status": "ERROR", "reason": str(e)}
    
    def _validate_payment(self, account_from: str, account_to: str, 
                         amount: float) -> bool:
        """Validate payment parameters"""
        if not account_from or not account_to:
            return False
        if amount <= 0 or amount > 1000000:  # Max 1M per transaction
            return False
        if account_from == account_to:
            return False
        return True
    
    def _send_notification(self, account_from: str, account_to: str, amount: float):
        """Send notification about successful payment"""
        logger.info(f"Notification sent for transfer ${amount} from {account_from} to {account_to}")
    
    def get_payment_status(self, payment_id: str) -> Optional[Dict]:
        """Get the status of a payment"""
        try:
            return self.db_manager.get_payment_by_id(payment_id)
        except Exception as e:
            logger.error(f"Error fetching payment status for {payment_id}: {str(e)}")
            return None
    
    def refund_payment(self, payment_id: str) -> Dict:
        """Refund a completed payment"""
        logger.info(f"Processing refund for payment {payment_id}")
        
        try:
            payment = self.get_payment_status(payment_id)
            if not payment:
                return {"status": "FAILED", "reason": "Payment not found"}
            
            if payment["status"] != "SUCCESS":
                return {"status": "FAILED", "reason": "Cannot refund unsuccessful payment"}
            
            # Reverse the transaction
            result = self.transaction_handler.execute_transfer(
                f"REFUND_{payment_id}",
                payment["account_to"],
                payment["account_from"],
                payment["amount"]
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing refund for {payment_id}: {str(e)}", exc_info=True)
            return {"status": "ERROR", "reason": str(e)}
