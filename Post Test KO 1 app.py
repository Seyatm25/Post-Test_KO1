import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Prediktor Uji Senyawa", page_icon="🧪", layout="centered")

# Custom CSS untuk kotak-kotak UI
st.markdown("""
    <style>
    .kotak {
        border: 2px solid #2ecc71;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #f9fbf9;
    }
    .label {
        font-weight: bold;
        color: #27ae60;
        font-size: 1.2em;
        margin-bottom: 5px;
        border-bottom: 2px solid #2ecc71;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Prediktor Uji Senyawa Organik")
st.write("Pilih senyawa dan pereaksi untuk melihat hasil uji laboratoriumnya.")

# ================= KOTAK INPUT (Bersebelahan) =================
col1, col2 = st.columns(2)

with col1:
    senyawa = st.selectbox("Senyawa", [
        "Alkohol Primer", 
        "Alkohol Sekunder", 
        "Alkohol Tersier", 
        "Formaldehida", 
        "Aseton", 
        "Heksana", 
        "Etil Asetat", 
        "Asam Asetat"
    ])

with col2:
    pereaksi = st.selectbox("Pereaksi", [
        "Oksidator (K2Cr2O7 / H+)", 
        "Pereaksi Lucas (ZnCl2 / HCl)", 
        "Pereaksi Tollens", 
        "Pereaksi Fehling",
        "Uji Iodoform (I2 / NaOH)",
        "Pereaksi Jones (CrO3 / H2SO4)",
        "Pereaksi Schiff",
        "Natrium Bisulfit (NaHSO3)",
        "Hidroksilamin (NH2OH)",
        "NaHCO3 + Uji Barit (Ba(OH)2)"
    ])

# ================= LOGIKA DATABASE REAKSI =================
# Default nilai jika tidak bereaksi
hasil = "(-) Tidak Bereaksi"
reaksi = "Tidak ada persamaan reaksi."
pembahasan = f"{senyawa} tidak bereaksi (negatif) dengan {pereaksi}."

# 1. K2Cr2O7
if pereaksi == "Oksidator (K2Cr2O7 / H+)":
    if senyawa in ["Alkohol Primer", "Alkohol Sekunder", "Formaldehida"]:
        hasil = "(+) Warna berubah jingga menjadi hijau"
        reaksi = "Cr₂O₇²⁻ (jingga) + Senyawa → Cr³⁺ (hijau) + Hasil Oksidasi"
        pembahasan = "Senyawa teroksidasi, mereduksi ion dikromat (jingga) menjadi ion krom(III) (hijau)."

# 2. LUCAS
elif pereaksi == "Pereaksi Lucas (ZnCl2 / HCl)":
    if senyawa == "Alkohol Tersier":
        hasil = "(+) Keruh seketika"
        reaksi = "R₃C-OH + HCl → R₃C-Cl↓ + H₂O"
        pembahasan = "Alkohol tersier sangat cepat membentuk alkil klorida yang tidak larut."
    elif senyawa == "Alkohol Sekunder":
        hasil = "(+) Keruh setelah 5-10 menit"
        reaksi = "R₂CH-OH + HCl → R₂CH-Cl↓ + H₂O"
        pembahasan = "Bereaksi lambat membentuk endapan alkil klorida."

# 3. TOLLENS
elif pereaksi == "Pereaksi Tollens":
    if senyawa == "Formaldehida":
        hasil = "(+) Terbentuk Cermin Perak"
        reaksi = "R-CHO + 2[Ag(NH₃)₂]⁺ + 3OH⁻ → R-COO⁻ + 2Ag↓ + 4NH₃ + 2H₂O"
        pembahasan = "Aldehid mereduksi ion perak menjadi logam perak murni di dinding kaca."

# 4. FEHLING
elif pereaksi == "Pereaksi Fehling":
    if senyawa == "Formaldehida":
        hasil = "(+) Terbentuk Endapan Merah Bata"
        reaksi = "R-CHO + 2Cu²⁺ + 5OH⁻ → R-COO⁻ + Cu₂O↓ (merah bata) + 3H₂O"
        pembahasan = "Aldehid mereduksi ion tembaga(II) biru menjadi endapan tembaga(I) oksida."

# 5. IODOFORM
elif pereaksi == "Uji Iodoform (I2 / NaOH)":
    if senyawa == "Aseton":
        hasil = "(+) Endapan Kuning Iodoform"
        reaksi = "CH₃-CO-CH₃ + 3I₂ + 4NaOH → CHI₃↓ (kuning) + CH₃COONa + 3NaI + 3H₂O"
        pembahasan = "Gugus metil keton pada aseton bereaksi membentuk kristal kuning iodoform (CHI₃)."
    elif senyawa == "Alkohol Sekunder":
        pembahasan = "Jika alkohol sekundernya memiliki gugus metil di ujung (seperti 2-propanol), hasilnya akan positif kuning. Jika tidak, maka negatif."

# 6. JONES
elif pereaksi == "Pereaksi Jones (CrO3 / H2SO4)":
    if senyawa in ["Alkohol Primer", "Alkohol Sekunder", "Formaldehida"]:
        hasil = "(+) Warna berubah merah-jingga ke hijau/biru-hijau"
        reaksi = "CrO₃ (jingga) + H₂SO₄ + Senyawa → Cr³⁺ (hijau) + Hasil Oksidasi"
        pembahasan = "Pereaksi Jones adalah oksidator kuat. Cr(VI) tereduksi menjadi Cr(III) berwarna hijau saat mengoksidasi alkohol/aldehid."

# 7. SCHIFF
elif pereaksi == "Pereaksi Schiff":
    if senyawa == "Formaldehida":
        hasil = "(+) Larutan berwarna Merah / Magenta (Fuksin)"
        reaksi = "Aldehid + Pereaksi Schiff → Kompleks warna magenta"
        pembahasan = "Uji sangat spesifik untuk aldehid. Aldehid memulihkan warna asli fuksin yang sebelumnya dihilangkan oleh SO₂."

# 8. NA-BISULFIT
elif pereaksi == "Natrium Bisulfit (NaHSO3)":
    if senyawa in ["Formaldehida", "Aseton"]:
        hasil = "(+) Endapan Putih Kristalin"
        reaksi = "R₂C=O + NaHSO₃ → R₂C(OH)SO₃Na↓ (kristal putih)"
        pembahasan = "Reaksi adisi nukleofilik pada gugus karbonil (aldehid/keton) membentuk garam bisulfit yang sukar larut."

# 9. HIDROKSILAMIN
elif pereaksi == "Hidroksilamin (NH2OH)":
    if senyawa in ["Formaldehida", "Aseton"]:
        hasil = "(+) Terbentuk Kristal Oksim"
        reaksi = "R₂C=O + NH₂OH → R₂C=N-OH (Oksim) + H₂O"
        pembahasan = "Gugus karbonil berkondensasi dengan hidroksilamin membentuk senyawa turunan oksim yang mengendap."

# 10. NaHCO3 + UJI BARIT
elif pereaksi == "NaHCO3 + Uji Barit (Ba(OH)2)":
    if senyawa == "Asam Asetat":
        hasil = "(+) Gelembung Gas & Air Barit Keruh (BaCO₃)"
        reaksi = "1) CH₃COOH + NaHCO₃ → CH₃COONa + H₂O + CO₂↑ \n2) CO₂ + Ba(OH)₂ → BaCO₃↓ (keruh) + H₂O"
        pembahasan = "Asam karboksilat melepaskan gas CO₂ saat ditambah NaHCO₃. Gas CO₂ ini bereaksi dengan uji barit menghasilkan endapan putih BaCO₃."


# ================= KOTAK OUTPUT BERDERET =================
st.write("---")

st.markdown(f"""
<div class="kotak">
    <div class="label">Hasil (+)/(-)</div>
    <p style="font-size: 1.1em; color: {'#d35400' if '(+)' in hasil else '#7f8c8d'};"><b>{hasil}</b></p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="kotak">
    <div class="label">Reaksi Kimia</div>
    <p style="font-size: 1.1em; font-family: monospace; white-space: pre-wrap;">{reaksi}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="kotak">
    <div class="label">Pembahasan Singkat</div>
    <p>{pembahasan}</p>
</div>
""", unsafe_allow_html=True)