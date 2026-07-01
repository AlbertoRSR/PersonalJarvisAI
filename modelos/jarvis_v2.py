import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import os
import subprocess
import re

def abrir_bloc():
    os.system("notepad.exe")
    
def abrir_calculadora():
    os.system("calc.exe")

def abrir_steam():
    ruta = r"E:\Steam\steam.exe"
    subprocess.Popen(ruta)

def abrir_opera():
    ruta = r"C:\Users\alber\AppData\Local\Programs\Opera GX\opera.exe"
    subprocess.Popen(ruta)

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = texto.strip()
    return texto

print("Cargando Whisper...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)
try:
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
        
        print(os.path.abspath("temp.wav"))

        print("Transcribiendo...")

        segments, info = model.transcribe("temp.wav")

        texto = ""

        for segment in segments:
            texto += segment.text
    
        texto_l = limpiar_texto(texto)
    
        print("\nTÚ:")
        print(texto)

        print("\nJARVIS:")
    
        if "abre bloc de notas" in texto_l:
            print("Abriendo bloc...")
            abrir_bloc()
            continue

        if "abre calculadora" in texto_l:
            print("Abriendo calculadora...")
            abrir_calculadora()
            continue

        if "abre steam" in texto_l:
            print("Abriendo Steam...")
            abrir_steam()
            continue
    
        if "abre opera" in texto_l:
            print("Abriendo Opera...")
            abrir_opera()
            continue
    
        if "jarvis salir" in texto_l:
            print("Hasta luego.")
            break
    
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
        
except KeyboardInterrupt:
    print("\nCerrando Jarvis...")
    
    
finally:
    print("Entrando en finally...")
    if os.path.exists("temp.wav"):
        try:
            os.remove("temp.wav")
            print("temp.wav eliminado")
        except Exception as e:
            print(f"Error borrando temp.wav: {e}")