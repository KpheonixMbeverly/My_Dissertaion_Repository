"""Addendum A, section 6: chapter-3 point estimates with P3 = 2021-08..2026-10 (robustness only).
usage: python hp_run_hetero_p3alt.py ZIP DATA_DIR MARKET OUT"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hp_lib as L
L.PERIODS['P3'] = ('2021-08', '2026-10')
import hp_run_hetero as H
ZIP, DATA, MARKET, OUT = sys.argv[1:5]
sys.argv = ['hp_run_hetero.py', ZIP, DATA, MARKET, 'points', '0', OUT]
H.main()
