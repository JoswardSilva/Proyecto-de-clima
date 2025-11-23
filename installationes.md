# Guía de Instalación de Herramientas

## Resumen

Esta parte te permitirá instalar los requerimientos para poder continuar con los pasos del README al pie de la letra.  
Los pasos de instalación son diferentes dependiendo de tu sistema operativo.

## Herramientas que Vas a Instalar

| Herramienta              | Propósito                                       |
| ------------------------ | ----------------------------------------------- |
| Python 3                | Ejecuta la aplicación Flask inicial             |
| pip / venv              | Maneja paquetes de Python                       |
| Docker (Colima o WSL2)  | Construye y ejecuta contenedores                |
| Minikube                | Ejecuta un clúster local de Kubernetes          |
| kubectl                 | Administra recursos de Kubernetes               |
| Homebrew (solo macOS)   | Instala herramientas de CLI                     |
| pipx + Ansible          | Infraestructura como Código (desde el Ejercicio 4.1) |

## Usuarios de macOS

Todos los usuarios de macOS (especialmente dispositivos administrados por IBM) **deben usar Colima** en lugar de Docker Desktop.

### Paso 1 – Instalar Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
```

### Paso 2 – Instalar Herramientas Requeridas

```bash
brew install python
brew install colima
brew install docker
brew install minikube
brew install kubectl
```

### Paso 3 – Iniciar Colima

```bash
colima start --cpu 4 --memory 6 --disk 60
docker version
```

## Usuarios de Windows (WSL2 + Ubuntu)

Debes instalar **WSL2** y usar **Ubuntu** como tu distribución Linux.  
Instalaremos **Docker Engine**, **Minikube** y **kubectl**.

### Paso 1 – Habilitar WSL2

Abre **PowerShell como Administrador** y ejecuta:

```powershell
wsl --install
```

Reinicia tu computadora.

### Paso 2 – Habilitar systemd en WSL2

Requerido para que Docker funcione como servicio dentro de WSL2.

En Ubuntu:

```bash
sudo nano /etc/wsl.conf
```

Agrega:

```
[boot]
systemd=true
```

En PowerShell (Windows):

```powershell
wsl --shutdown
```

Reabre Ubuntu.

### Paso 3 – Instalar Docker Engine (Repositorio Oficial)

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg   | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg]   https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) stable"   | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER
newgrp docker
sudo systemctl enable --now docker
docker version
```

### Paso 4 – Instalar kubectl (Repositorio Oficial)

```bash
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg   https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg]   https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /"   | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubectl
kubectl version --client
```

### Paso 5 – Instalar Minikube (Binario Oficial)

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube version
```

### Paso 6 – Instalar Python, pip, venv, pipx y Ansible

```bash
sudo apt-get install -y python3 python3-pip python3-venv pipx
pipx ensurepath
pipx install --include-deps ansible
ansible --version
```

## Iniciar Minikube

```bash
minikube start --driver=docker
kubectl get nodes
```

## Verificación de Herramientas

```bash
python3 --version
pip3 --version
docker --version
minikube version
kubectl version --client
ansible --version
```

## Notes Finales

- **Usuarios de macOS:** deben usar `colima` en lugar de Docker Desktop.  
- **Usuarios de Windows:** usan `WSL2 + Ubuntu + Docker Engine`.  
- Minikube utiliza el **driver Docker** (`--driver=docker`).  
- Una vez completado todo, ya estás listo para continuar con tu proyecto.
