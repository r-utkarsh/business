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
  {name:"Amul",logo:"logos/amul.png"},
  {name:"Apex Laboratories",logo:"logos/apex-laboratories.png"},
  {name:"Aristo Pharmaceuticals",logo:"logos/aristo-pharmaceuticals.png"},
  {name:"AstraZeneca India",logo:"logos/astrazeneca-india.png"},
  {name:"Baidyanath Jhansi",logo:"logos/baidyanath-jhansi.png"},
  {name:"Bajaj Healthcare",logo:"logos/bajaj-healthcare.png"},
  {name:"Bayer Pharmaceuticals",logo:"logos/bayer-pharmaceuticals.png"},
  {name:"Biological E",logo:"logos/biological-e.png"},
  {name:"Blue Cross Laboratories",logo:"logos/blue-cross-laboratories.png"},
  {name:"Bournvita",logo:"logos/bournvita.png"},
  {name:"Cadila Pharmaceuticals",logo:"logos/cadila-pharmaceuticals.png"},
  {name:"Centaur Pharmaceuticals",logo:"logos/centaur-pharmaceuticals.png"},
  {name:"Cetaphil",logo:"logos/cetaphil.png"},
  {name:"Charak Pharma",logo:"logos/charak-pharma.png"},
  {name:"Cipla",logo:"logos/cipla.png"},
  {name:"Cipla Health",logo:"logos/cipla-health.png"},
  {name:"Closeup",logo:"logos/closeup.png"},
  {name:"Colgate",logo:"logos/colgate-palmolive.png"},
  {name:"Complan",logo:"logos/complan.png"},
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
  {name:"Fair and Handsome",logo:"logos/fair-and-handsome.png"},
  {name:"FDC",logo:"logos/fdc.png"},
  {name:"Franco-Indian Pharmaceuticals",logo:"logos/franco-indian-pharmaceuticals.png"},
  {name:"GSK India",logo:"logos/gsk-india.png"},
  {name:"Galderma India",logo:"logos/galderma-india.png"},
  {name:"Garnier",logo:"logos/garnier.png"},
  {name:"Gillette",logo:"logos/gillette.png"},
  {name:"Glenmark Pharmaceuticals",logo:"logos/glenmark-pharmaceuticals.png"},
  {name:"Glow & Lovely",logo:"logos/glow-lovely.png"},
  {name:"Godrej Products",logo:"logos/godrej-consumer-products.png"},
  {name:"HIT",logo:"logos/hit.png"},
  {name:"Hamdard Dawakhana",logo:"logos/hamdard-dawakhana.png"},
  {name:"Hansaplast",logo:"logos/hansaplast.png"},
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
  {name:"Jagsonpal Pharmaceuticals",logo:"logos/jagsonpal-pharmaceuticals.png"},
  {name:"Johnson & Johnson",logo:"logos/johnson-johnson.png"},
  {name:"Jubilant Generics",logo:"logos/jubilant-generics.png"},
  {name:"Jubilant Pharmova",logo:"logos/jubilant-pharmova.png"},
  {name:"Kesh King",logo:"logos/kesh-king.png"},
  {name:"Khadi Natural",logo:"logos/khadi-natural.png"},
  {name:"Lakmé",logo:"logos/lakm.png"},
  {name:"Leeford",logo:"logos/leeford.png"},
  {name:"Lifebuoy",logo:"logos/lifebuoy.png"},
  {name:"Lotus Herbals",logo:"logos/lotus-herbals.png"},
  {name:"Lupin",logo:"logos/lupin.png"},
  {name:"Macleods Pharmaceuticals",logo:"logos/macleods-pharmaceuticals.png"},
  {name:"Mamaearth",logo:"logos/mamaearth.png"},
  {name:"MamyPoko",logo:"logos/mamypoko.png"},
  {name:"Mankind Pharma",logo:"logos/mankind-pharma.png"},
  {name:"Marico",logo:"logos/marico.png"},
  {name:"Merck India",logo:"logos/merck-india.png"},
  {name:"Meswak",logo:"logos/meswak.png"},
  {name:"Meyer Organics",logo:"logos/meyer-organics.png"},
  {name:"Micro Labs",logo:"logos/micro-labs.png"},
  {name:"Navratna",logo:"logos/navratna.png"},
  {name:"Nestle India Ltd",logo:"logos/nestl-health-science-india.png"},
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
  {name:"Pears",logo:"logos/pears.png"},
  {name:"Pepsodent",logo:"logos/pepsodent.png"},
  {name:"Pfizer India",logo:"logos/pfizer-india.png"},
  {name:"Piramal Pharma",logo:"logos/piramal-pharma.png"},
  {name:"Plethico Pharmaceuticals",logo:"logos/plethico-pharmaceuticals.png"},
  {name:"Pond's",logo:"logos/pond-s.png"},
  {name:"Procter & Gamble",logo:"logos/procter-gamble.png"},
  {name:"Reckitt",logo:"logos/reckitt.webp"},
  {name:"RPG Life Sciences",logo:"logos/rpg-life-sciences.jpg"},
  {name:"Sandoz India",logo:"logos/sandoz-india.png"},
  {name:"Sanofi India",logo:"logos/sanofi-india.png"},
  {name:"Savlon",logo:"logos/savlon.png"},
  {name:"Sensodyne",logo:"logos/sensodyne.png"},
  {name:"Set Wet",logo:"logos/set-wet.png"},
  {name:"Sofy",logo:"logos/sofy.png"},
  {name:"Streax",logo:"logos/streax.png"},
  {name:"Sun Pharmaceutical",logo:"logos/sun-pharmaceutical-industries.png"},
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

brandData.sort((a, b) => a.name.localeCompare(b.name));
const brands = brandData.map(b => b.name);
const brandLogoMap = {};
brandData.forEach(b => { brandLogoMap[b.name] = b.logo; });

function getBrandLogo(brandName) {
  if (!brandName) return '';
  if (brandLogoMap[brandName]) return brandLogoMap[brandName];
  const norm = brandName.toLowerCase().replace(/[^a-z0-9]/g, '');
  for (const b in brandLogoMap) {
    const bNorm = b.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (bNorm && (norm.includes(bNorm) || bNorm.includes(norm))) {
      return brandLogoMap[b];
    }
  }
  return '';
}

let products = (typeof shopProductsData !== 'undefined' && shopProductsData.length > 0)
  ? shopProductsData.map(p => ({
      name: p.name,
      brand: p.brand,
      trade: p.trade,
      salt: p.salt || '',
      category: p.trade || p.brand,
      icon: '💊',
      image: p.image
    }))
  : [];

const $ = id => document.getElementById(id);
const esc = s => (s||'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
const safeImagePath = path => /^product_images\/[a-z0-9][a-z0-9-]*\.(?:jpe?g|png|webp)$/i.test(path || '') ? path : '';
document.addEventListener('error', e => { if (e.target.tagName === 'IMG') { e.target.style.display = 'none'; const sib = e.target.nextElementSibling; if (sib) sib.style.display = 'grid'; } }, true);
let brandLimit = 18;
let productLimit = 24;
let activeLetter = '';

function brandCard(name) {
  const logo = brandLogoMap[name];
  const initials = name.replace(/[^A-Za-z]/g,'').slice(0,2).toUpperCase();
  const logoHtml = logo
    ? `<img src="${logo}" alt="${esc(name)}">`
    : '';
  const fallbackStyle = logo ? 'display:none' : 'display:grid';
  return `<article class="brand-card">${logoHtml}<span class="brand-mark" style="${fallbackStyle}">${esc(initials)}</span><strong>${esc(name)}</strong></article>`;
}

function renderBrands() {
  const term = $('brandSearch').value.toLowerCase();
  const filtered = brands.filter(b => b.toLowerCase().includes(term) && (!activeLetter || b[0].toUpperCase() === activeLetter));
  const shown = filtered.slice(0, brandLimit);
  $('brandGrid').innerHTML = shown.map(brandCard).join('');
  $('brandCount').textContent = `${filtered.length} brand${filtered.length === 1 ? '' : 's'} found`;
  $('loadMore').style.display = shown.length >= filtered.length ? 'none' : '';
}



function productCard(p) {
  const logo = getBrandLogo(p.brand);
  const image = safeImagePath(p.image);
  let imgHtml = '';
  if (image) {
    imgHtml = `<img src="${image}" alt="${esc(p.name)}" loading="lazy" />`;
  }
  const logoFallback = logo
    ? `<img src="${logo}" alt="${esc(p.brand)}" style="max-width:80px;max-height:80px;object-fit:contain;" />`
    : `<span style="font-size:32px">${p.icon}</span>`;
  const fallbackStyle = image ? 'display:none' : 'display:grid';
  return `<article class="product-card"><div class="product-image">${imgHtml}<div style="${fallbackStyle};place-items:center;width:100%;height:100%">${logoFallback}</div></div><p class="brand-label">${esc(p.brand)}</p><strong>${esc(p.name)}</strong></article>`;
}

function renderProducts() {
  const term = $('productSearch').value.toLowerCase().trim();
  const filtered = products.filter(p => !term || `${p.name} ${p.brand} ${p.category} ${p.trade || ''}`.toLowerCase().includes(term));
  const shown = filtered.slice(0, productLimit);
  $('productGrid').innerHTML = shown.map(productCard).join('');
  $('productCount').textContent = `${filtered.length} product${filtered.length === 1 ? '' : 's'} available in store`;
  $('noProducts').classList.toggle('hidden', filtered.length !== 0);
  if ($('loadMoreProducts')) {
    $('loadMoreProducts').style.display = shown.length >= filtered.length ? 'none' : '';
  }
}

function showPage(page) {
  document.querySelectorAll('.page').forEach(s=>s.classList.toggle('active',s.id===page));
  document.querySelectorAll('.nav-link').forEach(b=>b.classList.toggle('active',b.dataset.page===page));
  window.scrollTo(0,0);
}

document.querySelectorAll('.search-field input').forEach(input => {
  input.addEventListener('focus', () => {
    const field = input.closest('.search-field');
    if (field) {
      setTimeout(() => field.scrollIntoView({behavior:'smooth', block:'start'}), 50);
    }
  });
});

document.querySelectorAll('.nav-link').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.page)));
document.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.go)));

$('featuredBrands').innerHTML = ['Dabur India', 'Himalaya', 'Abbott India', 'Cipla', 'Mankind Pharma', 'Sun Pharmaceutical'].filter(b=>brands.includes(b)).map(brandCard).join('');
$('alphabet').innerHTML = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(letter=>`<button aria-label="Brands starting with ${letter}">${letter}</button>`).join('');

$('alphabet').addEventListener('click',e=>{ if(e.target.tagName !== 'BUTTON') return; activeLetter = activeLetter === e.target.textContent ? '' : e.target.textContent; document.querySelectorAll('.alphabet button').forEach(b=>b.classList.toggle('active',b.textContent===activeLetter)); brandLimit=18; renderBrands(); });

$('brandSearch').addEventListener('input',()=>{ activeLetter=''; brandLimit=18; renderBrands(); });
$('loadMore').addEventListener('click',()=>{brandLimit+=20;renderBrands();});
$('productSearch').addEventListener('input',()=>{ productLimit=24; renderProducts(); });
if ($('loadMoreProducts')) $('loadMoreProducts').addEventListener('click',()=>{ productLimit+=24; renderProducts(); });

// --- Salt / Composition Search ---
let saltLimit = 24;
const popularSalts = [
  'Paracetamol','Pantoprazole','Cetirizine','Azithromycin','Amoxicillin',
  'Metformin','Dapagliflozin','Telmisartan','Amlodipine','Levothyroxine Sodium',
  'Atorvastatin','Diclofenac','Omeprazole','Montelukast','Calcium + Vitamin D3',
  'Vitamin B1 + B6 + B12','Povidone-Iodine','Clopidogrel','Aspirin','Budesonide'
];

function renderSaltTags() {
  if (!$('saltTags')) return;
  $('saltTags').innerHTML = popularSalts.map(s => `<span class="salt-tag" role="button" tabindex="0">${s}</span>`).join('');
}

function renderSalts() {
  if (!$('saltSearch')) return;
  const term = $('saltSearch').value.toLowerCase().trim();
  const filtered = products.filter(p => {
    const salt = (p.salt || '').toLowerCase();
    return salt && (!term || salt.includes(term));
  });
  const shown = filtered.slice(0, saltLimit);
  $('saltGrid').innerHTML = shown.map(p => {
    const card = productCard(p);
    return card.replace('</article>', `<p class="salt-label">${esc(p.salt)}</p></article>`);
  }).join('');
  $('saltCount').textContent = term
    ? `${filtered.length} product${filtered.length === 1 ? '' : 's'} matching "${$('saltSearch').value.trim()}"`
    : `Type a salt name above or tap a popular salt badge`;
  $('noSalts').classList.toggle('hidden', filtered.length !== 0 || !term);
  if ($('loadMoreSalts')) $('loadMoreSalts').style.display = shown.length >= filtered.length ? 'none' : '';
}

renderSaltTags();

if ($('saltTags')) $('saltTags').addEventListener('click', e => {
  if (!e.target.classList.contains('salt-tag')) return;
  $('saltSearch').value = e.target.textContent;
  saltLimit = 24;
  renderSalts();
});

$('saltSearch').addEventListener('input', () => { saltLimit = 24; renderSalts(); });
if ($('loadMoreSalts')) $('loadMoreSalts').addEventListener('click', () => { saltLimit += 24; renderSalts(); });

renderBrands();
renderProducts();
renderSalts();
