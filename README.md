# README - AutoInstall TensorRT Script

## Overview

This Python script automates the process of installing TensorRT on Windows systems equipped with NVIDIA GPUs. It simplifies the installation and configuration of necessary components for leveraging TensorRT capabilities, including CUDA toolkit version checks, package extraction, and library management.

## Features

- **CUDA Version Detection**: Automatically detects the latest installed version of the NVIDIA CUDA toolkit on the system.
- **TensorRT Package Extraction**: Locates and extracts the appropriate TensorRT package based on the detected CUDA version from a local storage.
- **Library Management**: Uninstalls previous installations of TensorRT-related Python libraries to ensure compatibility.
- **Clean Installation**: Removes any existing TensorRT directories before and after the installation process to maintain a clean environment.

## Important Note

The script **does not automatically download TensorRT packages** from NVIDIA's website. Users must **manually download the TensorRT package** (in zip format) and save it on their computer. Currently, the script is compatible with **TensorRT version 8.6.1.6**. Ensure you have the correct version of the TensorRT zip package saved on your system before running the script.

## How It Works

1. **Find Latest CUDA Version**: Checks the specified CUDA base directory for installed versions, identifying the latest version to determine the compatible TensorRT package.

2. **Copy Directory Tree**: Facilitates the copying of directory structures, useful for managing installation directories and files.

3. **Extract TensorRT Package**: Based on the detected CUDA version, the script locates and extracts the corresponding TensorRT package from a specified search path on the local system, utilizing 7-Zip for extraction.

4. **Uninstall TensorRT-Related Libraries**: Uninstalls any existing TensorRT-related Python libraries (`onnx_graphsurgeon`, `graphsurgeon`, `uff`, `tensorrt`) to avoid version conflicts.

5. **Remove TensorRT Directory**: Cleans up any pre-existing TensorRT installation directories to ensure a fresh installation environment.

6. **Run AutoInstallTR Script**: Executes a specified Python script (e.g., an installer script) to complete the TensorRT installation process.

## Requirements

- Windows OS with NVIDIA GPU
- Python 3.x
- NVIDIA CUDA Toolkit installed
- 7-Zip installed for package extraction
- Administrative privileges for library installation and directory management
- A local copy of the TensorRT-8.6.1.6 zip package

## Usage

Before running the script, ensure that the CUDA Toolkit, 7-Zip, and the TensorRT zip package are installed on your system. Modify the script parameters (`cuda_base_path`, `seven_zip_path`, and `search_path`) as necessary to match your system configuration.

To execute the script, use the following command in a terminal with administrative privileges:

```bash
python autoinstall_tensorrt.py
```

Follow any on-screen prompts to complete the installation process.

## Note

This script is designed for convenience and automates many of the tedious steps involved in setting up TensorRT. However, it is recommended to manually verify the installation steps and requirements based on the latest NVIDIA documentation to ensure compatibility with your specific system and use case.
