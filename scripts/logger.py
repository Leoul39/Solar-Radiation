import os
import logging

def setup_logger():
    '''
    This function is used to setup logger for logging Error and Info to the logs directory.

    Returns:
    -----------
        a `logger` instance
    '''

    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(main_dir, 'log') 

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    log_file_info = os.path.join(log_dir, 'Info.log')
    log_file_error = os.path.join(log_dir, 'Error.log')

    info_handler = logging.FileHandler(log_file_info)
    error_handler = logging.FileHandler(log_file_error)
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s',
                                    datefmt= '%Y-%m-%d %H:%M')

    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    info_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    console_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(__name__)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    
    return logger

log=setup_logger()
