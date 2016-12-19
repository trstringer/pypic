"""Do work"""

import os
from cameracontroller.cameracontroller import CameraController
from storage.cloudstorage import CloudStorage
from storage.localstorage import LocalStorage

def main():
    """Main script execution"""

    camera_controller = CameraController(
        LocalStorage('/home/pi/Desktop'),
        CloudStorage(
            os.environ.get('AZSTORAGE_ACCOUNT_NAME'),
            os.environ.get('AZSTORAGE_ACCOUNT_KEY')
        )
    )
    camera_controller.record_video(continuous=True)

if __name__ == '__main__':
    main()
