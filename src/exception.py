"""Exception class"""

import sys
# from src.logger import logging


def error_message_detail(error, error_detail: sys):
    """Method is for Custom error message detail"""
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured in file {file_name}, at line number {exc_tb.tb_lineno}"
    return error_message, error


class CustomException(Exception):
    """Class is for Custom exception"""

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail)
