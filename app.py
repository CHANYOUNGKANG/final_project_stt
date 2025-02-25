from flask import Flask, request, jsonify
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(dotenv_path="stt.env")

# Azure Speech 서비스 설정
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
SPEECH_ENDPOINT = "https://koreacentral.api.cognitive.microsoft.com/"

app = Flask(__name__)

def speech_to_text(audio_file):
    """
    음성 파일을 받아 텍스트로 변환하는 함수
    """
    try:
        if not SPEECH_KEY or not SPEECH_REGION:
            raise ValueError("Azure Speech API 키 또는 리전이 설정되지 않았습니다.")

        # Azure Speech 설정
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.endpoint_id = SPEECH_ENDPOINT
        speech_config.speech_recognition_language = "ko-KR"

        # 오디오 파일 설정
        audio_config = speechsdk.AudioConfig(filename=audio_file)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        else:
            return "음성 인식 실패"

    except Exception as e:
        return f"오류 발생: {str(e)}"

@app.route('/stt', methods=['POST', 'GET'])
def stt():
    """
    음성 파일을 받아 STT 변환 후 텍스트 반환하는 API
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    file_path = "temp_audio.wav"
    file.save(file_path)

    text = speech_to_text(file_path)
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
