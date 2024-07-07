from django.db import transaction
from .repositories import ProductRepository, ProductImageRepository

class UnitOfWork:
    """
    Unit of Work class managing transactions.

    This class uses Django's transaction.atomic() to ensure that all operations within a context are part of a single database transaction.
    """
    def __init__(self):
        # Initializing repositories
        self.product_repository = ProductRepository()
        self.product_image_repository = ProductImageRepository()

    def __enter__(self):
        # Entering a transaction block
        self.txn = transaction.atomic()  # Creating a transaction context manager
        self.txn.__enter__()  # Manually enter the transaction
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Exiting the transaction block, managing exceptions
        if exc_type:
            # If an exception occurred, the transaction will be rolled back
            self.txn.__exit__(exc_type, exc_val, exc_tb)
            return False  # Propagate the exception
        else:
            # No exceptions, commit the transaction
            self.txn.__exit__(None, None, None)
            return True  # End transaction management

    # Commit and rollback methods can be provided for manual control, but aren't necessary with the above setup
    def commit(self):
        """
        Manual commit: Not needed in typical usage since __exit__ handles transaction end.
        """
        pass

    def rollback(self):
        """
        Manual rollback: To manually rollback, raise an exception within the transaction block.
        """
        pass
