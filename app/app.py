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
    parser.add_argument(
        '-s', '--stop',
        action='store_true',
        help='Run this single switch to stop other process recording'
    )
    if len(sys.argv) < 2:
        parser.print_help()
        return None
    else:
        return parser.parse_args()


def create_stop_signal():
    """Signal to other pypic processes that recording should be stopped"""

    open(os.path.expanduser('~/.pypic_stop'), 'a').close()


def remove_stop_signal():
    """Remove any possible stop signal if it exists"""

    try:
        os.remove(os.path.expanduser('~/.pypic_stop'))
    except FileNotFoundError:  # NOQA
        pass


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

    # if the user passed the stop switch then this control process is just
    # meant to signal another pypic process to stop recording and exit
    if args.stop:
        create_stop_signal()
        sys.exit(0)
    # but if this is a main recording process, we need to eliminate any
    # possibility that there is a residual stop signal file existing so that
    # we don't get a false signal from a past process
    else:
        remove_stop_signal()

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
