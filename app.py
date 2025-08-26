# app.py (수정본 예시)
import subprocess
from flask import Flask, request, abort

app = Flask(__name__)

# 1) 허용된 명령만 지정 (예: 'date', 'uptime' 만 허용)
ALLOWED_CMDS = {
    "date": ["date"],
    "uptime": ["uptime"],
}

def run_safe(cmd_key):
    # 2) 키 기반으로만 명령 실행 (임의 문자열/파라미터 금지)
    if cmd_key not in ALLOWED_CMDS:
        abort(400, "Command not allowed")
    # 3) shell=False + 리스트 인자
    result = subprocess.run(ALLOWED_CMDS[cmd_key], capture_output=True, text=True, check=True)
    return result.stdout

@app.get("/run")
def run_endpoint():
    # ex) /run?cmd=uptime
    cmd_key = request.args.get("cmd", "")
    return {"output": run_safe(cmd_key)}
