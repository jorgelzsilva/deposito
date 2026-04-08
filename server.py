"""
depósito — servidor web para automação editorial
Roda com: python server.py
CLI original continua funcionando: python main.py
"""
import os
import re
import sys
import json
import signal
import subprocess
import threading
import queue
import time
from flask import Flask, send_from_directory, jsonify, request, Response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
SETTINGS_FILE = os.path.join(BASE_DIR, 'config', 'settings.py')

app = Flask(__name__, static_folder=STATIC_DIR)

# ─── Global state for the running process ──────────────────────────
_process = None          # subprocess.Popen
_process_lock = threading.Lock()
_log_queues = []         # list of queue.Queue, one per SSE client
_queues_lock = threading.Lock()


# ═══════════════════════════════════════════════════════════════════
# STATIC / HTML
# ═══════════════════════════════════════════════════════════════════
@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(STATIC_DIR, path)


# ═══════════════════════════════════════════════════════════════════
# API — SETTINGS
# ═══════════════════════════════════════════════════════════════════
def _read_settings_raw():
    """Read and exec config/settings.py, returns (JOB, MODULOS, PATHS)"""
    with open(SETTINGS_FILE, 'r', encoding='utf-8', errors='replace') as f:
        src = f.read()
    ns = {}
    exec(compile(src, SETTINGS_FILE, 'exec'), ns)
    return (
        ns.get('JOB', {}),
        ns.get('MODULOS', {}),
        ns.get('PATHS', {}),
    )


@app.route('/api/settings', methods=['GET'])
def get_settings():
    try:
        job, modulos, paths = _read_settings_raw()
        return jsonify({'job': job, 'modulos': modulos, 'paths': paths})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/settings', methods=['POST'])
def save_settings():
    """Rewrite config/settings.py with updated JOB and MODULOS."""
    try:
        data = request.get_json(force=True)
        new_job = data.get('job', {})
        new_modulos = data.get('modulos', {})

        # Read current PATHS to preserve them
        _, _, current_paths = _read_settings_raw()

        # Build new file
        lines = []
        lines.append('# --- MAPEAMENTO MANUAL DE CAMINHOS ---')
        lines.append('JOB = {')
        lines.append(f'    "nome_projeto": {json.dumps(new_job.get("nome_projeto", ""), ensure_ascii=False)},')
        lines.append(f'    ')
        lines.append(f'    # Raízes AWS')
        lines.append(f'    "s3_capa_root": {json.dumps(new_job.get("s3_capa_root", ""), ensure_ascii=False)},')
        lines.append(f'    "s3_miolo_root": {json.dumps(new_job.get("s3_miolo_root", ""), ensure_ascii=False)},')
        lines.append(f'    # Bucket final para upload de saída (defina como s3://seu-bucket/Finalizados/)')
        lines.append(f'    "s3_final_root": {json.dumps(new_job.get("s3_final_root", ""), ensure_ascii=False)},')
        lines.append(f'    ')
        lines.append(f'    # Raízes VPN/Local (Agora com Originais e Metabooks explícitos)')
        lines.append(f'    "vpn_apoio_root": r"{new_job.get("vpn_apoio_root", "")}",')
        lines.append(f'    "vpn_originais": r"{new_job.get("vpn_originais", "")}",')
        lines.append(f'    "vpn_web_epub":  r"{new_job.get("vpn_web_epub", "")}",')
        lines.append(f'    "vpn_metabooks": r"{new_job.get("vpn_metabooks", "")}"')
        lines.append('}')
        lines.append('')
        lines.append('# Flags de ativação de módulos')
        lines.append('MODULOS = {')
        lines.append(f'    "aws_input": {new_modulos.get("aws_input", True)},')
        lines.append(f'    "vpn_sync": {new_modulos.get("vpn_sync", True)},')
        lines.append(f'    "indesign_parser": {new_modulos.get("indesign_parser", True)},')
        lines.append(f'    "ai_agent": {new_modulos.get("ai_agent", True)},')
        lines.append(f'    "aws_output": {new_modulos.get("aws_output", True)}')
        lines.append('}')
        lines.append('')
        lines.append('# Caminhos de pastas persistentes')
        lines.append('PATHS = {')
        lines.append(f'    "temp_local": {json.dumps(current_paths.get("temp_local", "./temp"), ensure_ascii=False)},')
        lines.append(f'    "lm_studio_url": {json.dumps(current_paths.get("lm_studio_url", "http://192.168.28.70:1234/v1"), ensure_ascii=False)}')
        lines.append('}')
        lines.append('')

        content = '\r\n'.join(lines)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# API — PROCESS CONTROL
# ═══════════════════════════════════════════════════════════════════
def _broadcast(msg_dict):
    """Send a message to all connected SSE clients."""
    data = json.dumps(msg_dict, ensure_ascii=False)
    with _queues_lock:
        for q in _log_queues:
            try:
                q.put_nowait(data)
            except queue.Full:
                pass  # drop if client is too slow


def _reader_thread(pipe, name):
    """Read lines from subprocess pipe and broadcast."""
    try:
        for raw_line in iter(pipe.readline, ''):
            line = raw_line.rstrip('\r\n')
            if line:
                _broadcast({'type': 'log', 'text': line})
    except Exception:
        pass
    finally:
        pipe.close()


def _waiter_thread(proc):
    """Wait for process to end, then broadcast done."""
    global _process
    try:
        proc.wait()
        _broadcast({'type': 'done', 'text': f'Processo finalizado (código {proc.returncode})'})
    except Exception as e:
        _broadcast({'type': 'error', 'text': str(e)})
    finally:
        with _process_lock:
            _process = None


@app.route('/api/run', methods=['POST'])
def run_process():
    global _process
    with _process_lock:
        if _process is not None and _process.poll() is None:
            return jsonify({'error': 'Processo já em execução'}), 409

    try:
        python_exe = sys.executable
        proc = subprocess.Popen(
            [python_exe, '-u', os.path.join(BASE_DIR, 'main.py')],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=BASE_DIR,
            env={**os.environ, 'PYTHONUNBUFFERED': '1'},
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
        )

        with _process_lock:
            _process = proc

        # Reader thread for stdout
        t_out = threading.Thread(target=_reader_thread, args=(proc.stdout, 'stdout'), daemon=True)
        t_out.start()

        # Waiter thread
        t_wait = threading.Thread(target=_waiter_thread, args=(proc,), daemon=True)
        t_wait.start()

        return jsonify({'ok': True, 'pid': proc.pid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stop', methods=['POST'])
def stop_process():
    global _process
    with _process_lock:
        if _process is None or _process.poll() is not None:
            return jsonify({'ok': True, 'msg': 'Nenhum processo em execução'})
        try:
            if os.name == 'nt':
                _process.terminate()
            else:
                os.killpg(os.getpgid(_process.pid), signal.SIGTERM)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'ok': True})


@app.route('/api/input', methods=['POST'])
def send_input():
    """Send text input to the running subprocess stdin (e.g. upload confirmation)."""
    global _process
    with _process_lock:
        if _process is None or _process.poll() is not None:
            return jsonify({'error': 'Nenhum processo em execução'}), 404
        try:
            text = request.get_json(force=True).get('text', '')
            _process.stdin.write(text + '\n')
            _process.stdin.flush()
            return jsonify({'ok': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/stream')
def stream():
    """SSE endpoint — clients connect here to receive logs in real-time."""
    q = queue.Queue(maxsize=500)
    with _queues_lock:
        _log_queues.append(q)

    def generate():
        try:
            while True:
                try:
                    data = q.get(timeout=30)
                    yield f"data: {data}\n\n"
                except queue.Empty:
                    # Send keepalive
                    yield ": keepalive\n\n"
        except GeneratorExit:
            pass
        finally:
            with _queues_lock:
                if q in _log_queues:
                    _log_queues.remove(q)

    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive',
        }
    )


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("═" * 50)
    print("  depósito — interface web")
    print("  http://localhost:5000")
    print("═" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
