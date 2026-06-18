# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import mediapipe

# Récupérer le chemin d'installation de mediapipe
mediapipe_dir = os.path.dirname(mediapipe.__file__)

# Nous incluons uniquement la DLL et le init de mediapipe/tasks/c
mp_tasks_c_path = os.path.join(mediapipe_dir, 'tasks', 'c')

datas = [
    ('hand_landmarker.task', '.'),
    ('gesture_model.pkl', '.'),
    (os.path.join(mp_tasks_c_path, '__init__.py'), 'mediapipe/tasks/c'),
    (os.path.join(mediapipe_dir, 'modules'), 'mediapipe/modules'), # requis pour les graphs MediaPipe
]

binaries = [
    (os.path.join(mp_tasks_c_path, 'libmediapipe.dll'), 'mediapipe/tasks/c'),
]

# Déclarer uniquement les imports cachés requis de mediapipe.tasks
hiddenimports = [
    'mediapipe.tasks.c',
]

# Lister dynamiquement les sous-modules python de mediapipe.tasks.python
mp_tasks_python_dir = os.path.join(mediapipe_dir, 'tasks', 'python')
for root, dirs, files in os.walk(mp_tasks_python_dir):
    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            rel_path = os.path.relpath(os.path.join(root, file), mediapipe_dir)
            module_name = 'mediapipe.' + rel_path.replace(os.sep, '.')[:-3]
            hiddenimports.append(module_name)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
