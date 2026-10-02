# -*- coding: utf-8 -*-
"""leer_x.py — igual que leer.py pero sobre las FICHAS agrupadas por tema (etapa del cruce)."""
import os, sys, runpy
os.environ["LEER_SUFIJO"] = "_x"
aqui = os.path.dirname(os.path.abspath(__file__))
sys.argv[0] = os.path.join(aqui, "leer.py")
runpy.run_path(sys.argv[0], run_name="__main__")
