"""API to save a file locally"""

import shutil

class LocalStorage: # pylint: disable=too-few-public-methods
    """Store files locally"""

    def __init__(self, destination_directory):
        self.destination_directory = destination_directory

    def save_file(self, source_file):
        """Save a file to the
        determined destination directory to
        act as the local cache
        """

        shutil.copy2(source_file, self.destination_directory)
