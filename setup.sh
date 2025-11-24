#!/bin/bash
# Setup APENAS DE DEPENDÊNCIAS - Raspberry Pi 3 (64-bit)
# O código Python você vai rodar depois manualmente

echo "🚀 Configurando dependências para Raspberry Pi 3"
echo "================================================"

# 1. Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python e ferramentas essenciais
echo "🐍 Instalando Python e ferramentas..."
sudo apt install -y python3 python3-venv python3-pip python3-full
sudo apt install -y git

# 3. Instalar dependências do OpenCV (sistema)
echo "📦 Instalando dependências do OpenCV..."
sudo apt install -y python3-opencv
sudo apt install -y libopenblas-dev libjpeg-dev libpng-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev
sudo apt install -y libgtk-3-dev libcanberra-gtk3-module

# 4. Instalar ferramentas de câmera
echo "📷 Instalando ferramentas de câmera..."
sudo apt install -y libcamera-dev libcamera-apps v4l-utils

# 5. Configurar câmera (se necessário)
echo "🔧 Verificando configuração da câmera..."
if ! grep -q "^start_x=1" /boot/firmware/config.txt 2>/dev/null && \
   ! grep -q "^start_x=1" /boot/config.txt 2>/dev/null; then
    echo "⚠️  Câmera não está habilitada no config.txt"
    echo "💡 Para habilitar manualmente depois:"
    echo "   sudo nano /boot/firmware/config.txt"
    echo "   Adicione: start_x=1 e gpu_mem=128"
else
    echo "✅ Câmera já está configurada"
fi

echo ""
echo "🎉 Dependências instaladas com sucesso!"
echo ""
echo "================================================"
echo "📝 PRÓXIMOS PASSOS:"
echo "================================================"
echo ""
echo "1️⃣  Clone seu repositório:"
echo "   cd ~"
echo "   git clone https://github.com/seu-usuario/seu-repo.git"
echo "   cd seu-repo"
echo ""
echo "2️⃣  Crie o ambiente virtual:"
echo "   python3 -m venv venv --system-site-packages"
echo ""
echo "3️⃣  Ative o venv:"
echo "   source venv/bin/activate"
echo ""
echo "4️⃣  Instale dependências Python:"
echo "   pip install --upgrade pip"
echo "   pip install numpy"
echo ""
echo "5️⃣  Rode seu código:"
echo "   python3 seu_script.py"
echo ""
echo "================================================"
echo "💡 DICAS:"
echo "================================================"
echo "• Testar câmera: ls /dev/video*"
echo "• Status câmera: vcgencmd get_camera"
echo "• Desativar venv: deactivate"
echo ""
echo "⚠️  Se mudou config da câmera, reinicie:"
echo "   sudo reboot"
echo "================================================"