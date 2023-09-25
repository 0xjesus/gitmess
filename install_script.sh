#!/bin/bash

echo "Installing gitmess..."

# Instala pip si no está presente
if ! command -v pip &> /dev/null; then
    echo "pip was not found, installing..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm get-pip.py
fi

# Instala tu paquete
pip install gitmess==0.1.2

# Comprueba si ~/.local/bin está en PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "Adding $HOME/.local/bin to PATH in .bashrc"
    echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
    source ~/.bashrc
fi

# Asegura que el comando gm está disponible globalmente
# Esto asume que gitmess proporciona un punto de entrada llamado gm después de la instalación.
GM_PATH="$HOME/.local/bin/gm"
if [ ! -f "$GM_PATH" ]; then
    echo '#!/bin/bash' > "$GM_PATH"
    echo 'python -m gitmess "$@"' >> "$GM_PATH"
    chmod +x "$GM_PATH"
fi

echo "Gitmess installed!"
