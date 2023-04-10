# Niz keyboard toolkit

# Install
Use a virtual environment (venv, conda, etc.) is recommended.
```python
pip install git+https://github.com/cgjosephlee/niz-toolkit.git
```

# Usage
Help
```sh
niztk -h
```

Calibration
```sh
# Calibration tool with GUI
niztk calib
```
![screenshot](https://github.com/cgjosephlee/niz-toolkit/raw/master/assets/calib_gui.png)
- "Lock" before calibration, "Unlock" before quit the app.
- "Calibrate init state": release all keys and calibrate initial state.
- "Calibrate one key": press one key and calibrate actuation state.

Lock/Unlock
```sh
# Lock or unlock your keyboard, for debug purpose
niztk lock
niztk unlock
```

# Reference
- https://github.com/cho45/niz-tools-ruby
- https://github.com/NickCao/nizctl
- https://github.com/chenjr15/niz-tool-python
