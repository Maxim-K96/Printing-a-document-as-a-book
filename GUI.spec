# -*- mode: python ; coding: utf-8 -*-

from kivy.deps import sdl2, glew
import sys

block_cipher = None

app_name = 'PageBooks'

a = Analysis(['GUI.py'],
  pathex=['C:\\Users\\User\\Desktop\\Python\\pages_print'],
  binaries=None,
  datas=None,

  hiddenimports=[
  'webbrowser',
  '__init__',
  'data.__init__',
  'data.screens.__init__',
  'data.screens.dbmanager',
  'data.screens.db_kv.__init__',
  'data.screens.db_kv.backupsd',
  ],

  hookspath=[],
  runtime_hooks=[],
  excludes=[],
  win_no_prefer_redirects=False,
  win_private_assemblies=False,
  cipher=block_cipher)


# exclusion list
from os.path import join
from fnmatch import fnmatch
# [Documentation]:(http://espressocode.top/fnmatch-unix-filename-pattern-matching-python/)
exclusion_patterns = (
  join("kivy_install", "data", "images", "testpattern.png"),
  join("kivy_install", "data", "images", "image-loading.gif"),
  join("kivy_install", "data", "keyboards*"),
  join("kivy_install", "data", "settings_kivy.json"),
  join("kivy_install", "data", "logo*"),
  join("kivy_install", "data", "fonts", "DejaVuSans*"),
  join("kivy_install", "modules*"),
  join("Include*"),
  join("sdl2-config"),

  # Filter app directory
  join(".idea*"),
)

def can_exclude(fn):
    for pat in exclusion_patterns:
        if fnmatch(fn, pat):
            return True

a.datas = [x for x in a.datas if not can_exclude(x[0])]
a.binaries = [x for x in a.binaries if not can_exclude(x[0])]
# Filter app directory
appfolder = [x for x in Tree('.\\', excludes=['*.py','*.pyc']) if not can_exclude(x[0])]  

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
  a.scripts,
  exclude_binaries=True,
  name=app_name,
  debug=False,
  strip=False,
  upx=True,
  console=True)

coll = COLLECT(exe, appfolder,
  a.binaries,
  a.zipfiles,
  a.datas,
  *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins )],
  strip=False,
  upx=True,
  name=app_name)

