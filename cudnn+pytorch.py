import os
import subprocess
import shutil
import re

def find_latest_cuda_version(cuda_base_path):
    """Trova la versione più recente di CUDA installata."""
    if not os.path.exists(cuda_base_path):
        return None, None  # Restituisce None anche per la versione principale di CUDA
    versions = []
    for dir in os.listdir(cuda_base_path):
        if re.match(r'v\d+\.\d+', dir):  # Assicura che il nome della cartella corrisponda al pattern di versione
            versions.append(dir)
    if not versions:
        return None, None
    latest_version = sorted(versions, key=lambda x: [int(num) for num in x[1:].split('.')], reverse=True)[0]
    major_version = latest_version.split('.')[0][1:]  # Estrae la parte numerica principale della versione (es. "11" da "v11.3")
    return os.path.join(cuda_base_path, latest_version), major_version

def copytree(src, dst, symlinks=False, ignore=None):
    """Copia i file da src a dst sovrascrivendo i file esistenti."""
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if not os.path.exists(d):
                os.makedirs(d)
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

cuda_base_path = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\"
final_dest, cuda_major_version = find_latest_cuda_version(cuda_base_path)

if not final_dest:
    print("Nessuna installazione di CUDA trovata. Verifica il percorso di installazione di CUDA.")
    exit()

# Seleziona il file ZIP di cuDNN in base alla versione principale di CUDA
if cuda_major_version == '11':
    zip_name = "cudnn-windows-x86_64-8.9.7.29_cuda11-archive.zip"
elif cuda_major_version == '12':
    zip_name = "cudnn-windows-x86_64-8.9.7.29_cuda12-archive.zip"
else:
    print(f"Versione CUDA {cuda_major_version} non supportata.")
    exit()

dest_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
seven_zip_path = "C:\\Program Files\\7-Zip\\7z.exe"

# Cerca il file ZIP
found = None
for root, dirs, files in os.walk("C:\\"):
    if zip_name in files:
        found = os.path.join(root, zip_name)
        break

if not found:
    print(f"File {zip_name} not found.")
else:
    print(f"Found {zip_name} at {found}")
    if not os.path.exists(seven_zip_path):
        print("7-Zip not found. Please install it or check the path.")
    else:
        # Estrae il file ZIP
        subprocess.run([seven_zip_path, 'x', found, f"-o{dest_path}", '-y'])
        print(f"Files extracted to {dest_path}.")
        
        extracted_folder = os.path.join(dest_path, zip_name[:-4])  # Rimuove '.zip' dal nome per ottenere il nome della cartella
        if os.path.exists(extracted_folder):
            print(f"Moving extracted files to {final_dest}")
            copytree(extracted_folder, final_dest)
            print("Files moved.")
            shutil.rmtree(extracted_folder)
            print("Extracted folder deleted from Desktop.")
        else:
            print("Extracted folder not found.")

# Disinstallazione e installazione di torch, torchvision, e torchaudio
subprocess.run(['pip', 'uninstall', 'torch', 'torchvision', 'torchaudio', '-y'])
print("Disinstallazione di torch, torchvision e torchaudio completata.")
subprocess.run(['pip3', 'install', 'torch', 'torchvision', 'torchaudio', '--index-url', 'https://download.pytorch.org/whl/cu121'])
print("Installazione delle versioni nightly di torch, torchvision e torchaudio completata.")
