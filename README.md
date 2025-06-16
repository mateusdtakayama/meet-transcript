# MeetTranscript 🎙️

**AI-Powered Meeting Transcription and Summarization Tool**

MeetTranscript is a Streamlit-based web application that provides real-time meeting recording, automatic transcription using OpenAI's Whisper, and AI-powered summarization using GPT models. Record meetings through your microphone, view transcriptions in real-time, and generate intelligent summaries of past meetings.

## ✨ Features

- **Real-time Audio Recording** - Record meetings directly through your web browser using WebRTC
- **Automatic Transcription** - Convert speech to text using OpenAI's Whisper model
- **AI-Powered Summarization** - Generate concise meeting summaries with key points and action items
- **Meeting Management** - Store, organize, and retrieve past meeting recordings and transcriptions
- **Web-based Interface** - Easy-to-use Streamlit interface accessible from any browser
- **Multilingual Support** - Configurable language support for transcription

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Microphone access in your browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd meet-transcript
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📋 Requirements

Create a `requirements.txt` file with the following dependencies:

```
streamlit>=1.28.0
streamlit-webrtc>=0.47.0
openai>=1.0.0
pydub>=0.25.0
python-dotenv>=1.0.0
```

## 🎯 Usage

### Recording a Meeting

1. Navigate to the **"Record Meeting"** tab
2. Click "Start" to begin recording
3. Grant microphone permissions when prompted
4. Start speaking - transcription will appear in real-time
5. The application automatically saves audio and transcription every 5 seconds

### Viewing Past Meetings

1. Navigate to the **"View saved transcriptions"** tab
2. Select a meeting from the dropdown list
3. Add a title to your meeting if not already added
4. View the AI-generated summary and full transcription

### File Structure

The application creates the following file structure:
```
files/
├── YYYY_MM_DD_HH_MM_SS/
│   ├── audio.mp3           # Complete meeting audio
│   ├── audio_temp.mp3      # Temporary audio chunks
│   ├── transcription.txt   # Full meeting transcription
│   ├── title.txt          # Meeting title
│   └── summary.txt        # AI-generated summary
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Customization Options

- **Transcription Language**: Modify the `language` parameter in `transcribe_audio()` function
- **AI Model**: Change the `model` parameter in `chat_openai()` function
- **Summary Prompt**: Customize the `PROMPT` constant to modify summary format
- **Transcription Interval**: Adjust the 5-second interval in `tab_record_meeting()`

## 🏗️ Architecture

### Core Components

- **Audio Processing**: WebRTC for real-time audio capture and PyDub for audio manipulation
- **Transcription Engine**: OpenAI Whisper API for speech-to-text conversion
- **AI Summarization**: OpenAI GPT models for intelligent meeting summaries
- **File Management**: Local file system for storing recordings and metadata
- **User Interface**: Streamlit for the web-based frontend

### Key Functions

- `tab_record_meeting()`: Handles real-time recording and transcription
- `tab_select_meeting()`: Manages meeting selection and display
- `transcribe_audio()`: Interfaces with OpenAI Whisper API
- `chat_openai()`: Handles GPT-based summarization
- `list_meetings()`: Retrieves and formats meeting history

## 🛠️ Development

### Running in Development Mode

```bash
streamlit run main.py --server.runOnSave true
```

### Code Style

The project follows Python best practices:
- Google-style docstrings
- Type hints where appropriate
- Descriptive variable and function names
- Modular function design

## 🔒 Privacy and Security

- **Local Storage**: All recordings and transcriptions are stored locally
- **API Security**: Requires secure OpenAI API key configuration
- **Browser Permissions**: Uses standard WebRTC permissions for microphone access

## 🐛 Troubleshooting

### Common Issues

1. **Microphone not working**
   - Ensure browser has microphone permissions
   - Check system audio settings
   - Try refreshing the page

2. **OpenAI API errors**
   - Verify your API key is correct
   - Check your OpenAI account usage limits
   - Ensure stable internet connection

3. **Audio quality issues**
   - Check microphone settings
   - Ensure quiet environment for better transcription
   - Adjust audio input levels

### Browser Compatibility

- **Recommended**: Chrome, Firefox, Safari (latest versions)
- **WebRTC Support**: Required for audio recording functionality

## 📄 License

This project is open source. Please check the license file for more details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📞 Support

For support and questions, please open an issue in the repository.

---

**Made with ❤️ using Streamlit and OpenAI** 