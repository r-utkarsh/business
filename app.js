const brandData = [
  {name:"Abbott India",logo:"logos/abbott-india.png"},
  {name:"AcneStar",logo:"logos/acnestar.png"},
  {name:"Aimil Pharmaceuticals",logo:"logos/aimil-pharmaceuticals.png"},
  {name:"Ajanta Pharma",logo:"logos/ajanta-pharma.png"},
  {name:"Akums Drugs & Pharmaceuticals",logo:"logos/akums-drugs-pharmaceuticals.png"},
  {name:"Al-Shifa",logo:"logos/al-shifa.png"},
  {name:"Alembic Pharmaceuticals",logo:"logos/alembic-pharmaceuticals.png"},
  {name:"Alkem Laboratories",logo:"logos/alkem-laboratories.png"},
  {name:"Ami Organics",logo:"logos/ami-organics.png"},
  {name:"Aristo Pharmaceuticals",logo:"logos/aristo-pharmaceuticals.png"},
  {name:"AstraZeneca India",logo:"logos/astrazeneca-india.png"},
  {name:"Baidyanath Jhansi",logo:"logos/baidyanath-jhansi.png"},
  {name:"Bajaj Healthcare",logo:"logos/bajaj-healthcare.png"},
  {name:"Bayer Pharmaceuticals",logo:"logos/bayer-pharmaceuticals.png"},
  {name:"Biological E",logo:"logos/biological-e.png"},
  {name:"Blue Cross Laboratories",logo:"logos/blue-cross-laboratories.png"},
  // {name:"BoroPlus",logo:"logos/boroplus.png"},
  {name:"Cadila Pharmaceuticals",logo:"logos/cadila-pharmaceuticals.png"},
  {name:"Centaur Pharmaceuticals",logo:"logos/centaur-pharmaceuticals.png"},
  {name:"Cetaphil",logo:"logos/cetaphil.png"},
  {name:"Charak Pharma",logo:"logos/charak-pharma.png"},
  // {name:"Cinthol",logo:"logos/cinthol.png"},
  {name:"Cipla",logo:"logos/cipla.png"},
  {name:"Cipla Health",logo:"logos/cipla-health.png"},
  // {name:"Clinic Plus",logo:"logos/clinic-plus.png"},
  {name:"Closeup",logo:"logos/closeup.png"},
  {name:"Colgate",logo:"logos/colgate-palmolive.png"},
  // {name:"Colgate-Palmolive",logo:"logos/colgate-palmolive.png"},
  {name:"Corona Remedies",logo:"logos/corona-remedies.png"},
  {name:"Dabur India",logo:"logos/dabur-india.png"},
  {name:"Dawakhana Tibbiya College",logo:"logos/dawakhana-tibbiya-college.png"},
  {name:"Dey's Medical",logo:"logos/dey-s-medical.png"},
  {name:"Dove",logo:"logos/dove.png"},
  {name:"Dr. Reddy's Laboratories",logo:"logos/dr-reddy-s-laboratories.png"},
  {name:"Dr. Willmar Schwabe India",logo:"logos/dr-willmar-schwabe-india.png"},
  {name:"East India Pharmaceutical Works",logo:"logos/east-india-pharmaceutical-works.png"},
  {name:"Elder Pharmaceuticals",logo:"logos/elder-pharmaceuticals.png"},
  {name:"Emami",logo:"logos/emami.png"},
  {name:"Emcure Pharmaceuticals",logo:"logos/emcure-pharmaceuticals.png"},
  {name:"Eris Lifesciences",logo:"logos/eris-lifesciences.png"},
  {name:"FDC",logo:"logos/fdc.png"},
  {name:"Fair & Lovely",logo:"logos/glow-lovely.png"},
  {name:"Fair and Handsome",logo:"logos/fair-and-handsome.png"},
  {name:"Franco-Indian Pharmaceuticals",logo:"logos/franco-indian-pharmaceuticals.png"},
  // {name:"Fulford India",logo:""},
  {name:"GSK India",logo:"logos/gsk-india.png"},
  {name:"Galderma India",logo:"logos/galderma-india.png"},
  {name:"Garnier",logo:"logos/garnier.png"},
  {name:"Gillette",logo:"logos/gillette.png"},
  {name:"Glenmark Pharmaceuticals",logo:"logos/glenmark-pharmaceuticals.png"},
  {name:"Glow & Lovely",logo:"logos/glow-lovely.png"},
  {name:"Godrej Consumer Products",logo:"logos/godrej-consumer-products.png"},
  {name:"Godrej No. 1",logo:"logos/godrej-no-1.png"},
  {name:"HIT",logo:"logos/hit.png"},
  {name:"Hamdard Dawakhana",logo:"logos/hamdard-dawakhana.png"},
  {name:"Head & Shoulders",logo:"logos/head-shoulders.png"},
  {name:"Himalaya",logo:"logos/himalaya.png"},
  {name:"Himalaya Wellness",logo:"logos/himalaya-wellness.png"},
  {name:"Hindustan Antibiotics",logo:"logos/hindustan-antibiotics.png"},
  {name:"Hindustan Unilever",logo:"logos/hindustan-unilever.png"},
  {name:"Ind-Swift Laboratories",logo:"logos/ind-swift-laboratories.png"},
  {name:"Indoco Remedies",logo:"logos/indoco-remedies.png"},
  {name:"Indulekha",logo:"logos/indulekha.png"},
  {name:"Intas Pharmaceuticals",logo:"logos/intas-pharmaceuticals.png"},
  {name:"Ipca Laboratories",logo:"logos/ipca-laboratories.png"},
  {name:"JB. Chemicals & Pharmaceuticals",logo:"logos/j-b-chemicals-pharmaceuticals.png"},
  // {name:"JB Chemicals & Pharmaceuticals",logo:"logos/jb-chemicals-pharmaceuticals.png"},
  {name:"Jagsonpal Pharmaceuticals",logo:"logos/jagsonpal-pharmaceuticals.png"},
  {name:"Johnson & Johnson",logo:"logos/johnson-johnson.png"},
  {name:"Jubilant Generics",logo:"logos/jubilant-generics.png"},
  {name:"Jubilant Pharmova",logo:"logos/jubilant-pharmova.png"},
  {name:"Kesh King",logo:"logos/kesh-king.png"},
  {name:"Khadi Natural",logo:"logos/khadi-natural.png"},
  {name:"Lakmé",logo:"logos/lakm.png"},
  {name:"Leeford",logo:"logos/leeford.png"},
  {name:"Lifebuoy",logo:"logos/lifebuoy.png"},
  // {name:"Livon",logo:"logos/livon.png"},
  {name:"Lotus Herbals",logo:"logos/lotus-herbals.png"},
  {name:"Lupin",logo:"logos/lupin.png"},
  {name:"Macleods Pharmaceuticals",logo:"logos/macleods-pharmaceuticals.png"},
  {name:"Mamaearth",logo:"logos/mamaearth.png"},
  {name:"Mankind Pharma",logo:"logos/mankind-pharma.png"},
  {name:"Marico",logo:"logos/marico.png"},
  {name:"Merck India",logo:"logos/merck-india.png"},
  {name:"Meswak",logo:"logos/meswak.png"},
  {name:"Meyer Organics",logo:"logos/meyer-organics.png"},
  {name:"Micro Labs",logo:"logos/micro-labs.png"},
  {name:"Navratna",logo:"logos/navratna.png"},
  {name:"Nestlé Health Science India",logo:"logos/nestl-health-science-india.png"},
  // {name:"Nihar Naturals",logo:"logos/nihar-naturals.png"},
  {name:"Nivea",logo:"logos/nivea.png"},
  {name:"Novartis India",logo:"logos/novartis-india.png"},
  {name:"Old Spice",logo:"logos/old-spice.png"},
  {name:"Oral-B",logo:"logos/oral-b.png"},
  {name:"P&G",logo:"logos/p-g.png"},
  {name:"Pampers",logo:"logos/pampers.png"},
  {name:"Panacea Biotec",logo:"logos/panacea-biotec.png"},
  {name:"Pantene",logo:"logos/pantene.png"},
  {name:"Parachute",logo:"logos/parachute.png"},
  {name:"Patanjali Ayurved",logo:"logos/patanjali-ayurved.png"},
  {name:"Patanjali Wellness",logo:"logos/patanjali-wellness.png"},
  {name:"Pepsodent",logo:"logos/pepsodent.png"},
  {name:"Pfizer India",logo:"logos/pfizer-india.png"},
  {name:"Piramal Pharma",logo:"logos/piramal-pharma.png"},
  {name:"Plethico Pharmaceuticals",logo:"logos/plethico-pharmaceuticals.png"},
  {name:"Pond's",logo:"logos/pond-s.png"},
  {name:"Procter & Gamble",logo:"logos/procter-gamble.png"},
  {name:"RPG Life Sciences",logo:"logos/rpg-life-sciences.jpg"},
  {name:"Sandoz India",logo:"logos/sandoz-india.png"},
  {name:"Sanofi India",logo:"logos/sanofi-india.png"},
  {name:"Sensodyne",logo:"logos/sensodyne.png"},
  {name:"Set Wet",logo:"logos/set-wet.png"},
  {name:"Streax",logo:"logos/streax.png"},
  {name:"Sun Pharmaceutical Industries",logo:"logos/sun-pharmaceutical-industries.png"},
  {name:"Sunsilk",logo:"logos/sunsilk.png"},
  {name:"Systopic Laboratories",logo:"logos/systopic-laboratories.png"},
  {name:"TTK Healthcare",logo:"logos/ttk-healthcare.png"},
  {name:"Torrent Pharmaceuticals",logo:"logos/torrent-pharmaceuticals.png"},
  {name:"Tresemmé",logo:"logos/tresemm.png"},
  {name:"Troikaa Pharmaceuticals",logo:"logos/troikaa-pharmaceuticals.png"},
  {name:"USV",logo:"logos/usv.png"},
  {name:"Unichem Laboratories",logo:"logos/unichem-laboratories.jpg"},
  {name:"Vaseline",logo:"logos/vaseline.png"},
  {name:"Vicco Laboratories",logo:"logos/vicco-laboratories.png"},
  {name:"Wallace Pharmaceuticals",logo:"logos/wallace-pharmaceuticals.png"},
  {name:"Walter Bushnell",logo:"logos/walter-bushnell.png"},
  {name:"Wanbury",logo:"logos/wanbury.png"},
  {name:"Whisper",logo:"logos/whisper.png"},
  {name:"Win-Medicare",logo:"logos/win-medicare.png"},
  {name:"Zandu",logo:"logos/zandu.png"},
  {name:"Zinda Tilismath",logo:"logos/zinda-tilismath.png"},
  {name:"Zuventus Healthcare",logo:"logos/zuventus-healthcare.png"},
  {name:"Zydus Lifesciences",logo:"logos/zydus-lifesciences.png"},
  {name:"Zydus Wellness",logo:"logos/zydus-wellness.png"}
];
const brands = brandData.map(b => b.name);
const brandLogoMap = {};
brandData.forEach(b => { brandLogoMap[b.name] = b.logo; });

let products = [
  ['Pampers Active Baby Diapers','Pampers','Baby care','👶'],['Himalaya Baby Lotion','Himalaya','Baby care','🧴'],['Cetaphil Gentle Skin Cleanser','Cetaphil','Personal care','🫧'],['Dettol Antiseptic Liquid','Dettol','First aid','🩹'],['Dabur Chyawanprash','Dabur','Wellness','🍯'],['Ensure Nutrition Powder','Abbott','Nutrition','🥛'],['Colgate Strong Teeth Toothpaste','Colgate','Personal care','🪥'],['Accu-Chek Active Test Strips','Accu-Chek','Devices','🩸'],['Vicks Vaporub','Vicks','Wellness','🌿'],['Johnson\'s Baby Shampoo','Johnson\'s','Baby care','🛁'],['Dr. Morepen Blood Pressure Monitor','Dr. Morepen','Devices','🩺'],['Savlon Hand Sanitizer','Savlon','Personal care','🧼']
].map(([name,brand,category,icon])=>({name,brand,category,icon}));

const $ = id => document.getElementById(id);
let brandLimit = 18;
let activeLetter = '';

function brandCard(name) {
  const logo = brandLogoMap[name];
  const initials = name.replace(/[^A-Za-z]/g,'').slice(0,2).toUpperCase();
  const logoHtml = logo
    ? `<img src="${logo}" alt="${name}" style="max-width:43px;max-height:43px;object-fit:contain;" onerror="this.style.display='none';this.nextElementSibling.style.display='grid'">`
    : '';
  const fallbackStyle = logo ? 'display:none' : 'display:grid';
  return `<article class="brand-card">${logoHtml}<span class="brand-mark" style="${fallbackStyle}">${initials}</span><strong>${name}</strong></article>`;
}

function renderBrands() {
  const term = $('brandSearch').value.toLowerCase();
  const filtered = brands.filter(b => b.toLowerCase().includes(term) && (!activeLetter || b[0].toUpperCase() === activeLetter));
  const shown = filtered.slice(0, brandLimit);
  $('brandGrid').innerHTML = shown.map(brandCard).join('');
  $('brandCount').textContent = `${filtered.length} brand${filtered.length === 1 ? '' : 's'} found`;
  $('loadMore').hidden = shown.length >= filtered.length;
}

function renderProducts() {
  const term = $('productSearch').value.toLowerCase().trim();
  const shown = products.filter(p => !term || `${p.name} ${p.brand} ${p.category}`.toLowerCase().includes(term));
  $('productGrid').innerHTML = shown.map(p => `<article class="product-card"><div class="product-image">${p.image ? `<img src="${p.image}" alt="" />` : p.icon}</div><p class="brand-label">${p.brand}</p><strong>${p.name}</strong></article>`).join('');
  $('productCount').textContent = `${shown.length} product${shown.length === 1 ? '' : 's'} shown`;
  $('noProducts').classList.toggle('hidden', shown.length !== 0);
}

function showPage(page) {
  document.querySelectorAll('.page').forEach(s=>s.classList.toggle('active',s.id===page));
  document.querySelectorAll('.nav-link').forEach(b=>b.classList.toggle('active',b.dataset.page===page));
  window.scrollTo(0,0);
}

document.querySelectorAll('.nav-link').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.page)));
document.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.go)));

$('featuredBrands').innerHTML = brands.slice(0,6).map(brandCard).join('');
$('alphabet').innerHTML = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(letter=>`<button aria-label="Brands starting with ${letter}">${letter}</button>`).join('');

$('alphabet').addEventListener('click',e=>{ if(e.target.tagName !== 'BUTTON') return; activeLetter = activeLetter === e.target.textContent ? '' : e.target.textContent; document.querySelectorAll('.alphabet button').forEach(b=>b.classList.toggle('active',b.textContent===activeLetter)); brandLimit=18; renderBrands(); });

$('brandSearch').addEventListener('input',()=>{ activeLetter=''; brandLimit=18; renderBrands(); });
$('loadMore').addEventListener('click',()=>{brandLimit+=20;renderBrands();});
$('productSearch').addEventListener('input',renderProducts);

$('productForm').addEventListener('submit',e=>{ e.preventDefault(); const data = new FormData(e.currentTarget); const file=data.get('image'); const add = image => { products.unshift({name:data.get('name'),brand:data.get('brand'),category:data.get('category'),icon:'📦',image}); if(!brands.includes(data.get('brand'))) brands.push(data.get('brand')); renderProducts(); e.currentTarget.reset(); showPage('products'); }; if(file && file.size) { const reader=new FileReader(); reader.onload=()=>add(reader.result); reader.readAsDataURL(file); } else add(''); });

renderBrands();
renderProducts();
