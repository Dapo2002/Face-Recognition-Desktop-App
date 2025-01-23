# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
import os
import sys
from PyInstaller.building.build_main import Analysis, PYZ, EXE

# Define the path to the additional files
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Path to the shape_predictor .dat files
face_landmarks_path = r'C:\Users\user\OneDrive\Desktop\Abdulbadie Projects\pythonProject\venv\Lib\site-packages\face_recognition_models\models\dlib_face_recognition_resnet_model_v1.dat'
face_landmarks_path_1 = r'C:\Users\user\OneDrive\Desktop\Abdulbadie Projects\pythonProject\venv\Lib\site-packages\face_recognition_models\models\mmod_human_face_detector.dat'
face_landmarks_path_2 = r'C:\Users\user\OneDrive\Desktop\Abdulbadie Projects\pythonProject\venv\Lib\site-packages\face_recognition_models\models\shape_predictor_5_face_landmarks.dat'
face_landmarks_path_3 = r'C:\Users\user\OneDrive\Desktop\Abdulbadie Projects\pythonProject\venv\Lib\site-packages\face_recognition_models\models\shape_predictor_68_face_landmarks.dat'

# Add your additional files here
a = Analysis(
    ['main.py'],
    pathex=[r'C:\Users\user\PycharmProjects\face recognition desktop app'],
    binaries=[],
    datas=[
        (resource_path('student_attendance.db'), '.'),
        (face_landmarks_path, 'face_recognition_models/models'),  # Include the .dat file
        (face_landmarks_path_1, 'face_recognition_models/models'), # _5_ .dat file
        (face_landmarks_path_2, 'face_recognition_models/models'),
        (face_landmarks_path_3, 'face_recognition_models/models')
    ],
    hiddenimports=['face_recognition'],
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
    name='FaceRecognitionApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
