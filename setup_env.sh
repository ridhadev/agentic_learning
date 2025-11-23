#!/bin/bash

# Define environment name
ENV_NAME="agentic_learning"

echo "🚀 Setting up the '$ENV_NAME' environment..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Error: Conda is not installed or not in your PATH."
    exit 1
fi

# Create the environment with Python 3.10
echo "📦 Creating Conda environment with Python 3.10..."
conda create -n $ENV_NAME python=3.10 -y

# Activate the environment
# Note: 'conda activate' might not work in all shell scripts depending on how conda is initialized.
# We use 'source' with the conda.sh script if available, or rely on the user to activate it later if this fails.
# A more robust way for scripts is often to run commands using 'conda run'.

echo "📥 Installing dependencies from requirements.txt..."
# Using conda run to execute pip install inside the new environment
conda run -n $ENV_NAME pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "    conda activate $ENV_NAME"
