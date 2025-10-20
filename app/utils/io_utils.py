import io, contextlib

def capture_stdout(code: str, globals_dict=None) -> str:
    stdout = io.StringIO()
    globals_dict = globals_dict or {"__name__": "__main__"}
    with contextlib.redirect_stdout(stdout):
        try:
            exec(code, globals_dict)
        except Exception as e:
            return f"❌ Error executing script: {str(e)}"
    return stdout.getvalue()
