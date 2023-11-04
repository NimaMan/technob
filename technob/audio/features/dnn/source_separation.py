
import io
from pathlib import Path
import select
from shutil import rmtree
import subprocess as sp
import sys
from typing import Dict, Tuple, Optional, IO


def find_files(in_path):
    """
    Recursively finds all files with the specified extensions in the given directory and its subdirectories.

    Args:
        in_path: A string representing the path to the directory to search.

    Returns:
        A list of `Path` objects representing the files found.

    Raises:
        None.
    """
    out = []
    for file in Path(in_path).rglob("*"):
        if file.is_file() and file.suffix.lower().lstrip(".") in extensions:
            out.append(file)
    return out


def copy_process_streams(process: sp.Popen):
    """
    Copies the output streams of a subprocess to the standard output and error streams of the parent process.

    Args:
        process: A `subprocess.Popen` object representing the subprocess to copy the streams from.

    Returns:
        None.

    Raises:
        None.

    Example:
        >>> process = subprocess.Popen(["ls", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        >>> copy_process_streams(process)
        total 0
        drwxr-xr-x  2 user  staff  64 Mar  1 14:30 dir1
        drwxr-xr-x  2 user  staff  64 Mar  1 14:30 dir2
        -rw-r--r--  1 user  staff   0 Mar  1 14:30 file1.txt
        -rw-r--r--  1 user  staff   0 Mar  1 14:30 file2.txt
    """
    def raw(stream: Optional[IO[bytes]]) -> IO[bytes]:
        assert stream is not None
        if isinstance(stream, io.BufferedIOBase):
            stream = stream.raw
        return stream

    p_stdout, p_stderr = raw(process.stdout), raw(process.stderr)
    stream_by_fd: Dict[int, Tuple[IO[bytes], io.StringIO, IO[str]]] = {
        p_stdout.fileno(): (p_stdout, sys.stdout),
        p_stderr.fileno(): (p_stderr, sys.stderr),
    }
    fds = list(stream_by_fd.keys())

    while fds:
        # `select` syscall will wait until one of the file descriptors has content.
        ready, _, _ = select.select(fds, [], [])
        for fd in ready:
            p_stream, std = stream_by_fd[fd]
            raw_buf = p_stream.read(2 ** 16)
            if not raw_buf:
                fds.remove(fd)
                continue
            buf = raw_buf.decode()
            std.write(buf)
            std.flush()


def separate_stems(input_dir=None, out_dir=None):
    cmd = ["python3", "-m", "demucs.separate", "-o", str(out_dir), "-n", model]
    if mp3:
        cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]
    if float32:
        cmd += ["--float32"]
    if int24:
        cmd += ["--int24"]
    if two_stems is not None:
        cmd += [f"--two-stems={two_stems}"]
    files = [str(f) for f in find_files(input_dir)]
    if not files:
        print(f"No valid audio files in {input_dir}")
        return
    print("Going to separate the files:")
    print('\n'.join(files))
    print("With command: ", " ".join(cmd))
    p = sp.Popen(cmd + files, stdout=sp.PIPE, stderr=sp.PIPE)
    copy_process_streams(p)
    p.wait()
    if p.returncode != 0:
        print("Command failed, something went wrong.")


if __name__ == "__main__":
    # Example usage
    # Customize the following options!
    model = "htdemucs_6s"
    extensions = ["mp3", "wav", "ogg", "flac"]  # we will look for all those file types.
    two_stems = None   # only separate one stems from the rest, for instance
    # two_stems = "vocals"

    # Options for the output audio.
    mp3 = False
    mp3_rate = 320
    float32 = True  # output as float 32 wavs, unsused if 'mp3' is True.
    int24 = False    # output as int24 wavs, unused if 'mp3' is True.
    out_dir = "/Users/nimamanaf/Desktop/Music/stems"
    input_dir = '/Users/nimamanaf/Desktop/Music/99'
    separate_stems(input_dir, out_dir)