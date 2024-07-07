from django.db import transaction
from .repositories import ProductRepository, ProductImageRepository

class UnitOfWork:
    """
    Unit of Work class managing transactions.
    
    Ensures all operations within a context are part of a single database transaction.
    """
    def __init__(self):
        self.product_repository = ProductRepository()
        self.product_image_repository = ProductImageRepository()

    def __enter__(self):
        self.txn = transaction.atomic()
        self.txn.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.txn.__exit__(exc_type, exc_val, exc_tb)
            return False  # Propagate the exception if any
        else:
            self.txn.__exit__(None, None, None)
            return True  # Successfully commit the transaction if no exceptions

    def commit(self):
        """
        Commit is handled by __exit__, so manual commits are generally unnecessary.
        """
        pass

    def rollback(self):
        """
        To rollback, an exception should be raised to trigger __exit__ with error handling.
        """
        pass
