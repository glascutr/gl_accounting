data =[ 
    {"title":"BDCOM Online Ltd IPTSP Telephone bill for July'25"},
    {"title":"BDCOM Online Ltd. IPTSP telephone bill for June'25"},
    {"title":"BTCL Telephone bill for July'25 with mobile flexiload"},
    {"title":"BTCL Telephone bill for June'25"},
    {"title":"Balancing Figure, Cash at the Bank (01-07-2025)"},
    {"title":"Balancing Figure, Cash in Hand (01-07/2025)"},
    {"title":"Bank Charge debit our a/c"},
    {"title":"Bank Charges debit our a/c"},
    {"title":"Binimoy Properties, Annual Main. June'25 to may'26 & Hosting fees Aug;25 to Jul'26"},
    {"title":"Cash Withdrawn against Electricity, Salary Tax with cleaner salary"},
    {"title":"Cash withdrawn against office petty cash"},
    {"title":"Cash withdrawn against office rent"},
    {"title":"Cheque received form intex web-based customized software"},
    {"title":"Cheque received from Intex web-based customized software"},
    {"title":"Conceyance for Mrs. Nowrin"},
    {"title":"Conveyance for Mahmud"},
    {"title":"Conveyance for Mahmud and Nowrin"},
    {"title":"Conveyance for Mr. Jahid"},
    {"title":"Conveyance for Mr. Mahmud"},
    {"title":"Conveyance for Mrs. Nowrin"},
    {"title":"Conveyance for Mrs. Nowrin and Jahid"},
    {"title":"Conveyance for Ms. Nowrin"},
    {"title":"Conveyance for Nowrin and Jahid"},
    {"title":"Conveyance for Siddique, Jahid and Nowrin"},
    {"title":"DESCO Electricity bill for July'25"},
    {"title":"DESCO Electricity bill for June'25"},
    {"title":"Entertainment for office "},
    {"title":"Entertainment for office guest"},
    {"title":"Food Allowance for July'25, (Officers) 8 persons"},
    {"title":"Food Allowance for June'25 (Officers)"},
    {"title":"Link3 Internet Bill for June'25"},
    {"title":"Link3 internet bill for July'25"},
    {"title":"Loan received from Chairman by cash"},
    {"title":"Md. Maswud Ul Hassan, Consultant"},
    {"title":"Mobile bill for July'25, 01712810365"},
    {"title":"Mobile flexiload  01712810365 & 01747647677"},
    {"title":"Mrs. Kashfia Nahreen, Land Owner, office rent for August'25"},
    {"title":"Mrs. Kashfia Nahreen, Land Owner, office rent for July'25"},
    {"title":"Multi Cable Network, Dishline bill for the month of August'25"},
    {"title":"Multi cable network, Dishline bill for July'25 "},
    {"title":"Newspaper bill for June'25 received by Mahfuz, land Caretaker "},
    {"title":"Newspaper bill for the month July'25"},
    {"title":"Purchase exhaust fan for bathroom"},
    {"title":"Purchase folder 12pices and gue stick 1pice"},
    {"title":"Purchase harpic, powder, tissu, poli etc"},
    {"title":"Purchase harpic, tissue paper, harpic, powder, poli and etc"},
    {"title":"Purchase kitchen tissue 2pices"},
    {"title":"Purchase medicine one pata"},
    {"title":"Purchase milk 1kg and entertainment for office"},
    {"title":"Purchase milk, tea bag, coffee, suger and etc."},
    {"title":"Purchase milk,suger,coffee,tea bag with entertainment for office guest"},
    {"title":"Purchase one rim paper and odonil"},
    {"title":"Purchase paper, glass cleaner with odonil"},
    {"title":"Purchase pen and battery 6 pices"},
    {"title":"Purchase towner for printer machine"},
    {"title":"Purchase two pices jel pen"},
    {"title":"Purchase two pices kitchen tissu"},
    {"title":"Purchase vim lequeid  "},
    {"title":"Pureit Unilever sfc service charge "},
    {"title":"Salary July'25 - Nazmul Hossain"},
    {"title":"Salary July'25 - Officer's (7 persons)"},
    {"title":"Salary July'25 - Omar Faruk"},
    {"title":"Salary July'25 - Shabana Khatun,Cleaner"},
    {"title":"Salary June'25 - Nazmul Hossain (Part Time)"},
    {"title":"Salary June'25 - Officer's (7 persons)"},
    {"title":"Salary June'25 - Shabana Khatun, Cleaner"},
    {"title":"Salary Jute'25 - Omar Faruk (Part time)"},
    {"title":"Salary Tax for July'25(Mahmud 3000/- Nowrin 500/- Siddiqur 1500/- Nazmul 2000/- Nusrat 500/-)"},
    {"title":"Salay Tax for June'25 (Mahmud 3000/-, Nowrin 500/- Siddique 1500/-)"},
    {"title":"Waste disposal bill for June'25 received by Mahmuz, land caretaker"},
    {"title":"Waste disposal bill for the month august'25 received by Jasim Mollik"}
]


skipped = []
for row in data:
    
    if frappe.db.exists("Particulars", {"title": row["title"]}):
            skipped.append(row)
            continue

    print(row)
    doc = frappe.get_doc({
        "doctype": "Particulars",
        **row
    })


    doc.insert(ignore_permissions=True)

frappe.db.commit()

