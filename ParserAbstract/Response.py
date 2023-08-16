
class Response:

    def __init__(self, status_code:str, html:str, error: str):
        self.status_code = status_code
        self.html = html
        self.error = error

    def is_response_ok(self):
        if not self.error:
            return True
        else:
            return False


    def __str__(self):
        HTML_LEN = 50


        if not self.html or len(self.html) == 0:
            html = ""
        else:
            if len(self.html) > HTML_LEN:
                html = self.html[:HTML_LEN]
            else:
                html = self.html
        return f"Response: [{self.status_code=}][{html=}] [{self.error=}]"


def test():
    res = Response('403', "Hello my friend, Hello my friend, Hello my friend, Hello my friend, Hello my friend, ", "Error")

    print(res)

    print(f'{res.is_response_ok()=}')

    res = Response('200', "Hello my friend, Hello my friend, Hello my friend, Hello my friend, Hello my friend, ", None)

    print(res)

    print(f'{res.is_response_ok()=}')

if __name__ == '__main__':
    test()