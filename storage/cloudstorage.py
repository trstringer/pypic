"""Handle cloud storage"""

import os
from azure.storage.blob import BlockBlobService

class CloudStorage: # pylint: disable=too-few-public-methods
    """Store files in cloud storage"""

    CONTAINER_NAME = 'pypic'

    def __init__(self, account_name, account_key):
        self.account_name = account_name
        self.account_key = account_key

    def upload_file(self, filename):
        """Upload a file to cloud storage"""

        block_blob_svc = BlockBlobService(
            account_name=self.account_name,
            account_key=self.account_key
        )
        block_blob_svc.create_container(CloudStorage.CONTAINER_NAME)
        block_blob_svc.create_blob_from_path(
            CloudStorage.CONTAINER_NAME,
            os.path.basename(filename),
            filename
        )
