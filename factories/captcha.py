import time
from os import remove

import requests
from requests import Session
from typing import Optional, List
from pathlib import Path

import speech_recognition as sr
from selectolax.parser import HTMLParser
from selenium.webdriver.common.by import By

from error import CaptchaError
from .selenium_factories import WebDriverChromeFactory


MAX_RETRIES = 5

class CaptchaAudioSeleniumFactory:
    def __init__(self) -> None:
        self.session = None
    
    def _get_audio_bytes(self, cookies: List[dict], url_audio: str) -> bytes:
        try:
            self.session = Session()
            for cookie in cookies:
                self.session.cookies.set(cookie['name'], cookie['value'])
                    
            r = self.session.get(url_audio)
            self.session.close()
            return r.content
        except:
            raise CaptchaError("Captcha audio not retrieved")
            
    def _is_captcha_page(self, parser: HTMLParser) -> bool:
        captcha_button = 'a[href="captchaAudio.svl"]'
        return parser.css_matches(captcha_button)

    def _recognize_audio(self, audio_data: bytes) -> str:
        """
        Use an audio recognition library to convert the audio to text.
        """
       
        audio_path = Path("./tmp/")
        audio_path.mkdir(parents=True, exist_ok=True)

        with open( audio_path / "audio_file.wav", "wb") as file:
            file.write(audio_data)
            
        # Use speech recognition to convert audio to text
        recognizer = sr.Recognizer()
        
        try:
            audio_retries = 0
            while audio_retries < MAX_RETRIES:
                with sr.AudioFile(f"{audio_path}/audio_file.wav") as source:
                    audio = recognizer.listen(source)
                    captcha_text = recognizer.recognize_google(audio, language="pt-BR")
                    if captcha_text.isnumeric():
                        return captcha_text.lower()
                    audio_retries += 1
        except sr.UnknownValueError:
            raise Exception("Google Speech Recognition could not understand audio.")
        except sr.RequestError:
            raise Exception("Could not request results from Google Speech Recognition service.")
        except:
            raise CaptchaError("Captcha audio not solved")

    def solve(self, url_main: str, url_audio: str) -> HTMLParser:
        print("Solving CAPTCHA...")
        retries = 0
        while retries <= MAX_RETRIES:
            with WebDriverChromeFactory().get_driver() as browser:
                browser.get(url_main)
                html_content = browser.page_source
                parser = HTMLParser(html_content)
                
                if self._is_captcha_page(parser):
                    try:
                        cookies = browser.get_cookies()
                        audio = self._get_audio_bytes(cookies, url_audio)
                        captcha_text = self._recognize_audio(audio)

                        captcha_input = browser.find_element(
                            By.ID, 
                            "captcha_text"
                        )
                        captcha_input.send_keys(captcha_text)

                        time.sleep(2)
                        html_content = browser.page_source
                        parser = HTMLParser(html_content)

                        if not self._is_captcha_page(parser):
                            return HTMLParser(html_content)
                        retries += 1 
                    except:
                        retries += 1
        raise CaptchaError(f"Captcha page not found after {MAX_RETRIES} retries.")

## TODO: review this solution below that try
## to solve the captcha using requests    

# class CaptchaAudioFactory:
#     def __init__(self, main_url, audio_url):
#         self.main_url = main_url
#         self.audio_url = audio_url
    
#     def is_captcha_page(self, url) -> bool:
#         r = requests.get(url)
#         if r.status_code == 200:
#             print("Captcha page retrieved successfully")
#             return False
#         parser = HTMLParser(r.content)
#         captcha_button = 'a[href="captchaAudio.svl"]'
#         audio_button = parser.css_first(captcha_button)
#         if not audio_button:
#             raise CaptchaError("Captcha page not found")
#         return True

#     def _get_cookies(self) -> None:
#         """
#         Send a request to the main URL and retrieve cookies.
#         """
#         response = requests.get(self.main_url)
#         if response.status_code == 401:
#             self.cookies = response.cookies.get_dict()
#             for k,v in response.cookies.items():
#                 cookies = ''.join([k,'=',v,';'])
#             print(self.headers)
#             print(cookies)
#             self.headers['Cookie'] = cookies
#         else:
#             raise Exception("Failed to retrieve cookies.")

#     def _request_captcha_audio(self) -> bytes:
#         """
#         Request the CAPTCHA audio using the retrieved cookies.
#         """
#         if not self.cookies:
#             raise Exception("Cookies are not set. Call _get_cookies() first.")
#         headers = {
#             "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Language":"en-US,en;q=0.9",
#             "Connection":"keep-alive",
#             "Cookie": self.cookies,
#             "Referer":"https://www5.tjmg.jus.br/jurisprudencia/pesquisaPalavraSentenca.do?palavrasConsulta=ementa+ou+parte+ou+recurso+ou+direito+ou&tipoFiltro=or&codigoComarca=&codigoOrgaoJulgador=&codigoCompostoRelator=&dataInicial=22%2F11%2F2023&dataFinal=22%2F11%2F2023&resultPagina=10&pesquisar=Pesquisar",
#             "Sec-Fetch-Dest":"document",
#             "Sec-Fetch-Mode":"navigate",
#             "Sec-Fetch-Site":"same-origin",
#             "Sec-Fetch-User":"?1",
#             "Upgrade-Insecure-Requests":"1",
#             "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#             "sec-ch-ua-mobile":"?0",
#             "sec-ch-ua-platform":"Windows",
#         }
#         response = requests.get(
#             self.audio_url,
#             headers=self.headers
#         ),
#         print(response[0].content)
#         exit()
#         if response.status_code == 200:
#             return response.content
#         else:
#             raise Exception("Failed to retrieve CAPTCHA audio.")

#     def _recognize_audio(self, audio_data):
#         """
#         Use an audio recognition library to convert the audio to text.
#         """
       
#         audio_path = Path("./tmp/")
#         audio_path.mkdir(parents=True, exist_ok=True)

#         with open( audio_path / "audio_file.wav", "wb") as file:
#             file.write(audio_data)
            
#         # Use speech recognition to convert audio to text
#         recognizer = sr.Recognizer()
        
#         try:
#             with sr.AudioFile(f"{audio_path}/audio_file.wav") as source:
#                 audio = recognizer.listen(source)
#                 captcha_text = recognizer.recognize_google(audio, language="pt-BR")
#             return captcha_text.lower()
#         except sr.UnknownValueError:
#             raise Exception("Google Speech Recognition could not understand audio.")
#         except sr.RequestError:
#             raise Exception("Could not request results from Google Speech Recognition service.")

#     def solve(self, headers: Optional[dict] = None) -> HTMLParser:
#         """
#         Solve the CAPTCHA using the above methods.
#         """
#         print("Solving CAPTCHA...")

#         self._get_cookies()
#         self.headers = headers[0]
       
#         audio_data = self._request_captcha_audio()
        
#         captcha_text = self._recognize_audio(audio_data)
#         is_solved = False
#         retry = 0
#         while not is_solved:
#             res = requests.get(self.main_url, headers=headers, cookies=self.cookies)
#             if res.status_code == 200:
#                 print("Captcha solved successfully")
#                 is_solved = True
#                 return HTMLParser(res.text, "html.parser")
#             retry += 1
#             if retry > MAX_RETRIES:
#                 print("Captcha not solved")
#                 raise Exception("Captcha not solved")

