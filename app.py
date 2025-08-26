import os, subprocess
from flask import Flask
app = Flask(__name__)

@app.get("/")
def hi():
    return "hello"

# (데모용 취약) URL 파라미터를 명령 실행에 사용 — Bandit이 잡을 대상
@app.get("/run/<cmd>")
def run(cmd):
    return subprocess.getoutput(cmd)

if __name__ == "__main__":
    app.run()
