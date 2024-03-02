import sys
import torch
import os
import shutil
import subprocess
import re

# Function to automatically find the CUDA bin path
def find_cuda_bin_path(base_path=r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"):
    version_pattern = re.compile(r'^v\d+\.\d+$')  # Regex to match 'vX.Y' pattern
    cuda_versions = []
    if os.path.exists(base_path):
        print("Checking CUDA installation directory.")
        for item in os.listdir(base_path):
            if version_pattern.match(item):
                cuda_versions.append(item)
        cuda_versions.sort(reverse=True)  # Sort versions to prefer the latest version
        if cuda_versions:
            print(f"Found CUDA version(s): {cuda_versions}")
            return os.path.join(base_path, cuda_versions[0], 'bin')
        else:
            print("No CUDA versions found matching pattern.")
    else:
        print("CUDA installation directory does not exist.")
    return None

# Function to find the TensorRT directory with a version suffix
def find_tensorrt_path(base_directory=os.getcwd()):
    tensorrt_pattern = re.compile(r'^TensorRT-[\d\.]+$')  # Regex to match 'TensorRT-X.Y.Z.W'
    for item in os.listdir(base_directory):
        if tensorrt_pattern.match(item):
            print(f"Found TensorRT directory: {item}")
            return os.path.join(base_directory, item)
    print("TensorRT directory not found.")
    return None

# Function to extract Python version string for TensorRT wheel file
def get_python_version_str():
    major, minor = sys.version_info[:2]
    return f"cp{major}{minor}"

# Function to find the TensorRT wheel file that matches the Python version
def find_tensorrt_whl(tensorrt_directory, python_version_str):
    for root, dirs, files in os.walk(tensorrt_directory):
        for file in files:
            if file.endswith(".whl") and python_version_str in file:
                return os.path.join(root, file)
    return None

python_version = sys.version
version_match = re.match(r"(\d+\.\d+)", python_version)

if version_match:
    python_version = version_match.group(1)
else:
    python_version = "N/A"
print(f"Python version: {python_version}")

cuda_version = torch.version.cuda if torch.cuda.is_available() else "N/A"
print(f"CUDA version: {cuda_version}")

cuda_bin_path = find_cuda_bin_path()
print(f"CUDA bin path: {cuda_bin_path}")

tensorrt_path = find_tensorrt_path()
print(f"TensorRT path: {tensorrt_path}")

python_version_str = get_python_version_str()
tensorrt_whl_path = find_tensorrt_whl(tensorrt_path, python_version_str) if tensorrt_path else None
print(f"TensorRT path: {tensorrt_whl_path}")

tensorrt_lib_path = None
if tensorrt_path:
    tensorrt_lib_path = os.path.join(tensorrt_path, "lib")
    print(f"TensorRT lib path: {tensorrt_lib_path}")
else:
    print("TensorRT directory does not exist or version pattern does not match.")

with open('info.txt', 'w') as info_file:
    info_file.write(f"Python Version: {python_version}\n")
    info_file.write(f"CUDA Toolkit Version: {cuda_version}\n")
    print(f"Writing Python and CUDA versions to info.txt.")

    if cuda_bin_path:
        info_file.write(f"CUDA Libraries Path: {cuda_bin_path}\n")
        print("CUDA Libraries Path found and written to info.txt.")
    else:
        info_file.write("Please install CUDA Toolkit and cuDNN before proceeding.\n")
        print("CUDA Toolkit and cuDNN installation required.")

    if tensorrt_lib_path:
        info_file.write(f"TensorRT Path: {tensorrt_lib_path}\n")
        print("TensorRT Path found and written to info.txt.")
        
        if cuda_bin_path:
            dll_files = [file for file in os.listdir(tensorrt_lib_path) if file.endswith(".dll")]
            for dll_file in dll_files:
                src_path = os.path.join(tensorrt_lib_path, dll_file)
                dst_path = os.path.join(cuda_bin_path, dll_file)
                shutil.copy(src_path, dst_path)
            info_file.write("DLL files copied from TensorRT to CUDA bin directory.\n")
            print("DLL files copied from TensorRT to CUDA bin directory.")
        else:
            info_file.write("Could not copy DLL files from TensorRT to CUDA bin directory because CUDA is unavailable.\n")
            print("Could not copy DLL files due to missing CUDA path.")
        
        # Process for 'uff', 'onnx_graphsurgeon', 'graphsurgeon', and 'python' directories
        for subdir in ['uff', 'onnx_graphsurgeon', 'graphsurgeon']:
            specific_path = os.path.join(tensorrt_path, subdir)
            if os.path.exists(specific_path):
                print(f"Checking directory: {subdir}")
                info_file.write(f"Path of {subdir} directory: {specific_path}\n")
                
                whl_file = next((file for file in os.listdir(specific_path) if file.endswith(".whl")), None)
                if whl_file:
                    whl_path = os.path.join(specific_path, whl_file)
                    info_file.write(f"Path of '.whl' file in {subdir} directory: {whl_path}\n")
                    print(f"Found '.whl' file in {subdir} directory: {whl_path}")
                    try:
                        subprocess.run(["pip", "install", whl_path], check=True)
                        info_file.write(f"Successfully installed '{whl_file}' using pip.\n")
                        print(f"Successfully installed '{whl_file}' using pip.")
                    except subprocess.CalledProcessError as e:
                        info_file.write(f"Failed to install '{whl_file}' with pip: {e}\n")
                        print(f"Failed to install '{whl_file}' with pip.")
                else:
                    info_file.write(f"No '.whl' file found in {subdir} directory.\n")
                    print(f"No '.whl' file found in {subdir} directory.")
            else:
                info_file.write(f"The '{subdir}' directory is not present in the TensorRT directory.\n")
                print(f"The '{subdir}' directory is not present in the TensorRT directory.")

    else:
        info_file.write("No suitable TensorRT wheel file found for the current Python version.\n")

    if tensorrt_whl_path:
        try:
            subprocess.run(["pip", "install", tensorrt_whl_path], check=True)
            info_file.write(f"Successfully installed TensorRT from {tensorrt_whl_path}\n")
            print("Successfully installed TensorRT")
        except subprocess.CalledProcessError as e:
            info_file.write(f"Failed to install TensorRT wheel: {e}\n")
            print("Failed to install TensorRT wheel")
    else:
        info_file.write("No suitable TensorRT wheel file found for the current Python version.\n")

print("Setup completed. Check info.txt for details.")
