import csv,glob,re,collections,os
P="parsed/"
def rd(name):
    return [r for r in csv.reader(open(P+name))]
def show(name,maxrows=60,maxcols=12,w=22):
    print(f"\n### {name}")
    for r in rd(name)[:maxrows]:
        cells=[c.strip().replace("\n"," ")[:w] for c in r[:maxcols]]
        if any(cells): print(" | ".join(cells))
def num(x):
    try: return float(str(x).replace(",","").replace("₹","").strip())
    except: return None

show("Expenditures_-Jan_to_Sep_2022__Sheet7.csv")
show("Expenditures_-Jan_to_Sep_2022__Salaries_Break_Up.csv")
show("Expenditures_-Jan_to_Sep_2022__All_Salaries.csv")
show("FINAL-JAN_22_to_FEB_23__13_Months.csv",50,10)
show("FINAL-JAN_22_to_FEB_23__Simple_13_Months_Report.csv")
show("FINAL-JAN_22_to_FEB_23__DashBoard_2_.csv",20,10)
show("REPORT-FOR_MANAGEMENT_-_18th_Jan_2023__Jan_Dec.csv",30,6,30)
show("REPORT-FOR_MANAGEMENT_-_18th_Jan_2023__April_2022_Sep_2022.csv",20,6,34)
show("REPORT-FOR_MANAGEMENT_-_18th_Jan_2023__All_Campaigns_Master_Dashboard.csv",95,14,16)
show("Tridas_common_Expenditure_Details__Tax_Planing.csv",25,8)
show("Tridas_common_Expenditure_Details__Expenditure.csv",60,4,34)
show("Tridas_common_Expenditure_Details__Salaries_Projection.csv",70,9,26)
show("Tele_Calling_-_MKCD_SHSD_-_Salary_Struct__Expenditures.csv",20,12,14)
show("Tele_Calling_-_MKCD_SHSD_-_Salary_Struct__Income.csv",10,6)
show("Monthly_Expenditures__Sheet1.csv",30,7,30)
show("Copy_of_DMT_COLLECTION_1___Sheet2.csv",30,13,12)
show("ALL_Salaries_from_April_to_October_2025-__Sheet2.csv",30,14,14)
show("Yatra_Marketing___Sheet1.csv",25,4,30)
show("harekrishna-movement.in-Prasadam_Account__Dashboard.csv",20,4)

# Salaries apportioned aggregation
print("\n### ALL Salaries Apr-Oct 2025 Sheet1 aggregation")
rows=rd("ALL_Salaries_from_April_to_October_2025-__Sheet1.csv")
hdr=None
for i,r in enumerate(rows):
    if r and r[0]=='Trusts': hdr=r; start=i+1; break
print("hdr:",hdr)
data=rows[start:]
# columns: Trusts,Beneficiary Name,CTC,Purpose,Diff,DMT SMS,DMT Paid,Websites,DLLP,Yatras,Tele Callers,Total,Month,Verticle,...
by_month=collections.defaultdict(float); by_vert=collections.defaultdict(float); by_paid=collections.defaultdict(float); by_person=collections.defaultdict(float)
by_cat=collections.defaultdict(float)
catidx={5:'DMT SMS',6:'DMT Paid',7:'Websites',8:'DLLP',9:'Yatras',10:'Tele Callers'}
n=0
for r in data:
    if len(r)<14: continue
    ctc=num(r[2]); 
    if ctc is None: continue
    n+=1
    by_month[r[12][:7]]+=ctc; by_vert[r[13]]+=ctc; by_person[r[1].strip().upper()]+=ctc
    if len(r)>15: by_paid[r[15]]+=ctc
    for k,v in catidx.items():
        x=num(r[k]); 
        if x: by_cat[v]+=x
print("rows",n,"total CTC",sum(by_month.values()))
for k in sorted(by_month): print("  month",k,round(by_month[k]))
for k,v in sorted(by_vert.items(),key=lambda x:-x[1]): print("  vertical",k,round(v))
for k,v in sorted(by_paid.items(),key=lambda x:-x[1]): print("  paidfrom",k,round(v))
for k,v in sorted(by_cat.items(),key=lambda x:-x[1]): print("  category",k,round(v))
print("  people:",len(by_person))
for k,v in sorted(by_person.items(),key=lambda x:-x[1])[:45]: print("   ",k,round(v))

# Yatra vendor payments 12 months
print("\n### Yatra vendor payments 12 months")
rows=rd("Yatra_Dept_-_Payments_Processed_to_Vendo__Sheet1.csv")
print(rows[0]); print(rows[1]); print(rows[2])
