# pack_go.py: 从 dsh-purge-Go版 复刻 npm pack 形态的 tgz（package/ 前缀，文件条目，mode 0o666）
import os, tarfile, json, hashlib, sys

SRC = r"D:/09_成果输出/DSH成果/05-DSH与AI工具链/dsh-purge-Go版"
DIST = r"D:/09_成果输出/DSH成果/05-DSH与AI工具链/dsh-purge-Go版/dist"
MTIME = 1794328979
EXCLUDE_DIRS = {".git", "dist", "node_modules", "__pycache__"}
EXCLUDE_FILES = {"src.tgz", ".DS_Store", "Thumbs.db"}

pkg = json.loads(open(os.path.join(SRC, "package.json"), encoding="utf-8").read())
ver = pkg["version"]
OUT = os.path.join(DIST, f"dsh-purge-{ver}.tgz")

entries = []
for dp, dns, fns in os.walk(SRC):
    dns[:] = sorted(d for d in dns if d not in EXCLUDE_DIRS)
    for f in sorted(fns):
        if f in EXCLUDE_FILES:
            print("exclude", f); continue
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, SRC).replace(os.sep, "/")
        entries.append(("package/" + rel, full))
entries.sort()

os.makedirs(DIST, exist_ok=True)
with tarfile.open(OUT, "w:gz", format=tarfile.GNU_FORMAT, compresslevel=9) as t:
    for name, full in entries:
        ti = tarfile.TarInfo(name)
        st = os.stat(full)
        ti.size = st.st_size; ti.mode = 0o666; ti.mtime = MTIME
        ti.uid = ti.gid = 0; ti.uname = ti.gname = "root"; ti.type = tarfile.REGTYPE
        with open(full, "rb") as fh:
            t.addfile(ti, fh)

h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
size = os.path.getsize(OUT)
with tarfile.open(OUT, "r:gz") as t:
    ms = t.getmembers()
print(json.dumps({"out": OUT, "bytes": size, "sha256": h, "version": ver,
                  "entries": len(ms), "dirs": sum(1 for m in ms if m.isdir()),
                  "nonfile": sum(1 for m in ms if not m.isfile()),
                  "sample": [m.name for m in ms[:3]]}, ensure_ascii=False))
open(os.path.join(DIST, "SHA256SUMS"), "w", encoding="utf-8", newline="\n").write(h + "  dsh-purge-" + ver + ".tgz\n")
print("SHA256SUMS written")