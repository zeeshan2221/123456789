import requests
import streamlit as st
from io import BytesIO
from pydub import AudioSegment

# Set up ResponsiveVoice API
rv_api_key = st.secrets["responsive_voice_api_key"]


def generate_presentation(topic):
    prompt = f"Please explain {topic} in the most easy and attractive way possible."

    # Set up OpenAI API parameters
    model_engine = "text-davinci-002"
    max_tokens = 1048
    temperature = 0.7

    # Generate the presentation content using OpenAI's GPT-3 API
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )

    return response.choices[0].text


def generate_audio(text):
    # Send a request to the ResponsiveVoice API
    api_url = "https://api.responsivevoice.org/v1/text-to-speech"
    params = {
        "key": rv_api_key,
        "src": text,
        "hl": "en-US",
        "r": "0",
        "c": "mp3",
        "f": "48khz_16bit_stereo",
        "ssml": "false",
        "b64": "true"
    }
    response = requests.get(api_url, params=params)

    # Convert the response audio to a playable format
    audio_bytes = BytesIO(response.content)
    audio_segment = AudioSegment.from_file(audio_bytes.getvalue(), format="mp3")
    audio_segment.export("presentation_audio.mp3", format="mp3")

    return audio_bytes


def main():
    st.title("AICademy")

    topic = st.text_input("Enter the topic for your presentation:")
    submit_button = st.button("Generate Presentation")

    if submit_button and topic:
        presentation = generate_presentation(topic)
        audio = generate_audio(presentation)

        # Display the presentation or video and the generated audio
        st.audio(audio.read(), format='audio/mp3')
        st.write(presentation)


if __name__ == "__main__":
    st.set_page_config(page_title="AICademy", page_icon=":books:")
    main()
