
class Response:

    def __init__(self, status_code:str, html:str, error: str):
        self.status_code = status_code
        self.html = html
        self.error = error

    def isResponseOK(self):
        if not self.error:
            return True
        else:
            return False