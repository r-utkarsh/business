"""Assign salt/composition to every product in the dataset.

Strategy: match by trade line or product name prefix against a curated dictionary
of common Indian pharma trade names -> active ingredients.
"""
import json, os, re

SALT_MAP = {
    # --- Analgesics / Antipyretics ---
    "dolo": "Paracetamol 650mg",
    "calpol": "Paracetamol",
    "crocin": "Paracetamol",
    "combiflam": "Ibuprofen + Paracetamol",
    "nise": "Nimesulide",
    "sumo": "Nimesulide + Paracetamol",
    "meftal": "Mefenamic Acid",
    "meftal spas": "Mefenamic Acid + Dicyclomine",
    "disprin": "Aspirin (Soluble)",
    "ecosprin": "Aspirin",
    "ketorol": "Ketorolac",
    "ketorol dt": "Ketorolac 10mg",
    "zerodol": "Aceclofenac",
    "zerodol p": "Aceclofenac + Paracetamol",
    "zerodol sp": "Aceclofenac + Paracetamol + Serratiopeptidase",
    "dynapar": "Diclofenac",
    "voveran": "Diclofenac Sodium",
    "volini": "Diclofenac Diethylamine Gel",
    "flexon": "Ibuprofen + Paracetamol",
    "nicip": "Nimesulide",
    "hifenac": "Aceclofenac",
    "ultracet": "Tramadol + Paracetamol",
    "saridon": "Propyphenazone + Paracetamol + Caffeine",

    # --- Gastric / Acidity / GI ---
    "pan": "Pantoprazole 40mg",
    "pan d": "Pantoprazole + Domperidone",
    "pantocid": "Pantoprazole",
    "pantocid dsr": "Pantoprazole + Domperidone SR",
    "pantodac": "Pantoprazole",
    "omez": "Omeprazole",
    "omez d": "Omeprazole + Domperidone",
    "omez insta": "Omeprazole",
    "rablet": "Rabeprazole",
    "rablet d": "Rabeprazole + Domperidone",
    "razo": "Rabeprazole",
    "razo d": "Rabeprazole + Domperidone",
    "digene": "Dried Al Hydroxide Gel + Mg Hydroxide + Simethicone",
    "cremaffin": "Liquid Paraffin + Milk of Magnesia",
    "cremaffin plus": "Liquid Paraffin + Milk of Magnesia + Sodium Picosulfate",
    "eno": "Sodium Bicarbonate + Citric Acid",
    "gelusil": "Aluminium Hydroxide + Magnesium Hydroxide + Simethicone",
    "mucaine": "Aluminium Hydroxide + Magnesium Hydroxide + Oxetacaine",
    "hajmola": "Ayurvedic Digestive",
    "pudin hara": "Mentha Oil",
    "duphalac": "Lactulose",
    "looz": "Lactulose",
    "norflox tz": "Norfloxacin + Tinidazole",
    "enterogermina": "Bacillus Clausii Probiotic",
    "econorm": "Saccharomyces Boulardii",
    "cyclopam": "Dicyclomine + Paracetamol",
    "drotin": "Drotaverine",
    "ondem": "Ondansetron",
    "emeset": "Ondansetron",
    "perinorm": "Metoclopramide",
    "domstal": "Domperidone",
    "o2": "Ofloxacin + Ornidazole",
    "metrogyl": "Metronidazole",

    # --- Antibiotics ---
    "augmentin": "Amoxicillin + Clavulanic Acid",
    "clavam": "Amoxicillin + Clavulanic Acid",
    "mox": "Amoxicillin",
    "novamox": "Amoxicillin",
    "azee": "Azithromycin",
    "azithral": "Azithromycin",
    "zithromax": "Azithromycin",
    "ciplox": "Ciprofloxacin",
    "cifran": "Ciprofloxacin",
    "taxim": "Cefixime",
    "taxim o": "Cefixime",
    "ceftas": "Ceftazidime",
    "cefix": "Cefixime",
    "monocef": "Ceftriaxone",
    "mahaflox": "Moxifloxacin",
    "avelox": "Moxifloxacin",
    "levoflox": "Levofloxacin",
    "levofloxacin": "Levofloxacin",
    "lfx": "Levofloxacin",
    "oflox": "Ofloxacin",
    "zocon": "Fluconazole",
    "fluconazole": "Fluconazole",
    "zoxan": "Ciprofloxacin",
    "bactrim": "Cotrimoxazole (Sulfamethoxazole + Trimethoprim)",
    "septran": "Cotrimoxazole (Sulfamethoxazole + Trimethoprim)",
    "linezolid": "Linezolid",

    # --- Antidiabetic ---
    "glycomet": "Metformin",
    "glycomet gp": "Glimepiride + Metformin",
    "glyciphage": "Metformin",
    "zoryl": "Glimepiride",
    "zoryl m": "Glimepiride + Metformin",
    "zoryl mv": "Glimepiride + Metformin + Voglibose",
    "glimisave": "Glimepiride",
    "amaryl": "Glimepiride",
    "amaryl m": "Glimepiride + Metformin",
    "dapanorm": "Dapagliflozin",
    "dapanorm m": "Dapagliflozin + Metformin",
    "galvus": "Vildagliptin",
    "galvus met": "Vildagliptin + Metformin",
    "januvia": "Sitagliptin",
    "janumet": "Sitagliptin + Metformin",
    "trajenta": "Linagliptin",
    "teneligliptin": "Teneligliptin",
    "tendia": "Teneligliptin",
    "tenepure": "Teneligliptin",
    "voglibose": "Voglibose",
    "ppg": "Voglibose",
    "glucobay": "Acarbose",
    "gluformin": "Metformin",
    "obimet": "Metformin",
    "jalra": "Vildagliptin",
    "jalra m": "Vildagliptin + Metformin",
    "remo": "Remogliflozin",
    "invokana": "Canagliflozin",

    # --- Cardiac / BP ---
    "telma": "Telmisartan",
    "telma h": "Telmisartan + Hydrochlorothiazide",
    "telma am": "Telmisartan + Amlodipine",
    "telmikind": "Telmisartan",
    "cilacar": "Cilnidipine",
    "cilacar t": "Cilnidipine + Telmisartan",
    "stamlo": "Amlodipine",
    "stamlo d": "Amlodipine + Hydrochlorothiazide",
    "amlokind": "Amlodipine",
    "amlokind at": "Amlodipine + Atenolol",
    "amlong": "Amlodipine",
    "losar": "Losartan",
    "losar h": "Losartan + Hydrochlorothiazide",
    "repace": "Losartan",
    "concor": "Bisoprolol",
    "metoprol": "Metoprolol",
    "betaloc": "Metoprolol",
    "met xl": "Metoprolol Succinate",
    "aten": "Atenolol",
    "dilzem": "Diltiazem",
    "prazopress": "Prazosin",
    "cardace": "Ramipril",
    "enalapril": "Enalapril",
    "rosuvas": "Rosuvastatin",
    "rozavel": "Rosuvastatin",
    "crestor": "Rosuvastatin",
    "atorva": "Atorvastatin",
    "tonact": "Atorvastatin",
    "lipitor": "Atorvastatin",
    "ecosprin av": "Aspirin + Atorvastatin",
    "ecosprin gold": "Aspirin + Atorvastatin + Clopidogrel",
    "clopitab": "Clopidogrel",
    "clopilet": "Clopidogrel",
    "deplatt": "Clopidogrel",
    "deplatt cv": "Clopidogrel + Atorvastatin",

    # --- Thyroid ---
    "thyronorm": "Levothyroxine Sodium",
    "eltroxin": "Levothyroxine Sodium",
    "thyrox": "Levothyroxine Sodium",
    "neo mercazole": "Carbimazole",
    "mercazole": "Carbimazole",

    # --- Respiratory / Cold / Allergy ---
    "alerid": "Cetirizine",
    "cetzine": "Cetirizine",
    "okacet": "Cetirizine",
    "zyrtec": "Cetirizine",
    "allegra": "Fexofenadine",
    "fexova": "Fexofenadine",
    "levocet": "Levocetirizine",
    "xyzal": "Levocetirizine",
    "montair": "Montelukast",
    "montair lc": "Montelukast + Levocetirizine",
    "montek lc": "Montelukast + Levocetirizine",
    "sinarest": "Paracetamol + Phenylephrine + Chlorpheniramine",
    "cheston": "Paracetamol + Phenylephrine + Cetirizine",
    "cheston cold": "Paracetamol + Phenylephrine + Cetirizine",
    "d cold total": "Paracetamol + Phenylephrine + Chlorpheniramine + Caffeine",
    "alex": "Phenylephrine + Chlorpheniramine + Dextromethorphan",
    "benadryl": "Diphenhydramine + Ammonium Chloride",
    "asthalin": "Salbutamol (Albuterol)",
    "deriphyllin": "Etophylline + Theophylline",
    "foracort": "Formoterol + Budesonide",
    "budecort": "Budesonide",
    "seroflo": "Salmeterol + Fluticasone",
    "duolin": "Levosalbutamol + Ipratropium",
    "tiova": "Tiotropium",
    "mucinac": "Acetylcysteine (NAC)",
    "ambrodil": "Ambroxol",
    "grilinctus": "Dextromethorphan + Phenylephrine + Chlorpheniramine",
    "honitus": "Herbal Cough Syrup (Tulsi + Mulethi + Honey)",
    "koflet": "Herbal Cough Syrup",
    "vicks": "Menthol + Camphor + Eucalyptus Oil",
    "vicks vaporub": "Menthol + Camphor + Eucalyptus Oil",
    "strepsils": "Dichlorobenzyl Alcohol + Amylmetacresol",

    # --- Vitamins / Supplements / Nutrition ---
    "cipcal": "Calcium + Vitamin D3",
    "shelcal": "Calcium + Vitamin D3",
    "calcimax": "Calcium + Vitamin D3",
    "gemcal": "Calcium + Calcitriol",
    "zincovit": "Multivitamin + Multimineral + Zinc",
    "supradyn": "Multivitamin + Multimineral",
    "becosules": "B-Complex + Vitamin C",
    "becosules z": "B-Complex + Vitamin C + Zinc",
    "neurobion": "Vitamin B1 + B6 + B12",
    "neurobion forte": "Vitamin B1 + B6 + B12",
    "methylcobal": "Methylcobalamin (Vitamin B12)",
    "nurokind": "Methylcobalamin",
    "mecobalamin": "Methylcobalamin",
    "folvite": "Folic Acid",
    "limcee": "Vitamin C (Ascorbic Acid)",
    "celin": "Vitamin C (Ascorbic Acid)",
    "d3": "Cholecalciferol (Vitamin D3)",
    "calcirol": "Cholecalciferol (Vitamin D3)",
    "uprise": "Cholecalciferol (Vitamin D3)",
    "tayo": "Cholecalciferol (Vitamin D3) 60K",
    "livogen": "Iron + Folic Acid",
    "autrin": "Iron + Folic Acid + B12",
    "dexorange": "Iron + Vitamin B12 + Folic Acid",
    "orofer xt": "Iron + Folic Acid",
    "revital": "Multivitamin + Ginseng",
    "evion": "Vitamin E (Tocopherol)",
    "ensure": "Balanced Complete Nutrition Powder",
    "pediasure": "Growth Nutrition for Children",
    "similac": "Infant Formula (DHA + HMO)",
    "protinex": "High Protein Nutrition Powder",
    "resource": "Balanced Nutrition Powder",
    "ceregrow": "Cereal Nutrition for Children",

    # --- Antacid / PPI (supplemental) ---
    "nexpro": "Esomeprazole",
    "nexpro rd": "Esomeprazole + Domperidone",
    "aciloc": "Ranitidine",
    "rantac": "Ranitidine",
    "zinetac": "Ranitidine",
    "famocid": "Famotidine",
    "sucralfate": "Sucralfate",
    "sucrafil": "Sucralfate",

    # --- Dermatology / Skin ---
    "betadine": "Povidone-Iodine",
    "betnovate": "Betamethasone Valerate",
    "betnovate c": "Betamethasone + Clioquinol",
    "betnovate n": "Betamethasone + Neomycin",
    "betnovate gm": "Betamethasone + Gentamicin + Miconazole",
    "clobetasol": "Clobetasol Propionate",
    "tenovate": "Clobetasol Propionate",
    "panderm": "Clobetasol + Ofloxacin + Miconazole + Dexpanthenol",
    "quadriderm": "Betamethasone + Gentamicin + Tolnaftate + Clioquinol",
    "candid": "Clotrimazole",
    "candid b": "Clotrimazole + Beclometasone",
    "mycoderm": "Clotrimazole Dusting Powder",
    "lulibest": "Luliconazole",
    "lulibet": "Luliconazole",
    "terbinafine": "Terbinafine",
    "silverex": "Silver Sulfadiazine",
    "soframycin": "Framycetin Skin Cream",
    "fucidin": "Fusidic Acid",
    "t-bact": "Mupirocin",
    "acnestar": "Clindamycin + Nicotinamide / Benzoyl Peroxide",
    "adapalene": "Adapalene",
    "retino a": "Tretinoin",
    "kojivit": "Kojic Acid + Arbutin + Vitamin C + Vitamin E",
    "lacto calamine": "Calamine + Zinc + Aloe Vera",

    # --- Eye / Ear Drops ---
    "moxifloxacin eye": "Moxifloxacin Eye Drops",
    "ciplox d": "Ciprofloxacin + Dexamethasone Eye Drops",
    "tobramycin": "Tobramycin Eye Drops",
    "tobrex": "Tobramycin Eye Drops",
    "genteal": "Hydroxypropyl Methylcellulose (Artificial Tears)",
    "refresh tears": "Carboxymethylcellulose (Artificial Tears)",
    "itone": "Herbal Eye Drops",

    # --- Muscle Relaxants ---
    "myospaz": "Chlorzoxazone + Paracetamol",
    "thiocolchicoside": "Thiocolchicoside",
    "myoril": "Thiocolchicoside",

    # --- Anti-anxiety / Neuro ---
    "librium": "Chlordiazepoxide",
    "calmpose": "Diazepam",
    "etizola": "Etizolam",

    # --- Antiseptics ---
    "dettol": "Chloroxylenol",
    "savlon": "Chlorhexidine Gluconate + Cetrimide",
    "hexidine": "Chlorhexidine Gluconate Mouthwash",
    "betadine gargle": "Povidone-Iodine Gargle",

    # --- Hormones / Gynec ---
    "duphaston": "Dydrogesterone",
    "primolut n": "Norethisterone",
    "regestrone": "Norethisterone",

    # --- Urology ---
    "urimax": "Tamsulosin",
    "urimax d": "Tamsulosin + Dutasteride",
    "dytor": "Torsemide",
    "lasix": "Furosemide",

    # --- Anti-parasitic ---
    "albendazole": "Albendazole",
    "zentel": "Albendazole",
    "bandy": "Albendazole",
    "ivermectin": "Ivermectin",

    # --- OTC / Personal Care ---
    "cetaphil": "Gentle Non-Comedogenic Cleanser",
    "moov": "Diclofenac Diethylamine + Linseed Oil + Menthol + Methyl Salicylate",
    "iodex": "Methyl Salicylate + Menthol",
    "zandu balm": "Menthol + Camphor + Methyl Salicylate",
    "amrutanjan": "Menthol + Camphor + Methyl Salicylate",
    "boroline": "Boric Acid Antiseptic Cream",
    "boroplus": "Antiseptic Cream",
    "himcolin": "Herbal (Jyotishmati + Lathakasthuri + Mukulaka)",
    "confido": "Herbal",
    "tentex": "Herbal",
    "himalaya liv 52": "Herbal Liver Tonic (Caper Bush + Chicory)",
    "liv 52": "Herbal Liver Tonic (Caper Bush + Chicory)",
    "cystone": "Herbal Kidney Stone (Pasanabheda + Shilapushpa)",

    # --- More Pharma (batch 2 — unmatched trade lines) ---
    "budamate": "Budesonide + Formoterol",
    "aerocort": "Levosalbutamol + Beclometasone",
    "ascoril": "Levosalbutamol + Ambroxol + Guaifenesin",
    "corex": "Chlorpheniramine + Codeine",
    "corex dx": "Chlorpheniramine + Dextromethorphan",
    "moxikind": "Amoxicillin + Clavulanic Acid",
    "moxikind cv": "Amoxicillin + Clavulanic Acid",
    "ceftum": "Cefuroxime Axetil",
    "tazloc": "Telmisartan + Amlodipine / Chlorthalidone",
    "corbis": "Bisoprolol",
    "storvas": "Atorvastatin",
    "nebicard": "Nebivolol",
    "gluconorm": "Glimepiride + Metformin / Voglibose",
    "gluconorm g": "Glimepiride + Metformin",
    "dynaglipt": "Teneligliptin",
    "pantakind": "Pantoprazole",
    "vomikind": "Ondansetron",
    "udiliv": "Ursodeoxycholic Acid (UDCA)",
    "zolfresh": "Zolpidem",
    "elocon": "Mometasone Furoate",
    "otrivin": "Xylometazoline Nasal",
    "electral": "ORS (Oral Rehydration Salts)",
    "lantus": "Insulin Glargine",
    "chymoral": "Trypsin + Chymotrypsin",
    "chymoral forte": "Trypsin + Chymotrypsin",
    "gabantip": "Gabapentin + Nortriptyline",
    "ondero": "Dapagliflozin",
    "caldikind": "Calcium + Vitamin D3 + Zinc",
    "calcium sandoz": "Calcium Gluconate",
    "cital": "Potassium Citrate + Citric Acid",
    "nicotex": "Nicotine Polacrilex",
    "ivrea": "Ketoconazole Shampoo",
    "salisia": "Salicylic Acid + Ketoconazole",
    "pyrimon": "Chloramphenicol + Dexamethasone Eye Drops",
    "cotaryl": "Clobetasol + Salicylic Acid",
    "khadirarishta": "Ayurvedic (Khadira + Triphala)",
    "maha sudarshan": "Ayurvedic (Sudarshan Churna)",
    "neo": "Herbal (Charak)",
    "nan": "Infant Milk Formula (Nestlé)",
    "cerelac": "Baby Cereal Nutrition (Nestlé)",

    # --- Sildenafil / Tadalafil ---
    "manforce": "Sildenafil Citrate / Condoms",

    # --- FMCG / Personal Care (category-level descriptions) ---
    "dabur": "Ayurvedic / Herbal (Dabur)",
    "patanjali": "Ayurvedic / Herbal (Patanjali)",
    "himalaya": "Herbal Healthcare (Himalaya)",
    "baidyanath": "Ayurvedic (Baidyanath)",
    "hamdard": "Unani / Herbal (Hamdard)",
    "johnsons": "Baby Care (Johnson & Johnson)",
    "johnson": "Baby Care (Johnson & Johnson)",
    "godrej": "Personal Care (Godrej)",
    "garnier": "Skin & Hair Care (Garnier)",
    "gillette": "Grooming & Shaving (Gillette)",
    "dove": "Personal Care (Dove)",
    "ponds": "Skin Care (Pond's)",
    "pond": "Skin Care (Pond's)",
    "colgate": "Oral Care (Colgate)",
    "sensodyne": "Potassium Nitrate + Sodium Fluoride Toothpaste",
    "bajaj": "Hair & Body Oil (Bajaj)",
    "vaseline": "Petroleum Jelly / Body Lotion (Vaseline)",
    "vicco": "Turmeric + Sandalwood (Vicco)",
    "pampers": "Baby Diapers (Pampers)",
    "mamy": "Baby Diapers (Mamy Poko)",
    "sofy": "Sanitary Pads (Sofy)",
    "whisper": "Sanitary Pads (Whisper)",
    "durex": "Condoms / Lubricants (Durex)",
    "pears": "Glycerine Soap (Pears)",
    "cinthol": "Deodorant Soap (Cinthol)",
    "lifebuoy": "Antibacterial Soap (Lifebuoy)",
    "hit": "Insecticide (Godrej HIT)",
    "harpic": "Bathroom Cleaner (Harpic)",
    "hansaplast": "Adhesive Bandages / First Aid (Hansaplast)",
    "bournvita": "Chocolate Health Drink (Bournvita)",
    "horlicks": "Health Drink (Horlicks)",
    "complan": "Nutrition Drink (Complan)",
    "veet": "Hair Removal Cream (Veet)",
    "lakme": "Beauty / Skincare (Lakmé)",
    "livon": "Hair Serum (Livon)",
    "emami": "Personal Care (Emami)",
    "nivea": "Skin Care (Nivea)",
    "abbott": "Healthcare (Abbott India)",
    "amul": "Dairy Nutrition (Amul)",
    "zandu": "Ayurvedic / Herbal (Zandu)",
    "doxolin": "Doxofylline",
}

def assign_salts():
    json_file = "shop_products_with_images.json"
    js_file = "product_data.js"

    with open(json_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    # Sort map keys longest-first so "pan d" matches before "pan"
    sorted_keys = sorted(SALT_MAP.keys(), key=len, reverse=True)

    updated = 0
    for p in products:
        pname = p["name"].lower()
        trade = (p.get("trade") or "").lower()

        salt = ""
        for key in sorted_keys:
            # Match trade line exactly, or product name starts with key
            if trade == key or pname.startswith(key + " ") or pname == key:
                salt = SALT_MAP[key]
                break
        p["salt"] = salt
        if salt:
            updated += 1

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    with open(js_file, "w", encoding="utf-8") as f:
        f.write("const shopProductsData = " + json.dumps(products, ensure_ascii=False) + ";\n")

    print(f"Assigned salt compositions to {updated} / {len(products)} products")

    # Show unmatched for review
    unmatched_trades = set()
    for p in products:
        if not p["salt"]:
            unmatched_trades.add(p.get("trade") or p["name"])
    print(f"\nUnmatched trade lines ({len(unmatched_trades)}):")
    for t in sorted(unmatched_trades)[:40]:
        print(f"  - {t}")
    if len(unmatched_trades) > 40:
        print(f"  ... and {len(unmatched_trades)-40} more")

if __name__ == "__main__":
    assign_salts()
