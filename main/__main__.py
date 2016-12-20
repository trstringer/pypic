"""Do work"""

import logging
import os
import sys
from cameracontroller.cameracontroller import CameraController
from storage.cloudstorage import CloudStorage

logger = logging.getLogger('pypic')
log_dir = os.path.expanduser('~/log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, 'pypiclog'),
    format='%(asctime)s :: %(levelname)s :: %(message)s',
    level=logging.DEBUG
)

def exception_handler(exception_type, exception, traceback):
    logger.exception(str(exception))

sys.excepthook = exception_handler

def main():
    """Main script execution"""

    logger.debug('Starting main() execution...')

    camera_controller = CameraController(
        os.path.expanduser('~/pypic_output'),
        CloudStorage(
            os.environ.get('AZSTORAGE_ACCOUNT_NAME'),
            os.environ.get('AZSTORAGE_ACCOUNT_KEY')
        )
    )
    camera_controller.record_video(continuous=True)

if __name__ == '__main__':
    main()
