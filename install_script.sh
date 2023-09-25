#!/bin/bash

echo "Instalando mipaquete..."

# Instala pip si no está presente
if ! command -v pip &> /dev/null; then
    echo "pip no se encontró, instalando..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm get-pip.py
fi

# Instala tu paquete
pip install gitmess==0.1.0

echo "mipaquete ha sido instalado exitosamente!"
