import os
import subprocess
import shutil
import re

# Disinstallazione e installazione di torch, torchvision, e torchaudio
subprocess.run(['pip', 'uninstall', 'torch', 'torchvision', 'torchaudio', '-y'])
print("Disinstallazione di torch, torchvision e torchaudio completata.")
subprocess.run(['pip3', 'install', 'torch', 'torchvision', 'torchaudio', '--index-url', 'https://download.pytorch.org/whl/cu121'])
print("Installazione delle versioni nightly di torch, torchvision e torchaudio completata.")
