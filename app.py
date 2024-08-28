import streamlit as st
import requests
from gtts import gTTS
from io import BytesIO
import base64

# 페이지 설정
st.set_page_config(page_title="다국어 번역기 (음성 지원)", layout="centered")

# 웹 페이지 UI
st.title("다국어 번역기 (음성 지원)")

st.markdown("""
<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
    <img src="https://flagicons.lipis.dev/flags/4x3/kr.svg" alt="Korean" style="width:50px;height:50px;">
    <img src="https://flagicons.lipis.dev/flags/4x3/gb.svg" alt="English" style="width:50px;height:50px;">
    <img src="https://flagicons.lipis.dev/flags/4x3/jp.svg" alt="Japanese" style="width:50px;height:50px;">
    <img src="https://flagicons.lipis.dev/flags/4x3/cn.svg" alt="Chinese" style="width:50px;height:50px;">
</div>
""", unsafe_allow_html=True)

input_text = st.text_area("번역할 한국어를 입력하세요...", height=100)
translate_button = st.button("번역하기")

languages = {
    "영어": "en",
    "일본어": "ja",
    "중국어": "zh"
}

def translate_text(text, lang):
    try:
        response = requests.get(f"https://api.mymemory.translated.net/get?q={text}&langpair=ko|{lang}")
        response.raise_for_status()
        data = response.json()
        return data['responseData']['translatedText']
    except requests.exceptions.RequestException as e:
        st.error(f"번역 중 오류가 발생했습니다: {e}")
        return None

def generate_audio(text, lang):
    tts = gTTS(text=text, lang=lang)
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer

def get_audio_player(audio_buffer):
    audio_base64 = base64.b64encode(audio_buffer.read()).decode()
    audio_html = f"""
    <audio controls>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    return audio_html

if translate_button and input_text:
    for language_name, lang_code in languages.items():
        st.subheader(language_name)
        translated_text = translate_text(input_text, lang_code)
        if translated_text:
            st.write(translated_text)
            audio_buffer = generate_audio(translated_text, lang_code)
            audio_player = get_audio_player(audio_buffer)
            st.markdown(audio_player, unsafe_allow_html=True)
