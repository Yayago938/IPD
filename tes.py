#!/usr/bin/env python3
"""
winfile_classifier_gui.py  –  WizTree-style interactive folder classifier
Light mode, clean professional UI.
"""

import os
import csv
import ctypes
import queue
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from collections import defaultdict

try:
    import win32api
    HAVE_WIN32 = True
except ImportError:
    HAVE_WIN32 = False

# ---------------------------------------------------------------------------
# Classification constants
# ---------------------------------------------------------------------------

ZONE_OS           = "WINDOWS / OS"
ZONE_APP          = "APPLICATIONS"
ZONE_USER         = "USER DATA"
ZONE_USER_APPDATA = "USER APP DATA"
SAFE_ZONES        = {ZONE_APP, ZONE_USER, ZONE_USER_APPDATA}

ZONE_BADGE = {
    ZONE_OS:           "OS",
    ZONE_APP:          "APP",
    ZONE_USER:         "USER",
    ZONE_USER_APPDATA: "APPDATA",
}

OS_TOP_LEVEL_PREFIXES = [
    r"C:\Windows", r"C:\Recovery", r"C:\System Volume Information",
    r"C:\$Recycle.Bin", r"C:\$WinREAgent", r"C:\Boot",
    r"C:\PerfLogs", r"C:\Documents and Settings", r"C:\MSOCache",
    r"C:\Config.Msi", r"C:\inetpub", r"C:\Windows.old",
]
OS_ROOT_FILES = {"pagefile.sys", "hiberfil.sys", "swapfile.sys", "bootmgr", "bootnxt"}
# NOTE: ProgramData is intentionally NOT in here — it's a mix of OS-critical
# data (Defender, package cache, driver install state) and pure third-party
# app leftovers. It gets its own gated check in classify_path() below instead
# of being blanket-marked APP/safe-to-delete.
APP_TOP_LEVEL_PREFIXES = [r"C:\Program Files", r"C:\Program Files (x86)"]
PROGRAMDATA_PREFIX = r"C:\ProgramData"
# Subfolders directly under ProgramData that hold OS/platform-critical state.
# Anything else under ProgramData is treated as ordinary (deletable) app data.
PROGRAMDATA_OS_SUBFOLDERS = {"microsoft", "package cache", "packages"}
USER_PERSONAL_SUBFOLDERS = {
    "desktop","documents","downloads","pictures","videos","music",
    "favorites","links","saved games","contacts","onedrive","3d objects","searches",
}
# Per-user registry hive files — these can appear directly under the profile
# root (NTUSER.DAT*) or nested inside AppData (UsrClass.dat, under
# AppData\Local\Microsoft\Windows\). Matched by filename anywhere in the
# profile tree, not just at a fixed depth.
PROFILE_SYSTEM_FILE_PREFIXES = ("ntuser.dat", "ntuser.ini", "ntuser.pol", "usrclass.dat")
PERSONAL_CONTENT_EXTENSIONS = {
    ".jpg",".jpeg",".png",".gif",".bmp",".heic",".webp",".raw",
    ".mp4",".mov",".avi",".mkv",".wmv",".m4v",
    ".mp3",".wav",".flac",".aac",".m4a",
    ".doc",".docx",".xls",".xlsx",".ppt",".pptx",".pdf",".odt",".txt",
    ".zip",".rar",".7z",".psd",".ai",".heif",
}
EXECUTABLE_EXTENSIONS = {
    ".exe",".dll",".sys",".drv",".ocx",".cpl",
    ".msi",".msp",".msu",".efi",".scr",".com",".cat",
}
APP_ROOT_MARKERS = [
    "c:\\program files\\","c:\\program files (x86)\\","c:\\programdata\\",
]

# ---------------------------------------------------------------------------
# Light-mode colour palette
# ---------------------------------------------------------------------------

# Backgrounds
C_WIN_BG     = "#f0f0f0"   # window / outer
C_TOOLBAR_BG = "#ffffff"   # top toolbar strip
C_HEADER_BG  = "#e8eaf0"   # column header
C_ROW_ODD    = "#ffffff"
C_ROW_EVEN   = "#f7f8fa"
C_ROW_HOVER  = "#e8f0fe"
C_ROW_SEL    = "#d2e3fc"
C_BORDER     = "#d0d3dc"
C_DIVIDER    = "#e0e2ea"

# Text
C_TEXT       = "#1a1a2e"
C_SUBTEXT    = "#6b6f85"
C_HDR_TEXT   = "#3a3d52"

# Zone colours  (badge pill background / bar fill)
C_OS         = "#e53935"   # red
C_OS_BG      = "#fde8e8"
C_APP        = "#1e88e5"   # blue
C_APP_BG     = "#e3f0fd"
C_USER       = "#2e7d32"   # green
C_USER_BG    = "#e6f4ea"
C_APPDATA    = "#f57c00"   # amber
C_APPDATA_BG = "#fff3e0"
C_FLAGGED    = "#e65100"
C_FLAGGED_BG = "#fff8e1"

# Accent / buttons
C_ACCENT     = "#1a73e8"
C_ACCENT_HOV = "#1557b0"
C_BTN_BG     = "#1a73e8"
C_BTN_FG     = "#ffffff"
C_BTN_SEC    = "#f1f3f4"
C_BTN_SEC_FG = "#3c4043"

ZONE_FG = {ZONE_OS: C_OS, ZONE_APP: C_APP, ZONE_USER: C_USER, ZONE_USER_APPDATA: C_APPDATA}
ZONE_PILL_BG = {ZONE_OS: C_OS_BG, ZONE_APP: C_APP_BG, ZONE_USER: C_USER_BG, ZONE_USER_APPDATA: C_APPDATA_BG}

# Bar colours
C_BAR_TRACK  = "#e0e2ea"
C_BAR_SAFE   = "#34a853"
C_BAR_UNSAFE = "#ea4335"

# Fonts  (Segoe UI is native on Windows; falls back gracefully)
F_UI    = ("Segoe UI", 9)
F_BOLD  = ("Segoe UI", 9, "bold")
F_SMALL = ("Segoe UI", 8)
F_HDR   = ("Segoe UI", 9, "bold")
F_TITLE = ("Segoe UI", 11, "bold")

ROW_H      = 22
HEADER_H   = 28
INDENT_PX  = 16
BAR_PAD    = 6     # vertical padding inside bar cell
PILL_H     = 14
PILL_R     = 4     # pill corner radius

COL_DEFS = [
    # (id,           label,           min_w, fixed_w, anchor)
    ("name",         "Folder / File", 300,   None,    "w"),
    ("pct",          "% of Parent",   160,   160,     "w"),
    ("size",         "Size",           80,    80,     "e"),
    ("total_files",  "Files",          60,    60,     "e"),
    ("safe_files",   "Safe to Delete", 90,    90,     "e"),
    ("safe_pct",     "Safe %",         60,    60,     "e"),
    ("zone",         "Zone",          100,   100,     "w"),
]

# ---------------------------------------------------------------------------
# Classification logic
# ---------------------------------------------------------------------------

def classify_path(filepath):
    try:
        resolved = str(Path(filepath).resolve())
    except OSError:
        resolved = filepath
    low = resolved.lower()
    for p in OS_TOP_LEVEL_PREFIXES:
        if low.startswith(p.lower()):
            return ZONE_OS
    for p in APP_TOP_LEVEL_PREFIXES:
        if low.startswith(p.lower()):
            return ZONE_APP
    if low.startswith(PROGRAMDATA_PREFIX.lower()):
        rel = resolved[len(PROGRAMDATA_PREFIX):].lstrip(os.sep)
        rp  = rel.split(os.sep) if rel else []
        if not rp or not rp[0]:
            # loose files directly in ProgramData root — be conservative
            return ZONE_OS
        if rp[0].lower() in PROGRAMDATA_OS_SUBFOLDERS:
            return ZONE_OS
        return ZONE_APP
    parts = resolved.split(os.sep)
    if len(parts) == 2 and parts[1].lower() in OS_ROOT_FILES:
        return ZONE_OS
    idx = low.find("c:\\users\\")
    if idx == 0:
        rel   = resolved[len("C:\\Users\\"):]
        rp    = rel.split(os.sep)
        if not rp:              return ZONE_USER
        if rp[0].lower() == "public": return ZONE_USER
        # Registry hive files can live at the profile root (NTUSER.DAT) or
        # nested inside AppData (UsrClass.dat) — check filename anywhere.
        filename = rp[-1].lower()
        if any(filename.startswith(p) for p in PROFILE_SYSTEM_FILE_PREFIXES):
            return ZONE_OS
        if len(rp) < 2:        return ZONE_USER
        second = rp[1].lower()
        if second == "appdata":
            if len(rp) >= 3 and rp[2].lower() == "local":
                if len(rp) >= 4 and rp[3].lower() == "programs":
                    return ZONE_APP
            return ZONE_USER_APPDATA
        if second in USER_PERSONAL_SUBFOLDERS:
            return ZONE_USER
        return ZONE_USER
    return ZONE_USER


def check_anomaly(filepath, zone):
    if zone not in (ZONE_OS, ZONE_APP):
        return ""
    ext = Path(filepath).suffix.lower()
    if ext in PERSONAL_CONTENT_EXTENSIONS:
        return (f"Personal-content file ({ext}) inside "
                f"{'OS' if zone == ZONE_OS else 'application'} folder — check manually")
    return ""


def get_file_version_info(filepath):
    if not HAVE_WIN32:
        return {}
    try:
        tr = win32api.GetFileVersionInfo(filepath, r"\VarFileInfo\Translation")
        lang, cp = tr[0]
        base = f"\\StringFileInfo\\{lang:04x}{cp:04x}\\%s"
        return {k: win32api.GetFileVersionInfo(filepath, base % k)
                for k in ("CompanyName","ProductName")}
    except Exception:
        return {}


def get_folder_hint(filepath, zone):
    try:
        resolved = str(Path(filepath).resolve())
    except OSError:
        resolved = filepath
    low = resolved.lower()
    if zone == ZONE_APP:
        for m in APP_ROOT_MARKERS:
            if low.startswith(m):
                parts = resolved[len(m):].split(os.sep)
                if parts and parts[0]: return parts[0]
        idx = low.find("appdata\\local\\programs\\")
        if idx != -1:
            parts = resolved[idx+len("appdata\\local\\programs\\"):].split(os.sep)
            if parts and parts[0]: return parts[0]
    if zone == ZONE_USER_APPDATA:
        for m in ("appdata\\roaming\\","appdata\\local\\","appdata\\locallow\\"):
            idx = low.find(m)
            if idx != -1:
                parts = resolved[idx+len(m):].split(os.sep)
                if parts and parts[0]: return parts[0]
    return ""


def get_source(filepath, zone, ext):
    if ext in EXECUTABLE_EXTENSIONS:
        info = get_file_version_info(filepath)
        co   = info.get("CompanyName")
        if co: return co
    hint = get_folder_hint(filepath, zone)
    if hint: return f"{hint} (folder)"
    if zone == ZONE_OS: return "Microsoft (Windows)"
    return ""


FILE_ATTRIBUTE_REPARSE_POINT = 0x400
INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF


def is_reparse_point(path):
    """True for NTFS junctions/symlinks (e.g. C:\\Documents and Settings,
    per-user 'Application Data' aliases). os.walk doesn't skip these on its
    own, so without this check the scanner can double-count the same files
    through two different paths, or wander back into an excluded tree via
    an alias that isn't itself in OS_TOP_LEVEL_PREFIXES."""
    if os.name != "nt":
        return False
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        if attrs == INVALID_FILE_ATTRIBUTES:
            return False
        return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
    except Exception:
        return False


def human_size(n):
    for u in ("B","KB","MB","GB","TB"):
        if n < 1024:
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} PB"


# ---------------------------------------------------------------------------
# Folder node
# ---------------------------------------------------------------------------

class FolderNode:
    __slots__ = ("path","name","parent","total_size","total_files",
                 "safe_files","safe_size","children","file_results",
                 "zone_counts","expanded")
    def __init__(self, path, parent=None):
        self.path        = path
        self.name        = os.path.basename(path) or path
        self.parent      = parent
        self.total_size  = 0
        self.total_files = 0
        self.safe_files  = 0
        self.safe_size   = 0
        self.zone_counts = defaultdict(int)
        self.children    = {}
        self.file_results = []
        self.expanded    = False


def build_folder_tree(results):
    root = FolderNode("__root__")
    nodes = {"__root__": root}

    def get_or_create(fp):
        if fp in nodes: return nodes[fp]
        pp = str(Path(fp).parent)
        par = root if pp == fp else get_or_create(pp)
        n = FolderNode(fp, par)
        nodes[fp] = n
        par.children[n.name] = n
        return n

    for r in results:
        get_or_create(str(Path(r["path"]).parent)).file_results.append(r)

    def roll(n):
        n.total_size  = sum(f["size"] for f in n.file_results)
        n.total_files = len(n.file_results)
        n.safe_files  = sum(1 for f in n.file_results if f["zone"] in SAFE_ZONES)
        n.safe_size   = sum(f["size"] for f in n.file_results if f["zone"] in SAFE_ZONES)
        for z in (ZONE_OS, ZONE_APP, ZONE_USER, ZONE_USER_APPDATA):
            n.zone_counts[z] = sum(1 for f in n.file_results if f["zone"] == z)
        for c in n.children.values():
            roll(c)
            n.total_size  += c.total_size
            n.total_files += c.total_files
            n.safe_files  += c.safe_files
            n.safe_size   += c.safe_size
            for z in (ZONE_OS, ZONE_APP, ZONE_USER, ZONE_USER_APPDATA):
                n.zone_counts[z] += c.zone_counts[z]

    roll(root)
    return root


# ---------------------------------------------------------------------------
# Canvas tree widget
# ---------------------------------------------------------------------------

class WizTree(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, bg=C_WIN_BG, **kw)
        self._rows       = []
        self._root_node  = None
        self._filter     = "All"
        self._sort_col   = "size"
        self._sort_desc  = True
        self._hover      = -1
        self._sel        = -1
        self._build()

    # ── build ──────────────────────────────────────────────────────────
    def _build(self):
        # Header
        self.hdr = tk.Canvas(self, height=HEADER_H, bg=C_HEADER_BG,
                             highlightthickness=0)
        self.hdr.pack(fill="x")
        self.hdr.bind("<Button-1>", self._hdr_click)
        self.hdr.bind("<Motion>",   self._hdr_motion)
        self.hdr.bind("<Leave>",    lambda e: self.hdr.config(cursor=""))

        # Body
        body = tk.Frame(self, bg=C_WIN_BG)
        body.pack(fill="both", expand=True)

        self.cv  = tk.Canvas(body, bg=C_ROW_ODD, highlightthickness=0,
                             bd=0)
        self.vsb = ttk.Scrollbar(body, orient="vertical",
                                 command=self._vscroll)
        self.cv.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.cv.pack(side="left",  fill="both", expand=True)

        self.cv.bind("<Configure>",        self._resize)
        self.cv.bind("<Button-1>",         self._click)
        self.cv.bind("<Double-Button-1>",  self._dbl)
        self.cv.bind("<Motion>",           self._motion)
        self.cv.bind("<Leave>",            lambda e: self._set_hover(-1))
        self.cv.bind("<MouseWheel>",       self._wheel)

    # ── public ─────────────────────────────────────────────────────────
    def load(self, root_node, filter_val="All"):
        self._root_node = root_node
        self._filter    = filter_val
        self._sel       = -1
        self._flatten()
        self._draw()

    def set_filter(self, val):
        self._filter = val
        if self._root_node:
            self._flatten()
            self._draw()

    # ── layout helpers ─────────────────────────────────────────────────
    def _col_layout(self):
        """Return list of (x, w) per column. Name column takes remaining space."""
        W = self.cv.winfo_width() or 900
        fixed = sum(c[3] for c in COL_DEFS if c[3] is not None)
        name_w = max(220, W - fixed - 16)
        xs, x = [], 0
        for cid, lbl, minw, fw, anc in COL_DEFS:
            w = name_w if cid == "name" else fw
            xs.append((x, w))
            x += w
        return xs

    # ── header ─────────────────────────────────────────────────────────
    def _draw_header(self):
        self.hdr.delete("all")
        W = self.cv.winfo_width() or 900
        self.hdr.configure(width=W)
        cols = self._col_layout()
        h    = HEADER_H

        # outer border bottom
        self.hdr.create_line(0, h-1, W, h-1, fill=C_BORDER)

        for i, (cid, lbl, _, _, anc) in enumerate(COL_DEFS):
            x0, cw = cols[i]
            # divider
            if i > 0:
                self.hdr.create_line(x0, 4, x0, h-4, fill=C_BORDER)
            # active sort highlight
            if cid == self._sort_col:
                self.hdr.create_rectangle(x0, 0, x0+cw, h-1,
                                          fill="#dde2f0", outline="")
            # text + arrow
            arrow = (" ▼" if self._sort_desc else " ▲") if cid == self._sort_col else ""
            tx = x0 + 8 if anc == "w" else x0 + cw - 8
            self.hdr.create_text(tx, h//2, text=lbl+arrow, fill=C_HDR_TEXT,
                                 font=F_HDR, anchor=anc)

    # ── flatten rows ────────────────────────────────────────────────────
    def _flatten(self):
        self._rows = []
        if self._root_node and self._root_node.path == "__root__":
            for ch in self._sorted_children(self._root_node):
                self._walk(ch, 0, self._root_node.total_size or 1)

    def _walk(self, node, depth, parent_sz):
        pct = (node.total_size / parent_sz * 100) if parent_sz else 0
        self._rows.append({"kind": "folder", "node": node,
                            "depth": depth, "pct": pct})
        if node.expanded:
            for ch in self._sorted_children(node):
                self._walk(ch, depth+1, node.total_size or 1)
            for f in self._filtered_files(node):
                fpct = (f["size"] / node.total_size * 100) if node.total_size else 0
                self._rows.append({"kind": "file", "result": f,
                                   "depth": depth+1, "pct": fpct})

    def _sorted_children(self, node):
        key = {
            "size":       lambda n: n.total_size,
            "total_files":lambda n: n.total_files,
            "safe_files": lambda n: n.safe_files,
            "safe_pct":   lambda n: (n.safe_files/n.total_files) if n.total_files else 0,
            "name":       lambda n: n.name.lower(),
        }.get(self._sort_col, lambda n: n.total_size)
        return sorted(node.children.values(), key=key, reverse=self._sort_desc)

    def _filtered_files(self, node):
        f = self._filter
        r = node.file_results
        if f == "All":           return r
        if f == "Flagged only":  return [x for x in r if x["anomaly"]]
        if f == "Safe only":     return [x for x in r if x["zone"] in SAFE_ZONES]
        return [x for x in r if x["zone"] == f]

    # ── draw ────────────────────────────────────────────────────────────
    def _draw(self):
        self.cv.delete("all")
        if not self._rows:
            self.cv.create_text(20, 30, anchor="w", fill=C_SUBTEXT, font=F_UI,
                text="No results yet — browse a folder and click Scan.")
            self.cv.configure(scrollregion=(0,0,100,60))
            return

        cols   = self._col_layout()
        W      = self.cv.winfo_width() or 900
        total  = len(self._rows)
        tot_h  = total * ROW_H + 8
        self.cv.configure(scrollregion=(0, 0, W, tot_h))

        # visible range
        frac0, frac1 = self.cv.yview()
        vis_start = int(frac0 * tot_h)
        vis_end   = int(frac1 * tot_h) + ROW_H
        first = max(0, vis_start // ROW_H)
        last  = min(total, vis_end  // ROW_H + 1)

        for i in range(first, last):
            row = self._rows[i]
            y0  = i * ROW_H
            y1  = y0 + ROW_H
            ym  = y0 + ROW_H // 2

            # ── row background ──────────────────────────────────────
            if i == self._sel:
                bg = C_ROW_SEL
            elif i == self._hover:
                bg = C_ROW_HOVER
            elif row["kind"] == "file":
                z = row["result"]["zone"]
                bg = (C_FLAGGED_BG if row["result"]["anomaly"]
                      else ZONE_PILL_BG.get(z, C_ROW_ODD))
                # lighten: blend toward white
                bg = self._tint(bg, 0.35)
            else:
                bg = C_ROW_ODD if i % 2 == 0 else C_ROW_EVEN

            self.cv.create_rectangle(0, y0, W, y1, fill=bg, outline="")
            self.cv.create_line(0, y1, W, y1, fill=C_DIVIDER)

            # ── col 0: name ─────────────────────────────────────────
            nx, nw = cols[0]
            indent  = 8 + row["depth"] * INDENT_PX

            if row["kind"] == "folder":
                node  = row["node"]
                arrow = "▾" if node.expanded else "▸"
                # arrow glyph
                self.cv.create_text(nx + indent, ym, text=arrow,
                                    fill=C_ACCENT, font=("Segoe UI", 10,"bold"),
                                    anchor="w")
                # folder icon + name
                self.cv.create_text(nx + indent + 14, ym,
                                    text=f"📁  {node.name}",
                                    fill=C_TEXT, font=F_BOLD, anchor="w")
            else:
                result = row["result"]
                fname  = Path(result["path"]).name
                zone   = result["zone"]
                clr    = C_FLAGGED if result["anomaly"] else ZONE_FG.get(zone, C_TEXT)
                self.cv.create_text(nx + indent + 14, ym,
                                    text=f"    📄  {fname}",
                                    fill=clr, font=F_UI, anchor="w")

            # clip line between name and next col
            bx = nx + nw
            self.cv.create_line(bx, y0, bx, y1, fill=C_BORDER)

            # ── col 1: % bar ────────────────────────────────────────
            bx0, bcw = cols[1]
            pct      = row["pct"]
            num_w    = 40
            bar_w    = bcw - num_w - 14
            bx_start = bx0 + 7
            by0      = y0 + BAR_PAD
            by1      = y1 - BAR_PAD

            # track
            self.cv.create_rectangle(bx_start, by0, bx_start + bar_w, by1,
                                     fill=C_BAR_TRACK, outline="")

            fill_w = max(1, int(bar_w * pct / 100))

            if row["kind"] == "folder":
                node     = row["node"]
                sp       = (node.safe_files / node.total_files) if node.total_files else 0
                safe_w   = int(fill_w * sp)
                # unsafe portion
                if fill_w > safe_w:
                    self.cv.create_rectangle(bx_start, by0,
                                             bx_start + fill_w, by1,
                                             fill=C_BAR_UNSAFE, outline="")
                # safe portion
                if safe_w > 0:
                    self.cv.create_rectangle(bx_start, by0,
                                             bx_start + safe_w, by1,
                                             fill=C_BAR_SAFE, outline="")
            else:
                zone = row["result"]["zone"]
                fc   = ZONE_FG.get(zone, C_ACCENT)
                self.cv.create_rectangle(bx_start, by0,
                                         bx_start + fill_w, by1,
                                         fill=fc, outline="")

            # pct number
            self.cv.create_text(bx_start + bar_w + 5, ym,
                                 text=f"{pct:.1f}%", fill=C_SUBTEXT,
                                 font=F_SMALL, anchor="w")
            self.cv.create_line(bx0+bcw, y0, bx0+bcw, y1, fill=C_BORDER)

            # ── col 2: size ─────────────────────────────────────────
            sx, scw = cols[2]
            sz = (row["node"].total_size if row["kind"] == "folder"
                  else row["result"]["size"])
            self.cv.create_text(sx + scw - 7, ym, text=human_size(sz),
                                fill=C_TEXT, font=F_UI, anchor="e")
            self.cv.create_line(sx+scw, y0, sx+scw, y1, fill=C_BORDER)

            if row["kind"] == "folder":
                node = row["node"]

                # col 3: total files
                tx, tcw = cols[3]
                self.cv.create_text(tx+tcw-7, ym, text=f"{node.total_files:,}",
                                    fill=C_TEXT, font=F_UI, anchor="e")
                self.cv.create_line(tx+tcw, y0, tx+tcw, y1, fill=C_BORDER)

                # col 4: safe to delete
                sfx, sfcw = cols[4]
                self.cv.create_text(sfx+sfcw-7, ym, text=f"{node.safe_files:,}",
                                    fill=C_USER, font=F_BOLD, anchor="e")
                self.cv.create_line(sfx+sfcw, y0, sfx+sfcw, y1, fill=C_BORDER)

                # col 5: safe %
                spx, spcw = cols[5]
                sp  = (node.safe_files / node.total_files * 100) if node.total_files else 0
                sc  = C_USER if sp >= 70 else (C_APPDATA if sp >= 30 else C_OS)
                self.cv.create_text(spx+spcw-7, ym, text=f"{sp:.0f}%",
                                    fill=sc, font=F_BOLD, anchor="e")
                self.cv.create_line(spx+spcw, y0, spx+spcw, y1, fill=C_BORDER)

                # col 6: zone pill (dominant)
                zx, zcw = cols[6]
                dom   = max(node.zone_counts, key=node.zone_counts.get)
                self._draw_pill(zx+8, ym, ZONE_BADGE[dom],
                                ZONE_FG[dom], ZONE_PILL_BG[dom])

            else:
                result = row["result"]
                zone   = result["zone"]

                # col 3
                tx, tcw = cols[3]
                self.cv.create_text(tx+tcw-7, ym, text="1",
                                    fill=C_SUBTEXT, font=F_UI, anchor="e")
                self.cv.create_line(tx+tcw, y0, tx+tcw, y1, fill=C_BORDER)

                # col 4: safe yes/no pill
                sfx, sfcw = cols[4]
                is_safe = zone in SAFE_ZONES
                s_txt = "✓ Safe" if is_safe else "✗ Keep"
                s_fg  = C_USER  if is_safe else C_OS
                s_bg  = C_USER_BG if is_safe else C_OS_BG
                self._draw_pill(sfx+8, ym, s_txt, s_fg, s_bg)
                self.cv.create_line(sfx+sfcw, y0, sfx+sfcw, y1, fill=C_BORDER)

                # col 5
                spx, spcw = cols[5]
                self.cv.create_text(spx+spcw-7, ym, text="—",
                                    fill=C_SUBTEXT, font=F_UI, anchor="e")
                self.cv.create_line(spx+spcw, y0, spx+spcw, y1, fill=C_BORDER)

                # col 6: zone pill
                zx, zcw = cols[6]
                self._draw_pill(zx+8, ym, ZONE_BADGE[zone],
                                ZONE_FG[zone], ZONE_PILL_BG[zone])

        self._draw_header()

    def _draw_pill(self, x, y, text, fg, bg):
        """Draw a rounded-rectangle badge pill."""
        pad_x, pad_y = 6, 3
        # measure text width roughly (Segoe UI 8 ≈ 6px/char)
        tw = len(text) * 6 + pad_x * 2
        th = PILL_H
        x1, y1 = x, y - th//2
        x2, y2 = x + tw, y + th//2
        r = PILL_R
        pts = [x1+r,y1, x2-r,y1, x2,y1, x2,y1+r,
               x2,y2-r, x2,y2, x2-r,y2, x1+r,y2,
               x1,y2, x1,y2-r, x1,y1+r, x1,y1]
        self.cv.create_polygon(pts, smooth=True, fill=bg, outline=bg)
        self.cv.create_text(x + tw//2, y, text=text, fill=fg,
                            font=("Segoe UI", 8, "bold"), anchor="center")

    @staticmethod
    def _tint(hex_col, alpha):
        """Blend hex_col toward white by alpha (0=original, 1=white)."""
        r = int(hex_col[1:3], 16)
        g = int(hex_col[3:5], 16)
        b = int(hex_col[5:7], 16)
        r = int(r + (255-r)*alpha)
        g = int(g + (255-g)*alpha)
        b = int(b + (255-b)*alpha)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ── events ──────────────────────────────────────────────────────────
    def _abs_y(self, canvas_y):
        tot_h = len(self._rows) * ROW_H
        return int(self.cv.yview()[0] * tot_h) + canvas_y

    def _row_at(self, canvas_y):
        idx = self._abs_y(canvas_y) // ROW_H
        return idx if 0 <= idx < len(self._rows) else -1

    def _click(self, ev):
        idx = self._row_at(ev.y)
        if idx < 0: return
        self._sel = idx
        row = self._rows[idx]
        if row["kind"] == "folder":
            row["node"].expanded = not row["node"].expanded
            self._flatten()
        self._draw()

    def _dbl(self, ev):
        idx = self._row_at(ev.y)
        if idx < 0: return
        row = self._rows[idx]
        if row["kind"] == "file":
            r   = row["result"]
            anm = f"\n\n⚠  Flagged: {r['anomaly']}" if r["anomaly"] else ""
            safe_s = ("✓ Yes — safe to delete"
                      if r["zone"] in SAFE_ZONES
                      else "✗ No — required by Windows")
            messagebox.showinfo("File Details",
                f"Path:            {r['path']}\n"
                f"Zone:            {r['zone']}\n"
                f"Source:          {r.get('source','')}\n"
                f"Size:            {human_size(r['size'])}\n"
                f"Safe to delete:  {safe_s}{anm}")
        else:
            node = row["node"]
            sp   = (node.safe_files/node.total_files*100) if node.total_files else 0
            zd   = "\n".join(
                f"  {ZONE_BADGE[z]}: {node.zone_counts[z]:,} files"
                for z in (ZONE_OS, ZONE_APP, ZONE_USER, ZONE_USER_APPDATA)
                if node.zone_counts[z])
            messagebox.showinfo("Folder Details",
                f"Path:            {node.path}\n"
                f"Total size:      {human_size(node.total_size)}\n"
                f"Total files:     {node.total_files:,}\n"
                f"Safe to delete:  {node.safe_files:,} files  ({sp:.0f}%)\n"
                f"Safe size:       {human_size(node.safe_size)}\n\n"
                f"Zone breakdown:\n{zd}")

    def _motion(self, ev):
        self._set_hover(self._row_at(ev.y))

    def _set_hover(self, idx):
        if idx != self._hover:
            self._hover = idx
            self._draw()

    def _vscroll(self, *args):
        self.cv.yview(*args)
        self._draw()

    def _wheel(self, ev):
        self.cv.yview_scroll(int(-1*(ev.delta/120)), "units")
        self._draw()

    def _resize(self, ev):
        self._draw()

    def _hdr_click(self, ev):
        cols = self._col_layout()
        for i, (cid, *_) in enumerate(COL_DEFS):
            x0, cw = cols[i]
            if x0 <= ev.x < x0+cw:
                if self._sort_col == cid:
                    self._sort_desc = not self._sort_desc
                else:
                    self._sort_col  = cid
                    self._sort_desc = True
                if self._root_node:
                    self._flatten()
                self._draw()
                return

    def _hdr_motion(self, ev):
        cols = self._col_layout()
        for i, _ in enumerate(COL_DEFS):
            x0, cw = cols[i]
            if x0 <= ev.x < x0+cw:
                self.hdr.config(cursor="hand2")
                return
        self.hdr.config(cursor="")


# ---------------------------------------------------------------------------
# Toolbar button helper  (flat, rounded-looking via relief)
# ---------------------------------------------------------------------------

def _make_btn(parent, text, cmd, primary=False, state="normal"):
    bg = C_BTN_BG  if primary else C_BTN_SEC
    fg = C_BTN_FG  if primary else C_BTN_SEC_FG
    b  = tk.Button(parent, text=text, command=cmd,
                   bg=bg, fg=fg,
                   relief="flat", bd=0,
                   font=F_UI, padx=10, pady=4,
                   cursor="hand2", state=state,
                   activebackground=C_ACCENT_HOV if primary else "#e0e0e0",
                   activeforeground=fg)
    return b


# ---------------------------------------------------------------------------
# Main App
# ---------------------------------------------------------------------------

class ClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows File Classifier")
        self.root.geometry("1120x720")
        self.root.configure(bg=C_WIN_BG)
        self.root.minsize(800, 500)

        self.q             = queue.Queue()
        self.stop_flag     = threading.Event()
        self.all_results   = []
        self.folder_tree   = None
        self.zone_counts   = {ZONE_OS:0, ZONE_APP:0, ZONE_USER:0, ZONE_USER_APPDATA:0}
        self.flagged_count = 0

        self._build_ui()
        self.root.after(100, self._poll)

    # ── UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar",
                        troughcolor=C_BORDER,
                        background=C_ACCENT,
                        thickness=4)
        style.configure("slim.Horizontal.TProgressbar",
                        troughcolor=C_BORDER,
                        background=C_ACCENT,
                        thickness=4)

        # ── toolbar ─────────────────────────────────────────────────
        tb = tk.Frame(self.root, bg=C_TOOLBAR_BG,
                      highlightbackground=C_BORDER,
                      highlightthickness=1)
        tb.pack(fill="x", padx=0, pady=0)

        tk.Label(tb, text="Folder", bg=C_TOOLBAR_BG,
                 fg=C_SUBTEXT, font=F_SMALL).pack(side="left", padx=(12,4), pady=8)

        self.folder_var = tk.StringVar()
        entry_frame = tk.Frame(tb, bg=C_BORDER, bd=1)
        entry_frame.pack(side="left", padx=0, pady=8)
        self.folder_entry = tk.Entry(
            entry_frame, textvariable=self.folder_var, width=52,
            font=F_UI, relief="flat", bd=4,
            bg="#ffffff", fg=C_TEXT, insertbackground=C_TEXT)
        self.folder_entry.pack()

        _make_btn(tb, "Browse…", self.browse, primary=False).pack(
            side="left", padx=(6,2), pady=8)

        self.scan_btn = _make_btn(tb, "▶  Scan", self.start_scan, primary=True)
        self.scan_btn.pack(side="left", padx=2, pady=8)

        self.stop_btn = _make_btn(tb, "■  Stop", self.stop_scan, primary=False,
                                  state="disabled")
        self.stop_btn.pack(side="left", padx=2, pady=8)

        # separator
        tk.Frame(tb, bg=C_BORDER, width=1).pack(
            side="left", fill="y", padx=8, pady=6)

        _make_btn(tb, "Export CSV…", self.export_csv).pack(
            side="left", padx=2, pady=8)

        self.recurse_var = tk.BooleanVar(value=True)
        tk.Checkbutton(tb, text="Include subfolders",
                       variable=self.recurse_var,
                       bg=C_TOOLBAR_BG, fg=C_TEXT,
                       font=F_UI, activebackground=C_TOOLBAR_BG,
                       selectcolor=C_TOOLBAR_BG).pack(
            side="left", padx=10, pady=8)

        # ── summary strip ───────────────────────────────────────────
        strip = tk.Frame(self.root, bg=C_WIN_BG)
        strip.pack(fill="x", padx=12, pady=(6,0))

        self.badge_lbls = {}
        defs = [
            (ZONE_OS,           C_OS,      C_OS_BG,      "OS Files"),
            (ZONE_APP,          C_APP,     C_APP_BG,     "Applications"),
            (ZONE_USER,         C_USER,    C_USER_BG,    "User Data"),
            (ZONE_USER_APPDATA, C_APPDATA, C_APPDATA_BG, "App Data"),
        ]
        for zone, fg, bg, label in defs:
            card = tk.Frame(strip, bg=bg, bd=0,
                            highlightbackground=fg,
                            highlightthickness=1)
            card.pack(side="left", padx=(0,8), pady=2, ipadx=10, ipady=4)
            tk.Label(card, text=label, bg=bg, fg=fg,
                     font=("Segoe UI", 7, "bold")).pack()
            lbl = tk.Label(card, text="0", bg=bg, fg=fg,
                           font=("Segoe UI", 14, "bold"))
            lbl.pack()
            self.badge_lbls[zone] = lbl

        # flagged card
        flag_card = tk.Frame(strip, bg=C_FLAGGED_BG, bd=0,
                             highlightbackground=C_FLAGGED,
                             highlightthickness=1)
        flag_card.pack(side="left", padx=(0,8), pady=2, ipadx=10, ipady=4)
        tk.Label(flag_card, text="⚠ Flagged", bg=C_FLAGGED_BG,
                 fg=C_FLAGGED, font=("Segoe UI", 7, "bold")).pack()
        self.flag_lbl = tk.Label(flag_card, text="0", bg=C_FLAGGED_BG,
                                 fg=C_FLAGGED, font=("Segoe UI", 14, "bold"))
        self.flag_lbl.pack()

        # ── filter + status row ─────────────────────────────────────
        frow = tk.Frame(self.root, bg=C_WIN_BG)
        frow.pack(fill="x", padx=12, pady=(6,2))

        tk.Label(frow, text="Show:", bg=C_WIN_BG,
                 fg=C_SUBTEXT, font=F_UI).pack(side="left")

        self.filter_var = tk.StringVar(value="All")
        flt_frame = tk.Frame(frow, bg=C_BORDER, bd=1)
        flt_frame.pack(side="left", padx=(4,0))

        # manual pill-style radio buttons (cleaner than Combobox)
        self._flt_btns = {}
        for val in ("All", ZONE_OS, ZONE_APP, ZONE_USER,
                    ZONE_USER_APPDATA, "Safe only", "Flagged only"):
            short = {"All":"All", ZONE_OS:"OS", ZONE_APP:"App",
                     ZONE_USER:"User", ZONE_USER_APPDATA:"AppData",
                     "Safe only":"Safe ✓", "Flagged only":"⚠ Flagged"}.get(val, val)
            b = tk.Button(flt_frame, text=short, relief="flat", bd=0,
                          font=F_SMALL, padx=8, pady=3,
                          cursor="hand2",
                          command=lambda v=val: self._set_filter(v))
            b.pack(side="left")
            self._flt_btns[val] = b
        self._highlight_filter("All")

        self.status_var = tk.StringVar(value="Ready — choose a folder and click Scan")
        tk.Label(frow, textvariable=self.status_var,
                 bg=C_WIN_BG, fg=C_SUBTEXT, font=F_SMALL).pack(
            side="right", padx=4)

        # ── thin progress bar ───────────────────────────────────────
        self.progress = ttk.Progressbar(
            self.root, mode="determinate",
            style="slim.Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=0, pady=(2,0))

        # ── tree ────────────────────────────────────────────────────
        tree_border = tk.Frame(self.root, bg=C_BORDER, bd=0,
                               highlightbackground=C_BORDER,
                               highlightthickness=1)
        tree_border.pack(fill="both", expand=True, padx=8, pady=(4,8))

        self.tree = WizTree(tree_border)
        self.tree.pack(fill="both", expand=True)

        # ── legend ──────────────────────────────────────────────────
        leg = tk.Frame(self.root, bg=C_WIN_BG)
        leg.pack(fill="x", padx=12, pady=(0,4))
        items = [
            ("% bar: ▓ = % of parent  |  green = safe portion  |  red = OS portion",
             C_SUBTEXT),
            ("  ●", C_USER), (" USER DATA", C_SUBTEXT),
            ("  ●", C_APP),  (" APP",       C_SUBTEXT),
            ("  ●", C_APPDATA),(" APPDATA",  C_SUBTEXT),
            ("  ●", C_OS),   (" OS (keep)", C_SUBTEXT),
        ]
        for txt, clr in items:
            tk.Label(leg, text=txt, bg=C_WIN_BG, fg=clr,
                     font=F_SMALL).pack(side="left")

    def _set_filter(self, val):
        self.filter_var.set(val)
        self._highlight_filter(val)
        self.tree.set_filter(val)

    def _highlight_filter(self, active):
        for val, btn in self._flt_btns.items():
            if val == active:
                btn.config(bg=C_ACCENT, fg="#ffffff")
            else:
                btn.config(bg="#f1f3f4", fg=C_TEXT)

    # ── scan ────────────────────────────────────────────────────────────
    def browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def start_scan(self):
        folder = self.folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Invalid folder",
                                 "Please choose a valid folder first.")
            return
        self.all_results   = []
        self.folder_tree   = None
        self.zone_counts   = {ZONE_OS:0, ZONE_APP:0, ZONE_USER:0,
                              ZONE_USER_APPDATA:0}
        self.flagged_count = 0
        self._refresh_badges()
        self.stop_flag.clear()
        self.status_var.set("Scanning…")
        self.progress["value"] = 0
        self.scan_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.tree.load(FolderNode("__root__"))
        threading.Thread(target=self._bg_scan,
                         args=(folder, self.recurse_var.get()),
                         daemon=True).start()

    def _bg_scan(self, folder, recurse):
        def prog(cur, tot):
            self.q.put(("prog", cur, tot))
        try:
            for r in self._scan(folder, recurse, prog):
                self.q.put(("result", r))
        except Exception as e:
            self.q.put(("err", str(e)))
        self.q.put(("done", None))

    def _scan(self, root_folder, recurse, prog_cb):
        files = []
        if recurse:
            for dp, dns, fns in os.walk(root_folder, topdown=True):
                # Prune junctions/symlinked dirs in-place so os.walk never
                # descends into them (prevents double-counting through
                # profile aliases and possible circular junction loops).
                dns[:] = [d for d in dns if not is_reparse_point(os.path.join(dp, d))]
                for fn in fns:
                    files.append(os.path.join(dp, fn))
        else:
            for fn in os.listdir(root_folder):
                fp = os.path.join(root_folder, fn)
                if os.path.isfile(fp):
                    files.append(fp)
        total = len(files)
        for i, fp in enumerate(files):
            if self.stop_flag.is_set(): break
            zone    = classify_path(fp)
            anomaly = check_anomaly(fp, zone)
            ext     = Path(fp).suffix.lower()
            source  = get_source(fp, zone, ext)
            try:    size = os.path.getsize(fp)
            except: size = 0
            prog_cb(i+1, total)
            yield {"path":fp,"zone":zone,"size":size,
                   "anomaly":anomaly,"source":source}

    def stop_scan(self):
        self.stop_flag.set()
        self.status_var.set("Stopping…")

    def _poll(self):
        try:
            for _ in range(300):
                item = self.q.get_nowait()
                kind = item[0]
                if kind == "prog":
                    _, c, t = item
                    self.progress.configure(maximum=max(t,1), value=c)
                    self.status_var.set(f"Scanning… {c:,} / {t:,} files")
                elif kind == "result":
                    r = item[1]
                    self.all_results.append(r)
                    self.zone_counts[r["zone"]] += 1
                    if r["anomaly"]: self.flagged_count += 1
                    self._refresh_badges()
                elif kind == "err":
                    messagebox.showerror("Error", item[1])
                elif kind == "done":
                    self._done()
        except queue.Empty:
            pass
        self.root.after(120, self._poll)

    def _done(self):
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        total = len(self.all_results)
        safe  = sum(1 for r in self.all_results if r["zone"] in SAFE_ZONES)
        pct   = int(safe*100/total) if total else 0
        self.status_var.set(
            f"{total:,} files scanned  ·  "
            f"Safe to delete: {safe:,} ({pct}%)  ·  "
            f"Double-click any row for details")
        self.folder_tree = build_folder_tree(self.all_results)
        for ch in self.folder_tree.children.values():
            ch.expanded = True
        self.tree.load(self.folder_tree, self.filter_var.get())

    def _refresh_badges(self):
        for zone, lbl in self.badge_lbls.items():
            lbl.config(text=f"{self.zone_counts[zone]:,}")
        self.flag_lbl.config(text=f"{self.flagged_count:,}")

    # ── export ──────────────────────────────────────────────────────────
    def export_csv(self):
        if not self.all_results:
            messagebox.showinfo("Nothing to export", "Run a scan first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files","*.csv")])
        if not path: return
        with open(path,"w",newline="",encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["path","zone","source","size","anomaly"])
            w.writeheader()
            w.writerows(self.all_results)
        messagebox.showinfo("Exported",
                            f"Saved {len(self.all_results):,} rows to {path}")


# ---------------------------------------------------------------------------

def main():
    if os.name != "nt":
        print("Note: designed for Windows (C:\\ drive paths).")
    root = tk.Tk()
    ClassifierApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()