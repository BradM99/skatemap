import threading
import time
import webbrowser
import uvicorn

def open_browser():
    """Wait a bit, then open the FastAPI docs page."""
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    """
    Run app with auto-reload and open browser
    """
    threading.Thread(target=open_browser).start()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)