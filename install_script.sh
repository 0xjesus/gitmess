#!/bin/bash

echo "Installing gitmess..."

# Instala pip si no está presente
if ! command -v pip &> /dev/null; then
    echo "pip no se encontró, instalando..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm get-pip.py
fi

# Instala tu paquete
pip install gitmess==0.1.0

# Asegura que el comando gm está disponible globalmente
# Esto asume que gitmess proporciona un punto de entrada llamado gm después de la instalación.
if [ ! -f /usr/local/bin/gm ]; then
    echo '#!/bin/bash' > /usr/local/bin/gm
    echo 'python -m gitmess "$@"' >> /usr/local/bin/gm
    chmod +x /usr/local/bin/gm
fi

echo "Gitmess installed!"
