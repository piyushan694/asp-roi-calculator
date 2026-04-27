with open("dashboard/roi_calculator.py", "r", encoding="utf-8") as f:
    c = f.read()
# Fix grid lines for dark background
c = c.replace('gridcolor="#eef0f3"', 'gridcolor="rgba(255,255,255,.06)"')
with open("dashboard/roi_calculator.py", "w", encoding="utf-8") as f:
    f.write(c)
print("OK")
