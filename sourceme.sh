if [ "$VIRTUAL_ENV" == "" ]; then
    echo "Activating venv.."
    if [ -f "venv/bin/activate" ]; then
        source "venv/bin/activate"
    fi
fi


export PB_BASE_URL=${PB_BASE_URL:-"http://127.0.0.1:5000/api/1.0"}
echo "PB_BASE_URL=$PB_BASE_URL"

if [ "$PB_USER" == "" -a "$PB_TOKEN" == "" ]; then
    echo "PB_USER or PB_TOKEN must be set in the environment" >&2
    return
fi
if [ "$PB_PASSWD" == "" -a "$PB_TOKEN" == "" ]; then
    echo "PB_PASSWD or PB_TOKEN must be set in the environment" >&2
    return
fi
