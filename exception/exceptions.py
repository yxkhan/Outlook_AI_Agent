import os
import sys

class OutlookAgentException(Exception):
    """
    Custom Exception class for the Outlook AI Agent  project.
    Provides detailed error information including the file name and line number.
    """

    def __init__(self, error_message, error_details: sys):
        """
        Initializes the exception with error message and traceback details.

        Parameters:
        - error_message (str): The 'e' original exception message.
        - error_details: The 'sys' module passed so we can use sys.exc_info() 
                         to get file name and line number where the error occurred."""
        
        self.error_message = error_message  ## Save the original error message
        
        # Extract traceback info which gives tuple of (type, value, traceback object)
        # We are only interested in the traceback object for line number and file name
        _, _, exc_tb = error_details.exc_info()
        
        # Get the line number where the exception occurred
        self.lineno = exc_tb.tb_lineno
        
        # Get the file name where the exception occurred
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):   #Overrides the default string representation (str(obj)) of the exception.S
        """
        Return a string representation of the error, including file name, line number, and message.
        """
        return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )

        
        
# Entry point of the script
if __name__ == '__main__':
    try:
        # This will raise a ZeroDivisionError intentionally
        a = 1 / 0
        print("This will not be printed", a)
    except Exception as e:
        # Catch the error and raise a custom exception with more context
        # Passing both the error object and sys module
        raise OutlookAgentException(e, sys)