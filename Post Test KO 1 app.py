import streamlit as st

# ================= KONFIGURASI HALAMAN =================
# Mengubah layout menjadi "wide" agar seperti dashboard modern
st.set_page_config(page_title="Prediktor Uji Senyawa Organik", page_icon="🧪", layout="wide")

# ================= KUSTOMISASI CSS (UI/UX) =================
st.markdown("""
    <style>
    /* Mengubah warna background utama agar lebih soft */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Desain Kartu (Card) Modern */
    .modern-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 6px solid #10b981;
        transition: transform 0.2s ease-in-out;
    }
    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    /* Kartu khusus hasil Negatif */
    .card-negative { border-left: 6px solid #ef4444; }
    
    /* Tipografi Judul dalam Kartu */
    .card-title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #64748b;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    /* Teks Hasil Utama */
    .card-content {
        font-size: 1.25em;
        color: #1e293b;
        font-weight: 500;
        line-height: 1.6;
    }
    
    /* Font monospace khusus untuk reaksi kimia */
    .chemical-reaction {
        font-family: 'Courier New', Courier, monospace;
        background-color: #f1f5f9;
        padding: 10px 15px;
        border-radius: 8px;
        color: #0f172a;
        font-weight: bold;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# ================= SIDEBAR (MENU NAVIGASI USER FRIENDLY) =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1046/1046374.png", width=80)
    st.title("Panel Kendali")
    st.write("Pilih parameter di bawah ini untuk memulai simulasi laboratorium.")
    st.divider()
    
    # Input diletakkan di sidebar agar rapi
    senyawa = st.selectbox("1️⃣ Pilih Senyawa:", [
        "Alkohol Primer", "Alkohol Sekunder", "Alkohol Tersier", 
        "Formaldehida", "Aseton", "Heksana", "Etil Asetat", "Asam Asetat"
    ])
    
    pereaksi = st.selectbox("2️⃣ Pilih Pereaksi:", [
        "Oksidator (K2Cr2O7 / H+)", "Pereaksi Lucas (ZnCl2 / HCl)", 
        "Pereaksi Tollens", "Pereaksi Fehling", "Uji Iodoform (I2 / NaOH)",
        "Pereaksi Jones (CrO3 / H2SO4)", "Pereaksi Schiff",
        "Natrium Bisulfit (NaHSO3)", "Hidroksilamin (NH2OH)",
        "NaHCO3 + Uji Barit (Ba(OH)2)", "Uji Ceric Nitrat"
    ])
    
    st.divider()
    st.caption("Dibuat untuk keperluan praktikum & pembelajaran Kimia Organik.")

# ================= HEADER UTAMA =================
st.title("🧪 AI Chemical Reaction Predictor")
st.write("Aplikasi cerdas untuk memprediksi hasil uji kualitatif senyawa organik beserta analisis mekanismenya.")

# Membuat TABS agar tampilan tidak menumpuk (User Friendly)
tab1, tab2 = st.tabs(["🎯 Simulasi Uji Reaksi", "📖 Teori Dasar & Panduan"])

# ================= TAB 1: SIMULASI UJI (LOGIKA UTAMA) =================
with tab1:
    # Logika Default
    hasil = "(-) Tidak Bereaksi"
    reaksi = "Tidak ada persamaan reaksi."
    pembahasan = ""
    is_positive = False # Indikator untuk warna UI nanti

    def alasan_negatif_umum(senyawa):
        if senyawa == "Heksana": return "Heksana adalah alkana rantai lurus (non-polar dan jenuh) yang sangat stabil dan tidak memiliki gugus fungsi reaktif."
        if senyawa == "Etil Asetat": return "Etil asetat adalah ester yang cukup stabil. Gugus karbonilnya terstabilkan oleh resonansi sehingga kurang reaktif terhadap pereaksi ini."
        return f"{senyawa} tidak memiliki gugus fungsi yang sesuai untuk berinteraksi dengan pereaksi ini."

    # 1. K2Cr2O7
    if pereaksi == "Oksidator (K2Cr2O7 / H+)":
        if senyawa in ["Alkohol Primer", "Alkohol Sekunder", "Formaldehida"]:
            hasil = "(+) Warna berubah jingga menjadi hijau"
            reaksi = "Cr₂O₇²⁻ (jingga) + Senyawa → Cr³⁺ (hijau) + Hasil Oksidasi"
            pembahasan = "✅ **Kenapa bereaksi:** Senyawa ini memiliki atom Hidrogen yang terikat pada atom Karbon pembawa gugus fungsi, sehingga dapat dioksidasi. Ion dikromat (jingga) tereduksi menjadi ion Cr³⁺ (hijau)."
            is_positive = True
        elif senyawa == "Alkohol Tersier":
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Karbon yang mengikat gugus -OH pada alkohol tersier tidak memiliki atom hidrogen (hidrogen alfa) sama sekali, sehingga ikatan C-C harus diputus untuk oksidasi, yang mana tidak bisa dilakukan oleh dikromat."
        elif senyawa in ["Aseton", "Asam Asetat"]:
            pembahasan = f"❌ **Kenapa TIDAK bereaksi:** {senyawa} sudah berada pada tingkat oksidasi yang tinggi (karbonil keton/asam karboksilat stabil) sehingga tidak dapat dioksidasi lebih lanjut oleh oksidator sedang."
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** " + alasan_negatif_umum(senyawa)

    # 2. LUCAS
    elif pereaksi == "Pereaksi Lucas (ZnCl2 / HCl)":
        if senyawa == "Alkohol Tersier":
            hasil = "(+) Keruh seketika"
            reaksi = "R₃C-OH + HCl → R₃C-Cl↓ + H₂O"
            pembahasan = "✅ **Kenapa bereaksi:** Alkohol tersier sangat mudah mengalami reaksi substitusi nukleofilik (SN1) karena membentuk karbokation tersier yang sangat stabil, langsung menghasilkan alkil klorida yang tak larut air."
            is_positive = True
        elif senyawa == "Alkohol Sekunder":
            hasil = "(+) Keruh setelah 5-10 menit"
            reaksi = "R₂CH-OH + HCl → R₂CH-Cl↓ + H₂O"
            pembahasan = "✅ **Kenapa bereaksi:** Reaksi berjalan lambat melalui mekanisme SN1 karena karbokation sekunder kurang stabil dibanding tersier. Butuh waktu untuk menghasilkan endapan alkil klorida."
            is_positive = True
        elif senyawa == "Alkohol Primer":
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Karbokation primer sangat tidak stabil. Tanpa pemanasan ekstrem, alkohol primer tidak akan bereaksi dengan pereaksi Lucas."
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Pereaksi Lucas dirancang khusus untuk mensubstitusi gugus hidroksil (-OH) pada alkohol. Senyawa ini tidak memiliki gugus -OH alkoholik bebas."

    # 3. TOLLENS
    elif pereaksi == "Pereaksi Tollens":
        if senyawa == "Formaldehida":
            hasil = "(+) Terbentuk Cermin Perak"
            reaksi = "R-CHO + 2[Ag(NH₃)₂]⁺ + 3OH⁻ → R-COO⁻ + 2Ag↓ + 4NH₃ + 2H₂O"
            pembahasan = "✅ **Kenapa bereaksi:** Gugus aldehid sangat mudah dioksidasi. Ia mampu mereduksi ion perak kompleks menjadi logam perak murni (Ag) yang menempel mengkilap di dinding tabung."
            is_positive = True
        elif senyawa == "Aseton":
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Keton (aseton) tidak memiliki atom hidrogen yang menempel pada gugus karbonil, sehingga tidak bisa dioksidasi oleh oksidator lemah seperti Tollens."
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Senyawa ini tidak mengandung gugus aldehid yang punya sifat pereduksi."

    # 4. FEHLING
    elif pereaksi == "Pereaksi Fehling":
        if senyawa == "Formaldehida":
            hasil = "(+) Terbentuk Endapan Merah Bata"
            reaksi = "R-CHO + 2Cu²⁺ + 5OH⁻ → R-COO⁻ + Cu₂O↓ (merah bata) + 3H₂O"
            pembahasan = "✅ **Kenapa bereaksi:** Aldehid memiliki sifat pereduksi yang kuat, mereduksi ion tembaga(II) kompleks berwarna biru menjadi endapan tembaga(I) oksida yang berwarna merah bata."
            is_positive = True
        elif senyawa == "Aseton":
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Sama seperti Tollens, keton tidak bisa dioksidasi oleh oksidator lemah seperti Fehling karena ketiadaan ikatan C-H pada gugus karbonilnya."
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Hanya senyawa aldehid alifatik yang memiliki sifat pereduksi untuk mereduksi ion Cu²⁺ pada suhu pemanasan."

    # 5. IODOFORM
    elif pereaksi == "Uji Iodoform (I2 / NaOH)":
        if senyawa == "Aseton":
            hasil = "(+) Endapan Kuning Iodoform"
            reaksi = "CH₃-CO-CH₃ + 3I₂ + 4NaOH → CHI₃↓ (kuning) + CH₃COONa + 3NaI + 3H₂O"
            pembahasan = "✅ **Kenapa bereaksi:** Aseton memiliki gugus metil keton (CH₃-C=O). Atom hidrogen alfa pada metil ini sangat asam, sehingga tersubstitusi oleh iodin lalu terputus membentuk endapan kuning iodoform (CHI₃)."
            is_positive = True
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Senyawa ini tidak memiliki struktur metil keton (CH₃-CO-) ataupun alkohol sekunder dengan struktur metil di sebelahnya (CH₃-CH(OH)-)."

    # 6. JONES
    elif pereaksi == "Pereaksi Jones (CrO3 / H2SO4)":
        if senyawa in ["Alkohol Primer", "Alkohol Sekunder", "Formaldehida"]:
            hasil = "(+) Warna berubah merah-jingga ke hijau/biru-hijau"
            reaksi = "CrO₃ (jingga) + H₂SO₄ + Senyawa → Cr³⁺ (hijau) + Hasil Oksidasi"
            pembahasan = "✅ **Kenapa bereaksi:** Jones adalah oksidator kuat. Memiliki atom hidrogen alfa membuat senyawa ini teroksidasi, sementara Kromium(VI) tereduksi menjadi Kromium(III) hijau."
            is_positive = True
        elif senyawa == "Alkohol Tersier":
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Tidak ada hidrogen pada karbon pengikat -OH. Oksidasi gagal terjadi."
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Senyawa sudah berada pada titik oksidasi maksimumnya (seperti asam asetat) atau tidak punya gugus yang bisa dioksidasi (seperti heksana)."

    # 7. SCHIFF
    elif pereaksi == "Pereaksi Schiff":
        if senyawa == "Formaldehida":
            hasil = "(+) Larutan berwarna Merah / Magenta"
            reaksi = "Aldehid + Pereaksi Schiff → Kompleks warna magenta"
            pembahasan = "✅ **Kenapa bereaksi:** Aldehid mudah bereaksi dengan fuksin-asam sulfit (Schiff) tanpa hambatan sterik (ruang), memulihkan kembali warna asli magenta dari fuksin."
            is_positive = True
        elif senyawa == "Aseton":
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Keton memiliki hambatan sterik (ruang lingkup molekul yang lebih besar) sehingga tidak bisa berikatan kuat dengan pereaksi Schiff untuk memunculkan warna."
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Pereaksi ini sangat spesifik bereaksi secara adisi nukleofilik hanya dengan gugus aldehid."

    # 8. NA-BISULFIT
    elif pereaksi == "Natrium Bisulfit (NaHSO3)":
        if senyawa in ["Formaldehida", "Aseton"]:
            hasil = "(+) Endapan Putih Kristalin"
            reaksi = "R₂C=O + NaHSO₃ → R₂C(OH)SO₃Na↓ (kristal putih)"
            pembahasan = "✅ **Kenapa bereaksi:** Gugus karbonil polar (C=O) pada aldehid/keton mengalami adisi nukleofilik oleh ion bisulfit yang kaya elektron, menghasilkan produk garam yang sukar larut."
            is_positive = True
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Senyawa tidak memiliki gugus karbonil reaktif. Pada asam asetat/etil asetat, efek resonansi membuat karbon karbonilnya tidak cukup positif untuk diserang bisulfit."

    # 9. HIDROKSILAMIN
    elif pereaksi == "Hidroksilamin (NH2OH)":
        if senyawa in ["Formaldehida", "Aseton"]:
            hasil = "(+) Terbentuk Kristal Oksim"
            reaksi = "R₂C=O + NH₂OH → R₂C=N-OH (Oksim) + H₂O"
            pembahasan = "✅ **Kenapa bereaksi:** Hidroksilamin menyerang karbonil pada aldehid/keton, melepaskan air (kondensasi), dan membentuk ikatan rangkap C=N baru (oksim) yang mengendap."
            is_positive = True
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Hanya senyawa aldehid dan keton murni yang bereaksi membentuk oksim. Gugus lain kurang elektrofilik atau tidak memilikinya sama sekali."

    # 10. NaHCO3 + UJI BARIT
    elif pereaksi == "NaHCO3 + Uji Barit (Ba(OH)2)":
        if senyawa == "Asam Asetat":
            hasil = "(+) Gelembung Gas & Air Barit Keruh"
            reaksi = "1) CH₃COOH + NaHCO₃ → CH₃COONa + H₂O + CO₂↑ \n2) CO₂ + Ba(OH)₂ → BaCO₃↓ (keruh) + H₂O"
            pembahasan = "✅ **Kenapa bereaksi:** Asam asetat bersifat cukup asam untuk mendonasikan proton (H⁺) ke ion bikarbonat (HCO₃⁻), menghasilkan asam karbonat yang terurai jadi gas CO₂. Gas ini lalu bereaksi dengan barit membentuk BaCO₃ yang keruh."
            is_positive = True
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Senyawa ini tidak bersifat asam atau keasamannya sangat lemah (seperti alkohol), sehingga tidak mampu bereaksi dengan garam basa lemah seperti NaHCO₃."

    # 11. CERIC NITRAT
    elif pereaksi == "Uji Ceric Nitrat":
        if senyawa in ["Alkohol Primer", "Alkohol Sekunder", "Alkohol Tersier"]:
            hasil = "(+) Warna kuning menjadi merah/merah muda"
            reaksi = "R-OH + [Ce(NO₃)₆]²⁻ → [Ce(OR)(NO₃)₅]²⁻ (kompleks merah) + HNO₃"
            pembahasan = "✅ **Kenapa bereaksi:** Pasangan elektron bebas pada oksigen di gugus hidroksil (-OH) alkohol mendesak ligan nitrat dan berikatan koordinasi dengan logam Cerium pusat, menghasilkan perubahan serapan cahaya (menjadi merah)."
            is_positive = True
        elif senyawa == "Asam Asetat":
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Meskipun punya OH, gugus karboksil sangat menarik elektron (electron-withdrawing), sehingga atom oksigennya kurang nukleofilik untuk berkoordinasi dengan Cerium."
        else:
            pembahasan = "❌ **Kenapa TIDAK bereaksi:** Uji ini spesifik untuk gugus hidroksil (-OH) alifatik bebas. Senyawa ini tidak memiliki gugus tersebut."

    # Render Hasil Output dengan UI Premium
    card_class = "modern-card" if is_positive else "modern-card card-negative"
    ikon_hasil = "✅" if is_positive else "❌"
    warna_hasil = "#10b981" if is_positive else "#ef4444"

    # Informasi kombinasi apa yang sedang diuji
    st.info(f"🔍 Menguji **{senyawa}** menggunakan **{pereaksi}**...")

    # Kotak 1: HASIL
    st.markdown(f"""
    <div class="{card_class}">
        <div class="card-title">🔬 Hasil Pengamatan Fisis</div>
        <div class="card-content" style="color: {warna_hasil}; font-weight: bold;">
            {ikon_hasil} {hasil}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Kotak 2: REAKSI KIMIA (Hanya muncul jika bereaksi)
    if is_positive:
        st.markdown(f"""
        <div class="modern-card">
            <div class="card-title">⚗️ Persamaan Reaksi Kimia</div>
            <div class="chemical-reaction">{reaksi}</div>
        </div>
        """, unsafe_allow_html=True)

    # Kotak 3: PEMBAHASAN / ALASAN
    st.markdown(f"""
    <div class="{card_class}">
        <div class="card-title">💡 Analisis & Mekanisme</div>
        <div class="card-content">{pembahasan}</div>
    </div>
    """, unsafe_allow_html=True)


# ================= TAB 2: TEORI DASAR (Menambah Nilai Kebermanfaatan) =================
with tab2:
    st.header("Mengenal Gugus Fungsi")
    st.write("Aplikasi ini berfokus pada identifikasi gugus fungsi berdasarkan sifat kimiawinya. Berikut adalah ringkasan singkat:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        with st.expander("🍷 Golongan Alkohol (-OH)", expanded=True):
            st.write("""
            Alkohol dibedakan menjadi primer, sekunder, dan tersier berdasarkan letak gugus hidroksilnya.
            * **Uji Spesifik:** Uji Lucas (membedakan jenis alkohol), Uji Ceric Nitrat (identifikasi -OH umum).
            * **Oksidasi:** Sangat bergantung pada keberadaan *hidrogen alfa*.
            """)
        with st.expander("🍏 Golongan Asam Karboksilat (-COOH)"):
            st.write("""
            Bersifat asam lemah. Dapat melepaskan proton (H+) dalam air.
            * **Uji Spesifik:** Uji NaHCO3 (menghasilkan gas Karbondioksida).
            """)
            
    with col_b:
        with st.expander("💊 Golongan Aldehid (-CHO)", expanded=True):
            st.write("""
            Memiliki gugus karbonil di ujung rantai. Bersifat reduktor kuat.
            * **Uji Spesifik:** Pereaksi Fehling (endapan merah bata), Tollens (cermin perak), Schiff (magenta).
            """)
        with st.expander("💅 Golongan Keton (-CO-)"):
            st.write("""
            Memiliki gugus karbonil di tengah rantai. Tidak dapat dioksidasi oleh oksidator lemah.
            * **Uji Spesifik:** Uji Iodoform khusus untuk *metil keton* seperti aseton.
            """)
