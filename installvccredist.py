import subprocess
import os
import time

# Definisce il contenuto dello script PowerShell
ps_script_content = """
Write-Host "#######INSTALL WIN APP#####"
# Array di pacchetti
$packages = @(
    # Pacchetti Visual C++
    'Microsoft.VCRedist.2008.x86'
    'Microsoft.VCRedist.2008.x64'
    'Microsoft.VCRedist.2010.x86'
    'Microsoft.VCRedist.2010.x64'
    'Microsoft.VCRedist.2012.x86'
    'Microsoft.VCRedist.2012.x64'
    'Microsoft.VCRedist.2013.x86'
    'Microsoft.VCRedist.2013.x64'
    'Microsoft.VCRedist.2015+.x86'
    'Microsoft.VCRedist.2015+.x64'


    # Pacchetti DirectX
    'Microsoft.DirectX'
    # Pacchetti Framework 4.5.1
    'Microsoft.DotNet.Framework.DeveloperPack_4'

)

# Installa tutti i pacchetti
ForEach ($packageName in $packages) {
    Write-Host "Installazione di $packageName in corso..."
    winget install $packageName -e  --accept-source-agreements
    Write-Host "Installazione di $packageName completata!"
}

# Messaggio di completamento
Write-Host "Installazione di tutti i pacchetti completata!"

"""

# Imposta il percorso e il nome del file dello script PowerShell
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
ps_script_filename = "manage_devices.ps1"
ps_script_path = os.path.join(desktop_path, ps_script_filename)

# Scrive lo script PowerShell in un file
with open(ps_script_path, "w") as ps_script_file:
    ps_script_file.write(ps_script_content)

# Comando per eseguire lo script PowerShell come amministratore
run_as_admin_command = f"powershell Start-Process powershell -ArgumentList '-File {ps_script_path}' -Verb RunAs"

# Esegue lo script PowerShell come amministratore
subprocess.run(run_as_admin_command, shell=True)

# [OPZIONALE] Attesa per simulare l'attesa del completamento dello script
# Questo passo è opzionale e dipende da quanto tempo ci si aspetta che lo script impieghi
#time.sleep(1)

# Elimina il file dello script PowerShell dopo l'esecuzione
# Si consiglia di utilizzare questa riga con cautela e di assicurarsi che lo script PowerShell sia effettivamente terminato
os.remove(ps_script_path)
