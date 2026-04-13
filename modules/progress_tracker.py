import time
import os
import sys

class ProgressTracker:
    PHASES = ["Coletando arquivos", "Enviando para S3"]
    
    def __init__(self):
        self.phase = 0
        self.current = 0
        self.total = 0
        self.speed_bps = 0
        self.errors = []
        self.missing_files = []
        self._start_time = None
        self._bytes_total = 0
        self._phase_errors = []
        self._is_tty = sys.stdout.isatty()
        self._last_progress_print = 0
    
    def start_phase(self, phase_idx, total_files):
        self.phase = phase_idx
        self.current = 0
        self.total = total_files
        self._start_time = time.time()
        self._bytes_total = 0
        self._phase_errors = []
        self.speed_bps = 0
        self._print_state()
    
    def add_total(self, count):
        """Increment total by count. Called by transfer functions when they know exact file count."""
        self.total += count
        self._print_state()
    
    def update(self, bytes_transferred=0, file_path=None):
        self.current += 1
        self._bytes_total += bytes_transferred
        elapsed = time.time() - self._start_time
        if elapsed > 0:
            self.speed_bps = self._bytes_total / elapsed
        else:
            self.speed_bps = 0
        
        if self._is_tty:
            now = time.time()
            if now - self._last_progress_print >= 0.5 or self.current >= self.total:
                self._print_progress_bar()
                self._last_progress_print = now
        else:
            self._print_state()
    
    def log_file(self, filename, source_path, dest_path=None):
        """Print current file being processed (indented below progress bar)."""
        if dest_path:
            print(f"   → {filename} from {source_path} → {dest_path}", flush=True)
        else:
            print(f"   → {filename} from {source_path}", flush=True)
    
    def _print_progress_bar(self):
        if self.total <= 0:
            return
        pct = self.current / self.total
        bar_len = 30
        filled = int(bar_len * pct)
        bar = '█' * filled + '░' * (bar_len - filled)
        speed_str = self._format_speed(self.speed_bps)
        phase_name = self.PHASES[self.phase]
        print(f"\r{phase_name} [{bar}] {self.current}/{self.total} {speed_str}", end='', flush=True)
        if self.current >= self.total:
            print()
    
    def _print_state(self):
        speed_str = self._format_speed(self.speed_bps)
        msg = f"[PROGRESS] phase={self.phase} current={self.current} total={self.total} speed={speed_str}"
        print(msg, flush=True)
    
    def _format_speed(self, bps):
        if bps >= 1024 * 1024:
            return f"{bps / (1024 * 1024):.1f} MB/s"
        elif bps >= 1024:
            return f"{bps / 1024:.1f} KB/s"
        return f"{bps:.0f} B/s"
    
    def add_error(self, message):
        err_entry = {"phase": self.phase, "message": message}
        self.errors.append(err_entry)
        self._phase_errors.append(err_entry)
        print(f"[ERROR] phase={self.phase} {message}", flush=True)
    
    def add_missing_file(self, path):
        self.missing_files.append(path)
        print(f"[MISSING_FILE] {path}", flush=True)
    
    def finish_phase(self):
        print(f"[PHASE_COMPLETE] phase={self.phase}", flush=True)
        
        if self._phase_errors:
            print(f"[ERROR_CARD] phase={self.phase} count={len(self._phase_errors)}", flush=True)
            for err in self._phase_errors:
                print(f"[ERROR_ITEM] [{self.PHASES[self.phase]}] {err['message']}", flush=True)
            print("[ERROR_CARD_END]", flush=True)
        
        if self.missing_files and self.phase == 0:
            print(f"[MISSING_FILES_CARD] count={len(self.missing_files)}", flush=True)
            for f in self.missing_files:
                print(f"[MISSING_FILE_ITEM] {f}", flush=True)
            print("[MISSING_FILES_CARD_END]", flush=True)
        
        return {
            "phase": self.phase,
            "errors": self._phase_errors,
            "missing_files": self.missing_files if self.phase == 0 else []
        }
    
    def get_state(self):
        speed_str = self._format_speed(self.speed_bps)
        return {
            "type": "progress",
            "phase": self.phase,
            "phase_name": self.PHASES[self.phase],
            "current": self.current,
            "total": self.total,
            "speed_bps": self.speed_bps,
            "speed_display": speed_str
        }
    
    def get_phase_data(self):
        return {
            "phase": self.phase,
            "errors": self._phase_errors,
            "missing_files": self.missing_files if self.phase == 0 else []
        }