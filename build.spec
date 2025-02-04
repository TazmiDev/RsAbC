# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas = [
        ("attack_methods/*.py", "attack_methods"),
        ("utils/*.py", "utils"),
        ("assets/*.*", "assets")
    ],
    hiddenimports=[
        'attack_methods.基础解密',
        'attack_methods.共模攻击',
        'attack_methods.小指数攻击',
        'attack_methods.维纳攻击',
        'attack_methods.费马分解',
        'attack_methods.DP泄露攻击',
        'attack_methods.Pollard分解',
        'attack_methods.已知pq求d',
        'attack_methods.中国剩余定理攻击',
        'attack_methods.CRT快速解密',
        'attack_methods.自动分解攻击'
    ],
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
    name='RsAbC-Windows-x86_64',
    icon='assets/app.ico',
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
