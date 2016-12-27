"""Do work"""

import argparse
import logging
import os
import sys
from cameracontroller import CameraController
from storage import CloudStorage
from data import create_upload_table


def setup_logger():
    """Create the log directory if
    it doesn't exist and setup the
    logging configuration
    """

    logger = logging.getLogger('pypic')
    log_dir = os.path.expanduser('~/log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        filename=os.path.join(log_dir, 'pypiclog'),
        format='%(asctime)s :: %(levelname)s :: %(message)s',
        level=logging.DEBUG
    )
    return logger


def parse_args():
    """Parse and return passed arguments to the app"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--continuous',
        action='store_true',
        help='If set, run the video feed continuously'
    )
    parser.add_argument(
        '-d', '--duration',
        default=10,
        type=float,
        help='Duration (in seconds) to run the video loop'
    )
    parser.add_argument(
        '-o', '--outputdir',
        help='Local directory to store video files'
    )
    parser.add_argument(
        '-t', '--containername',
        help='Cloud storage container name (default \'pypic\')'
    )
    if len(sys.argv) < 2:
        parser.print_help()
        return None
    else:
        return parser.parse_args()


# pylint: disable=unused-argument
def exception_handler(exception_type, exception, traceback):
    """This is the logging handler that
    will log uncaught exceptions. This
    is important for running unattended
    """

    logging.error(str(exception))


def main():
    """Main script execution"""

    logger = setup_logger()
    sys.excepthook = exception_handler

    args = parse_args()

    # if no args were passed, the help menu was printed and we need to exit
    if not args:
        sys.exit(0)

    if not args.outputdir:
        error_msg = 'You must specify an output directory (-o, --outputdir)'
        logger.error(error_msg)
        print(error_msg)
        sys.exit(1)

    create_upload_table()

    cloud_storage_account_name = os.environ.get('AZSTORAGE_ACCOUNT_NAME')
    cloud_storage_account_key = os.environ.get('AZSTORAGE_ACCOUNT_KEY')
    cloud_storage = None
    if cloud_storage_account_name and cloud_storage_account_key:
        cloud_storage = CloudStorage(
            cloud_storage_account_name,
            cloud_storage_account_key,
            args.containername or 'pypic'
        )

    camera_controller = CameraController(
        os.path.expanduser(args.outputdir),
        cloud_storage
    )
    camera_controller.record_video(
        continuous=args.continuous,
        duration=args.duration
    )

if __name__ == '__main__':
    main()
