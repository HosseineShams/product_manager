from django.db import transaction
from .repositories import ProductRepository, ProductImageRepository

class UnitOfWork:
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
            return False
        else:
            self.txn.__exit__(None, None, None)
            return True

    def commit(self):
        transaction.savepoint_commit(self.txn.savepoint_id)

    def rollback(self):
        transaction.savepoint_rollback(self.txn.savepoint_id)
