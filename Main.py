import os
import subprocess
import shutil
import re

cuda_base_path = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\"
seven_zip_path = "C:\\Program Files\\7-Zip\\7z.exe"

def find_latest_cuda_version(cuda_base_path):
    if not os.path.exists(cuda_base_path):
        return None, None
    versions = []
    for dir_name in os.listdir(cuda_base_path):
        if re.match(r'v\d+\.\d+', dir_name):
            versions.append(dir_name)
    if not versions:
        return None, None
    latest_version = sorted(versions, key=lambda x: [int(num) for num in x[1:].split('.')], reverse=True)[0]
    major_version = latest_version.split('.')[0][1:]
    return os.path.join(cuda_base_path, latest_version), major_version

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            copytree(src_path, dst_path, symlinks, ignore)
        else:
            shutil.copy2(src_path, dst_path)

def extract_tensorrt_package(cuda_base_path, seven_zip_path, search_path="C:\\"):
    cuda_path, cuda_major_version = find_latest_cuda_version(cuda_base_path)
    if not cuda_major_version:
        print("CUDA version not found or not supported.")
        return

    if cuda_major_version == '11':
        zip_name = "TensorRT-8.6.1.6.Windows10.x86_64.cuda-11.8.zip"
    elif cuda_major_version == '12':
        zip_name = "TensorRT-8.6.1.6.Windows10.x86_64.cuda-12.0.zip"
    else:
        print(f"Versione CUDA {cuda_major_version} non supportata.")
        return

    current_directory = os.path.dirname(os.path.realpath(__file__))
    dest_path = current_directory

    found = None
    for root, dirs, files in os.walk(search_path):
        if zip_name in files:
            found = os.path.join(root, zip_name)
            break

    if not found:
        print(f"File {zip_name} not found.")
        return

    print(f"Found {zip_name} at {found}")
    if not os.path.exists(seven_zip_path):
        print("7-Zip not found. Please install it or check the path.")
        return

    subprocess.run([seven_zip_path, 'x', found, f"-o{dest_path}", '-y'])
    print(f"Files extracted to {dest_path}.")

def uninstall_tensorrt_related_libraries():
    libraries = ['onnx_graphsurgeon', 'graphsurgeon', 'uff', 'tensorrt']
    for lib in libraries:
        try:
            subprocess.run(['pip', 'uninstall', lib, '-y'], check=True)
            print(f"{lib} disinstallation completed.")
        except subprocess.CalledProcessError:
            print(f"Failed to uninstall {lib}. It might not be installed.")

def remove_tensorrt_directory_if_exists(directory_name="TensorRT-8.6.1.6"):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    target_directory_path = os.path.join(current_directory, directory_name)
    
    if os.path.exists(target_directory_path) and os.path.isdir(target_directory_path):
        try:
            shutil.rmtree(target_directory_path)
            print(f"La cartella {directory_name} è stata eliminata con successo.")
        except Exception as e:
            print(f"Errore nell'eliminazione della cartella {directory_name}: {e}")
    else:
        print(f"La cartella {directory_name} non esiste nella directory corrente.")

def run_autoinstallTR_script(script_name="installer.py"):
    try:
        # Esegue lo script Python specificato
        result = subprocess.run(['python', script_name], check=True, text=True, capture_output=True)
        print(f"Script executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        # Gestisce l'errore nel caso in cui lo script termini con un errore
        print(f"Error executing script: {e.stderr}")

def run_apytorch_script(script_name="apytorch.py"):
    try:
        # Esegue lo script Python specificato
        result = subprocess.run(['python', script_name], check=True, text=True, capture_output=True)
        print(f"Script executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        # Gestisce l'errore nel caso in cui lo script termini con un errore
        print(f"Error executing script: {e.stderr}")

def run_cudnn_script(script_name="acudnn.py"):
    try:
        # Esegue lo script Python specificato
        result = subprocess.run(['python', script_name], check=True, text=True, capture_output=True)
        print(f"Script executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        # Gestisce l'errore nel caso in cui lo script termini con un errore
        print(f"Error executing script: {e.stderr}")


# Esempio di utilizzo della funzione
uninstall_tensorrt_related_libraries()
remove_tensorrt_directory_if_exists()
extract_tensorrt_package(cuda_base_path, seven_zip_path)
run_autoinstallTR_script()
remove_tensorrt_directory_if_exists()
run_cudnnpytorch_script()
