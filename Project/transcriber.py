import whisper
import ssl

ssl._create_default_https_context = ssl._create_unverified_context # whisper model load시 인증서 오류가 남

def transcribe_audio(file_path):
    """ Transcribes the audio in the file_path.

    Args:
        file_path (string): Path of this audio file. In this case, file name is fixed to 'temp_audio'.

    Returns:
        string: transcription of the audio
    """    
    model = whisper.load_model("turbo", device='cpu')
    result = model.transcribe(file_path)
    return result['text']

