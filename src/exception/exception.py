import sys
import os

class CustomException(Exception):
    def __init__(self, error,error_details:sys):
        _,_,exc_tb=error_details.exc_info()
        self.filename=exc_tb.tb_frame.f_code.co_filename
        self.lineno=exc_tb.tb_lineno
        self.error_message="Error occured in python scrypt [{0}] on line no. [{1}] error message [{2}]".format(
            self.filename,
            self.lineno,
            error
        )
    def __str__(self):
        return self.error_message

if __name__=='__main__':
    try:
        a=1/0
    except Exception as e:
        raise CustomException(e,sys)

