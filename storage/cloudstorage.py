"""Handle cloud storage"""

import os
from azure.storage.blob import BlockBlobService

class CloudStorage: # pylint: disable=too-few-public-methods
    """Store files in cloud storage"""

    def __init__(self, account_name, account_key, container_name):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name

    def upload_file(self, filename):
        """Upload a file to cloud storage"""

        block_blob_svc = BlockBlobService(
            account_name=self.account_name,
            account_key=self.account_key
        )
        block_blob_svc.create_container(self.container_name)
        block_blob_svc.create_blob_from_path(
            self.container_name,
            os.path.basename(filename),
            filename
        )
