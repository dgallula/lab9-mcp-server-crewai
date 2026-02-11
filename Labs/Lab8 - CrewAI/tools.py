from crewai.tools import tool
import subprocess
import sys
import tempfile
import pandas as pd


@tool("repl")
def repl(code: str) -> str:
	"""Execute Python code in a subprocess and return stdout or stderr."""
	try:
		with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8') as tf:
			tf.write(code)
			tf_name = tf.name
		proc = subprocess.run([sys.executable, tf_name], capture_output=True, text=True, timeout=30)
		if proc.returncode == 0:
			return proc.stdout
		return proc.stderr or f"Process exited with code {proc.returncode}"
	except Exception as e:
		return f"Error: {e}"


@tool("file_read")
def file_read(path: str) -> str:
	"""Read a text file from disk and return its contents."""
	try:
		with open(path, 'r', encoding='utf-8') as f:
			return f.read()
	except Exception as e:
		return f"Error: {e}"


file_read_tool = file_read

