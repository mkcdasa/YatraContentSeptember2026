import openpyxl,glob,os,csv,re
RAW="raw"; OUT="parsed"
for p in sorted(glob.glob(RAW+"/*.xlsx")):
    b=os.path.basename(p)
    if b.startswith('~$') or re.match(r'^1[A-Za-z0-9_-]{5}_',b): continue
    try: wb=openpyxl.load_workbook(p,read_only=True,data_only=True)
    except Exception as e: print("ERR",b,e); continue
    for ws in wb.worksheets:
        rows=[r for r in ws.iter_rows(values_only=True) if any(v is not None for v in r)]
        if not rows: continue
        fn=OUT+"/"+b[:-5][:40]+"__"+re.sub(r'[^A-Za-z0-9]+','_',ws.title)[:30]+".csv"
        with open(fn,'w',newline='') as f:
            w=csv.writer(f)
            for r in rows: w.writerow(["" if v is None else v for v in r])
        print(len(rows),fn)
