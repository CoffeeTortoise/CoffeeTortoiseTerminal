import subprocess as sp
from config import Config
from constants import EXIT_ERR_STR, EXIT_STR


def run_command(command: str) -> tuple[str, ...]:
    try:
        res: sp.CompletedProcess[str] = sp.run(
            command,
            capture_output=True,
            check=True,
            text=True,
            shell=True,
            encoding=Config.OUTPUT_ENCODING)
        out: str = f'Res:\n{res.stdout}'
        return out, EXIT_STR
    except sp.CalledProcessError as e:
         return f'An error occurred:\n{e}\n{e.stderr}', EXIT_ERR_STR
    except PermissionError as e:
        return f'Not enough rights to run {command}!\n{e}', EXIT_ERR_STR
    except OSError as e:
        return f'General error:\n{e}', EXIT_ERR_STR
    except UnicodeDecodeError as e:
        return f'Decoding error!\n{e}', EXIT_ERR_STR
    except UnicodeEncodeError as e:
        return f'Encoding error!\n{e}', EXIT_ERR_STR
    except UnicodeError as e:
        return f'Some unicode error occurred!\n{e}', EXIT_ERR_STR
    except LookupError as e:
        return f'Access error!\n{e}', EXIT_ERR_STR
    except Exception as e:
        return f'Something went wrong:\n{e}', EXIT_ERR_STR
