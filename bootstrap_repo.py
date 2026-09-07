import hashlib
import json
import pathlib
import shutil
import subprocess
import zlib

EXPECTED_HEX_LEN = 47774
EXPECTED_SHA256 = "9ac3b744ed81135a22ce25e9524771b475bec6b5e161efc7f9c5ec8f91a0dc46"
PART_COUNT = 14


def run(*args):
    subprocess.run(args, check=True)


def main():
    parts = []
    for i in range(1, PART_COUNT + 1):
        p = pathlib.Path(f".bootstrap_payload/part_{i:02d}.txt")
        parts.append(p.read_text(encoding="utf-8").strip())
    payload_hex = "".join(parts)
    if len(payload_hex) != EXPECTED_HEX_LEN:
        raise RuntimeError(f"Expected payload length {EXPECTED_HEX_LEN}, found {len(payload_hex)}")
    compressed = bytes.fromhex(payload_hex)
    digest = hashlib.sha256(compressed).hexdigest()
    if digest != EXPECTED_SHA256:
        raise RuntimeError(f"Payload hash mismatch: {digest}")
    files = json.loads(zlib.decompress(compressed).decode("utf-8"))
    for path, content in files.items():
        target = pathlib.Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    shutil.rmtree(".bootstrap_payload")
    pathlib.Path("bootstrap_repo.py").unlink()
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run("git", "add", "-A")
    run("git", "commit", "-m", "Add automatic formal verification CPS research framework")
    run("git", "push", "origin", "HEAD:main")


if __name__ == "__main__":
    main()
