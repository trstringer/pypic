"""Handle the camera"""

from datetime import datetime
from multiprocessing import Pool
import logging
import os
import time
from picamera import PiCamera  # pylint: disable=import-error
from data import insert_upload_data


class CameraController:  # pylint: disable=too-few-public-methods
    """Camera operations"""

    def __init__(self, local_path, cloud_storage):
        self.local_path = local_path
        self.cloud_storage = cloud_storage
        self.camera = PiCamera()

    def record_video(self, continuous=False, duration=10):
        """Record a video either once or continuously"""

        pool = Pool()

        while True:
            local_filename = self.__filename_generator()
            self.camera.start_recording(local_filename)
            time.sleep(duration)
            self.camera.stop_recording()
            logging.debug('testing for cloud storage if defined')
            if self.cloud_storage:
                logging.debug('cloud storage is defined')
                pool.apply_async(
                    self.cloud_storage.upload_file,
                    (local_filename,),
                    callback=self.__upload_callback
                )
            if not continuous or self.__stop_signal():
                pool.close()
                pool.join()
                break

    # pylint: disable=no-self-use
    def __stop_signal(self):
        if os.path.exists(os.path.expanduser('~/.pypic_stop')):
            os.remove('~/.pypic_stop')
            return True
        else:
            return False

    # pylint: disable=no-self-use
    def __upload_callback(self, output):
        logging.debug('in upload callback')
        other_info = str(output['error']) if 'error' in output.keys() else ''
        insert_upload_data(
            output['filename'],
            output['date_created'],
            output['is_uploaded'],
            other_info
        )

    def __filename_generator(self):
        return os.path.join(
            self.local_path,
            '{}.h264'.format(datetime.utcnow().strftime('%Y_%m_%d_%H:%M:%S.%f'))
        )
