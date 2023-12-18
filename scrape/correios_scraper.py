from urllib.parse import urlencode
from factories.captcha import CaptchaAudioSeleniumFactory

URL_MAIN = "https://rastreamento.correios.com.br/app/index.php"

class CorreiosScraper:
    def __init__(self) -> None:
        self._url = None

    def url(self, captcha: str, code: str = "QP487749745BR") -> str:
        payload = {
           "objeto": f"{code}",
           "captcha": f"{captcha}",
           "mqs": "S"
        }
        return f"{URL_MAIN}?{urlencode(payload)}"

    def execute(self) -> None:
        captcha_factory = CaptchaAudioSeleniumFactory()
        captcha_factory.solve()