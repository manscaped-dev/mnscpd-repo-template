"""This is the custom error module for consistent and pertinent messaging.

# Author: @philipdelorenzo-manscaped<phil.delorenzo@manscaped.com>
"""

class GenericError(Exception):
    def __init__(self):
        # Call the base class constructor with the parameters it needs
        self.message = f"[ERROR] - A specific error message here."
        print(self.message)
        exit(1)
