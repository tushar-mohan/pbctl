if [ "$VIRTUAL_ENV" == "" ]; then
    echo "Activating venv.."
    if [ -f "venv/bin/activate" ]; then
        source "venv/bin/activate"
    fi
fi

export PB_BASE_URL=${PB_BASE_URL:-"http://127.0.0.1:5000/api/1.0"}
echo "PB_BASE_URL=$PB_BASE_URL"
export PATH="$PWD:$PATH"; echo "Added $PWD to PATH"
