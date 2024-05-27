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
        """
        GPT 클래스는 OpenAI GPT 모델을 사용하여 대화 기능을 제공합니다.

        Args:
            api_key (str): OpenAI API 키입니다.
            model (str, optional): 사용할 GPT 모델의 이름입니다. 기본값은 "gpt-4o-2024-05-13"입니다.
            sys_prompt (str, optional): 시스템 프롬프트로 사용할 문장입니다. 기본값은 "You are a helpful assistant. please speak Korean."입니다.
            top_p (float, optional): GPT 모델의 출력 확률 분포의 상위 p%를 사용하여 텍스트를 생성합니다. 기본값은 1.0입니다.
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.top_p= top_p
        self.messages = [
            {'role': 'system', 'content': f'{sys_prompt}'},
        ]
    
    def _encode_image(self, image_path):
        """
        이미지를 base64로 인코딩하는 함수입니다. GPT에 이미지를 전달하기 위해서는 인터넷 URL이 아닌 경우 base64로 인코딩하여 전달해야 합니다.

        Args:
            image_path (str): 인코딩할 이미지 파일의 경로입니다.

        Returns:
            str: 인코딩된 이미지의 base64 문자열입니다.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _audio_transcript(self,audio_path):
        """
        오디오 파일을 텍스트로 변환하는 함수입니다.

        Args:
            audio_path (str): 변환할 오디오 파일의 경로입니다.

        Returns:
            str: 오디오 파일의 텍스트 변환 결과입니다.
        """
        audio_file= open(audio_path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=audio_file,
        )
        return transcription.text
    
    def assistant_message(self, message):
        """
        Assistant의 메시지를 추가하는 메서드입니다.

        Args:
            message (str): Assistant의 메시지 내용입니다.
        """
        self.messages.append({'role': 'Assistant', 'content': message})
    
    def generate(self, text_prompt, img_list:list=None, audio_list:list=None):
        """
        GPT 모델을 사용하여 텍스트, 이미지, 오디오를 기반으로 대화를 생성하는 메서드입니다.

        Args:
            text_prompt (str): 텍스트 프롬프트로 사용할 문장입니다.
            img_list (list, optional): 이미지 파일 경로의 리스트입니다. 기본값은 None입니다.
            audio_list (list, optional): 오디오 파일 경로의 리스트입니다. 기본값은 None입니다.

        Returns:
            str: 생성된 대화 결과입니다.
        """
        messages = [{"type": "text", "text": text_prompt},]
        if audio_list:
            for audio in audio_list:
                messages.append({"type": "text", "text": self._audio_transcript(audio)})
        if img_list:
            for img in img_list:
                img_type = img.split('.')[-1]
                img = self._encode_image(img)
                messages.append({"type": "image_url", 
                                 "image_url": {"url": f"data:image/{img_type};base64,{img}"}
                })
        self.messages.append({'role': 'user', 'content': messages})
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
    system_prompt = "You are a helpful assistant. please speak Korean."
    gpt = GPT(api_key=openai, model="gpt-4o-2024-05-13", sys_prompt = system_prompt, top_p=1.0)
    text = """
    Q: 언제 가장 외로움을 느끼나요?
    A: 아무도 없는 곳에서 혼자 있을 때 외로움을 느낍니다.
    """
    imgs = []
    answer = gpt.generate(text_prompt = text, 
                          img_list = imgs,
                          audio_list = None
                          )
    print(answer)
