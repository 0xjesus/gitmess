#!/bin/bash

echo "Installing gitmess..."

# Check if pip is installed
if ! command -v pip &>/dev/null; then
    echo "pip was not found, installing..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python get-pip.py
    rm get-pip.py
fi

# Install your package
pip install gitmess==0.1.2

# Ensure the gm command is globally available
# This assumes that gitmess provides an entry point named gm after installation.
if [ ! -f /usr/local/bin/gm ]; then
    echo '#!/bin/bash' > /usr/local/bin/gm
    echo 'python -m gitmess "$@"' >> /usr/local/bin/gm
    chmod +x /usr/local/bin/gm
fi

echo "gitmess has been successfully installed!"
