import os
from dotenv import load_dotenv
from openai import OpenAI
import base64
import requests

class GPT:
    def __init__(self, 
                 api_key, 
                 model="gpt-4o-2024-05-13", 
                 sys_prompt="You are a helpful assistant. please speak Korean.",
                 top_p=1.0, 
                 ):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.top_p= top_p
        self.messages = [
            {'role': 'system', 'content': f'{sys_prompt}'},
        ]
    
    def _encode_image(self, image_path):
        # 이미지를 base64로 인코딩하는 함수입니다. gpt에 이미지를 넘기기 위해서는 인터넷url이 아닌경우 base64로 인코딩하여 넘겨야합니다.
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _audio_transcript(self,audio_path):
        #단일 오디오 파일만 입력가능합니다.
        #오디오 파일을 텍스트로 변환하는 함수입니다.
        audio_file= open(audio_path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=audio_file,
        )
        return transcription.text
    
    def assistant_message(self, message):
        self.messages.append({'role': 'Assistant', 'content': message})
    
    def generate(self, text_prompt, img_list:list=None, audio_list:list=None):
        messages = [{"type": "text", "text": text_prompt},]
        # 오디오가 입력되었을때 오디오를 텍스트로 변환합니다.
        if audio_list:
            for audio in audio_list:
                # 오디오 파일을 텍스트로 변환후 메세지에 추가합니다.
                messages.append({"type": "text", "text": self._audio_transcript(audio)})
        # 이미지가 입력되었을때 이미지를 base64로 인코딩하여 메세지에 추가합니다.
        if img_list:
            for img in img_list:
                # 이미지가 입력되면 이미지의 확장자를 가져옵니다. base64로 인코딩하게 될때 url에 이미지 타입이 포함되어 다양한 상황에 대응하기 위함입니다.
                img_type = img.split('.')[-1]
                # 이미지를 base64로 인코딩합니다.
                img = self._encode_image(img)
                # 이미지를 메세지에 추가합니다. 다중 이미지를 넘기기 위해서는 여러번 추가하기 위해 for문을 사용합니다.
                messages.append({"type": "image_url", 
                                 "image_url": {"url": f"data:image/{img_type};base64,{img}"}
                })
        # openai api에 요청할 메세지를 생성합니다.
        self.messages.append({'role': 'user', 'content': messages})
        # 메세지를 openai에 전달합니다.
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            top_p=self.top_p,
        )

        self.messages.append({'role': 'assistant', 'content': completion.choices[0].message.content})
        return completion.choices[0].message.content
    
if __name__ == "__main__":     
    load_dotenv()
    openai = os.getenv("OPENAI_API_KEY")
    ## Example
    gpt = GPT(api_key=openai, model="gpt-4o-2024-05-13", top_p=1.0)
    text_prompt = """
    Q: What is human life expectancy in the United States?
    A: Human life expectancy in the United States is 78 years.
    """
    img_prompt = []
    img_prompt.append('image.png')
    # img_prompt.append('football.png')
    answer = gpt.generate(text_prompt="", img_list=img_prompt,audio_list=None)
    print(answer)
