"""
MeetTranscript - AI-Powered Meeting Transcription and Summarization Tool

This Streamlit application provides real-time meeting recording,
transcription using OpenAI's Whisper,
and AI-powered summarization using GPT models. Users can record meetings through their microphone,
view transcriptions in real-time, and generate summaries of past meetings.

Features:
- Real-time audio recording via WebRTC
- Automatic transcription using OpenAI Whisper
- AI-powered meeting summarization
- Meeting storage and retrieval system
- Web-based interface using Streamlit

Dependencies:
- streamlit
- streamlit-webrtc
- openai
- pydub
- python-dotenv
"""

from pathlib import Path
from datetime import datetime
import time
import queue

from streamlit_webrtc import WebRtcMode, webrtc_streamer
import streamlit as st

import pydub
import openai
from dotenv import load_dotenv, find_dotenv

FILES_FOLDER = Path(__file__).parent / "files"
FILES_FOLDER.mkdir(exist_ok=True)

PROMPT = """
Summarize the text delimited by #### 
The text is a transcription of a meeting.
The summary should include the main topics discussed.
The summary should have a maximum of 300 characters.
The summary should be in running text.
At the end, all agreements and arrangements 
made in the meeting should be presented in bullet point format.

The final format I want is:

Meeting Summary:
- write the summary here.

text: ####{}####
"""


_ = load_dotenv(find_dotenv())


def save_file(file_path, content):
    """
    Save content to a file.

    Args:
        file_path (Path): Path to the file where content will be saved
        content (str): Content to write to the file

    Returns:
        None
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def read_file(file_path):
    """
    Read content from a file.

    Args:
        file_path (Path): Path to the file to read

    Returns:
        str: Content of the file, or empty string if file doesn't exist
    """
    if file_path.exists():
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    else:
        return ""


def list_meetings():
    """
    List all meetings stored in the files folder.

    Returns:
        dict: Dictionary mapping meeting dates to formatted display strings
              Format: {date_string: "YYYY/MM/DD HH:MM:SS - title"}
    """
    meeting_list = FILES_FOLDER.glob("*")
    meeting_list = list(meeting_list)
    meeting_list.sort(reverse=True)
    meetings_dict = {}
    for meeting_folder in meeting_list:
        meeting_date = meeting_folder.stem
        year, month, day, hour, min, sec = meeting_date.split("_")
        meetings_dict[meeting_date] = f"{year}/{month}/{day} {hour}:{min}:{sec}"
        title = read_file(meeting_folder / "title.txt")
        if title != "":
            meetings_dict[meeting_date] += f" - {title}"
    return meetings_dict


# OPENAI UTILS =====================
client = openai.OpenAI()


def transcribe_audio(audio_path, language="pt", response_format="text"):
    """
    Transcribe audio file using OpenAI's Whisper model.

    Args:
        audio_path (Path): Path to the audio file to transcribe
        language (str): Language code for transcription (default: "pt")
        response_format (str): Format of the response (default: "text")

    Returns:
        str: Transcribed text from the audio file
    """
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            language=language,
            response_format=response_format,
            file=audio_file,
        )
    return transcription


def chat_openai(
    message,
    model="gpt-3.5-turbo-1106",
):
    """
    Send a message to OpenAI's chat completion API.

    Args:
        message (str): Message to send to the AI model
        model (str): OpenAI model to use (default: "gpt-3.5-turbo-1106")

    Returns:
        str: Response from the AI model
    """
    messages = [{"role": "user", "content": message}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content


# TAB RECORD MEETING =====================


def add_audio_chunk(audio_frames, audio_chunk):
    """
    Add audio frames to an existing audio chunk.

    Args:
        audio_frames (list): List of audio frames from WebRTC
        audio_chunk (AudioSegment): Existing audio chunk to append to

    Returns:
        AudioSegment: Updated audio chunk with new frames added
    """
    for frame in audio_frames:
        sound = pydub.AudioSegment(
            data=frame.to_ndarray().tobytes(),
            sample_width=frame.format.bytes,
            frame_rate=frame.sample_rate,
            channels=len(frame.layout.channels),
        )
        audio_chunk += sound
    return audio_chunk


def tab_record_meeting():
    """
    Handle the meeting recording tab functionality.

    Sets up WebRTC audio streaming, records audio in real-time,
    performs periodic transcription, and saves both audio and transcription
    to the file system.

    Returns:
        None
    """
    webrtx_ctx = webrtc_streamer(
        key="receive_audio",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={"video": False, "audio": True},
    )

    if not webrtx_ctx.state.playing:
        return

    container = st.empty()
    container.markdown("Start speaking")
    meeting_folder = FILES_FOLDER / datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    meeting_folder.mkdir()

    last_transcription = time.time()
    complete_audio = pydub.AudioSegment.empty()
    audio_chunk = pydub.AudioSegment.empty()
    transcription = ""

    while True:
        if webrtx_ctx.audio_receiver:
            try:
                audio_frames = webrtx_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                continue
            complete_audio = add_audio_chunk(audio_frames, complete_audio)
            audio_chunk = add_audio_chunk(audio_frames, audio_chunk)
            if len(audio_chunk) > 0:
                complete_audio.export(meeting_folder / "audio.mp3")
                now = time.time()
                if now - last_transcription > 5:
                    last_transcription = now
                    audio_chunk.export(meeting_folder / "audio_temp.mp3")
                    chunk_transcription = transcribe_audio(
                        meeting_folder / "audio_temp.mp3"
                    )
                    transcription += chunk_transcription
                    save_file(meeting_folder / "transcription.txt", transcription)
                    container.markdown(transcription)
                    audio_chunk = pydub.AudioSegment.empty()
        else:
            break


# TAB SELECT MEETING =====================
def tab_select_meeting():
    """
    Handle the meeting selection tab functionality.

    Displays a list of previously recorded meetings, allows users to select
    a meeting, add titles, and view transcriptions and AI-generated summaries.

    Returns:
        None
    """
    meetings_dict = list_meetings()
    if len(meetings_dict) > 0:
        selected_meeting = st.selectbox(
            "Select a meeting", list(meetings_dict.values())
        )
        st.divider()
        meeting_date = [k for k, v in meetings_dict.items() if v == selected_meeting][0]
        meeting_folder = FILES_FOLDER / meeting_date
        if not (meeting_folder / "title.txt").exists():
            st.warning("Add a title")
            meeting_title = st.text_input("Meeting title")
            st.button("Save", on_click=save_title, args=(meeting_folder, meeting_title))
        else:
            title = read_file(meeting_folder / "title.txt")
            transcription = read_file(meeting_folder / "transcription.txt")
            summary = read_file(meeting_folder / "summary.txt")
            if summary == "":
                generate_summary(meeting_folder)
                summary = read_file(meeting_folder / "summary.txt")
            st.markdown(f"## {title}")
            st.markdown(f"{summary}")
            st.markdown(f"Transcription: {transcription}")


def save_title(meeting_folder, title):
    """
    Save the title of a meeting to a file.

    Args:
        meeting_folder (Path): Path to the meeting folder
        title (str): Title to save for the meeting

    Returns:
        None
    """
    save_file(meeting_folder / "title.txt", title)


def generate_summary(meeting_folder):
    """
    Generate an AI-powered summary of a meeting transcription.

    Args:
        meeting_folder (Path): Path to the meeting folder containing transcription.txt

    Returns:
        None

    Side Effects:
        Creates a summary.txt file in the meeting folder with the generated summary
    """
    transcription = read_file(meeting_folder / "transcription.txt")
    summary = chat_openai(message=PROMPT.format(transcription))
    save_file(meeting_folder / "summary.txt", summary)


# MAIN =====================
def main():
    """
    Main function that sets up and runs the Streamlit application.

    Creates the main interface with two tabs:
    1. Record Meeting - for real-time recording and transcription
    2. View saved transcriptions - for reviewing past meetings

    Returns:
        None
    """
    st.header("Welcome to MeetTranscript 🎙️", divider=True)
    tab_record, tab_selection = st.tabs(["Record Meeting", "View saved transcriptions"])
    with tab_record:
        tab_record_meeting()
    with tab_selection:
        tab_select_meeting()


if __name__ == "__main__":
    main()
