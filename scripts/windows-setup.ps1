# windows-setup.ps1 -- Prepara Windows para el "Curso Python con Pokemon".
#
# Que hace:
#   - Comprueba que es Windows 10/11.
#   - Instala WSL2 + Ubuntu con un solo comando (wsl --install -d Ubuntu).
#   - Te explica, en espanol, los 3 pasos que quedan despues de reiniciar.
#
# NO ejecutes este .ps1 directamente: haz doble clic en "windows-setup.bat"
# (que pide permisos de administrador, necesarios para instalar WSL).

$ErrorActionPreference = "Stop"

function Titulo($t) { Write-Host ""; Write-Host "==> $t" -ForegroundColor Cyan }
function OK($t)     { Write-Host "    [OK] $t" -ForegroundColor Green }
function Aviso($t)  { Write-Host "    [AVISO] $t" -ForegroundColor Yellow }

Titulo "Comprobando Windows..."
$os = [System.Environment]::OSVersion.Version
if ($os.Major -lt 10) {
    Aviso "Necesitas Windows 10 o 11. Detectado: $($os.ToString())"
    Read-Host "Pulsa Enter para salir"
    exit 1
}
OK "Windows $($os.Major) detectado."

Titulo "Comprobando si WSL ya esta instalado..."
$wslPresente = $false
try {
    $distros = (wsl.exe -l -q) 2>$null
    if ($LASTEXITCODE -eq 0 -and $distros) { $wslPresente = $true }
} catch { $wslPresente = $false }

if ($wslPresente) {
    OK "WSL ya esta instalado. Distros: $($distros -join ', ')"
    Aviso "No hace falta instalar nada mas. Salta a 'SIGUIENTES PASOS'."
} else {
    Titulo "Instalando WSL2 + Ubuntu (esto puede tardar unos minutos)..."
    Aviso "Si falla con 'virtualizacion', activa la virtualizacion en la BIOS"
    Aviso "(Intel VT-x / AMD-V) y vuelve a ejecutar este instalador."
    try {
        wsl.exe --install -d Ubuntu
        OK "WSL2 + Ubuntu instalados."
    } catch {
        Aviso "El comando 'wsl --install' fallo o no existe en tu Windows."
        Aviso "Actualiza Windows o instala WSL manualmente:"
        Aviso "  https://learn.microsoft.com/windows/wsl/install"
        Read-Host "Pulsa Enter para salir"
        exit 1
    }
}

Write-Host ""
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host " SIGUIENTES PASOS (importante, leelos)" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host " 1. REINICIA el ordenador (si te lo pide)."
Write-Host ""
Write-Host " 2. Abre el menu Inicio, escribe 'Ubuntu' y abrelo."
Write-Host "    La primera vez te pedira crear un usuario y contrasena"
Write-Host "    de Linux. NOTA: al teclear la contrasena no se ve nada"
Write-Host "    en pantalla; es normal, escribela y pulsa Enter."
Write-Host ""
Write-Host " 3. Dentro de esa ventana de Ubuntu, pega este comando:"
Write-Host ""
Write-Host "      curl -fsSL https://raw.githubusercontent.com/DanielMf31/Curso_Python_Pokemon/main/scripts/bootstrap.sh | bash" -ForegroundColor White
Write-Host ""
Write-Host "    Eso descarga el curso e instala Python y el entorno."
Write-Host ""
Write-Host " 4. Instala VS Code en WINDOWS: https://code.visualstudio.com"
Write-Host "    y dentro de VS Code instala la extension 'WSL'."
Write-Host "    Luego, desde la terminal de Ubuntu:  code ."
Write-Host ""
Write-Host "===========================================================" -ForegroundColor Cyan
Read-Host "Pulsa Enter para cerrar esta ventana"
