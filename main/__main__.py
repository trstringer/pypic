"""Do work"""

import os
from cameracontroller.cameracontroller import CameraController
from storage.cloudstorage import CloudStorage

def main():
    """Main script execution"""

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
