"""Check that the Python environment can run this project:  python scripts/check_env.py"""
import sys

ok = True
print("Python", sys.version.split()[0])
if sys.version_info < (3, 8):
    print("  -> Python 3.8 or newer is needed"); ok = False
for mod, need in [("numpy", "1.20"), ("scipy", "1.6"), ("pandas", "1.2"), ("joblib", None), ("pytest", None)]:
    try:
        m = __import__(mod)
        v = getattr(m, "__version__", "?")
        bad = need is not None and tuple(int(s) for s in v.split(".")[:2]) < tuple(int(s) for s in need.split("."))
        print("%-7s %-10s %s" % (mod, v, "TOO OLD, need >= " + need if bad else "ok"))
        ok = ok and not bad
    except ImportError:
        optional = mod in ("joblib", "pytest")
        print("%-7s missing %s" % (mod, "(optional)" if optional else ""))
        ok = ok and optional
try:
    from scipy.optimize import linprog
    linprog([1.0], bounds=[(0, None)], method="highs")
    print("HiGHS solver ok")
except Exception as e:  # noqa
    print("HiGHS solver not available:", e); ok = False
print("\nENVIRONMENT OK" if ok else "\nPLEASE FIX THE ITEMS ABOVE")
