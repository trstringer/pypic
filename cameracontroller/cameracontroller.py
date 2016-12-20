"""Handle the camera"""

from datetime import datetime
import os
import time
from picamera import PiCamera

class CameraController: # pylint: disable=too-few-public-methods
    """Camera operations"""

    def __init__(self, local_path, cloud_storage):
        self.local_path = local_path
        self.cloud_storage = cloud_storage
        self.camera = PiCamera()

    def record_video(self, continuous=False, duration=10):
        """Record a video either once or continuously"""

        while True:
            local_filename = self.__filename_generator()
            self.camera.start_recording(local_filename)
            time.sleep(duration)
            self.camera.stop_recording()
            if self.cloud_storage:
                self.cloud_storage.upload_file(local_filename)
            if not continuous:
                break

    def __filename_generator(self):
        return os.path.join(
            self.local_path,
            '{}.h264'.format(datetime.utcnow().strftime('%Y_%m_%d_%H:%M:%S.%f'))
        )
