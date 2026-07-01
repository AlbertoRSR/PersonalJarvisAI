import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import subprocess

print("Cargando Whisper...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

while True:

    input("\nPulsa ENTER para hablar...")

    fs = 16000
    duration = 5

    print("Escuchando...")

    audio = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    write("temp.wav", fs, audio)

    print("Transcribiendo...")

    segments, info = model.transcribe("temp.wav")

    texto = ""

    for segment in segments:
        texto += segment.text

    print("\nTÚ:")
    print(texto)

    print("\nJARVIS:")

    comando = [
        "ollama",
        "run",
        "qwen3:14b",
        texto
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    print(resultado.stdout)