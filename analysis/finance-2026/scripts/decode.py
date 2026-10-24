"""Decode Google Drive connector download results (JSON with base64 content) into .xlsx files.

Usage: python3 -I decode.py <tool-results-dir> <raw-output-dir>
"""
import json,base64,sys,os,re,glob
TR=sys.argv[1]
OUT=sys.argv[2]
os.makedirs(OUT,exist_ok=True)
for f in sorted(glob.glob(TR+"/mcp-Google_Drive-download_file_content-*.txt")):
    try:
        d=json.load(open(f))
    except Exception as e:
        print("skip",f,e); continue
    title=re.sub(r'[^A-Za-z0-9._-]+','_',d['title'])[:80]
    if not title.lower().endswith('.xlsx'): title+='.xlsx'
    p=os.path.join(OUT,title)
    if os.path.exists(p): p=os.path.join(OUT,d['id'][:6]+'_'+title)
    open(p,'wb').write(base64.b64decode(d['content']))
    print(os.path.getsize(p),p)
