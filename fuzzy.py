import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ======== Definisi Variabel Fuzzy ========
suhu = ctrl.Antecedent(np.arange(24, 35, 0.1), 'suhu')
kelembaban = ctrl.Antecedent(np.arange(70, 100.1, 0.1), 'kelembaban')
angin = ctrl.Antecedent(np.arange(0, 11, 0.1), 'angin')
penyinaran = ctrl.Antecedent(np.arange(0, 101, 1), 'penyinaran')
cuaca = ctrl.Consequent(np.arange(0, 101, 1), 'cuaca')

# ======== Fungsi Keanggotaan Input ========
suhu['dingin'] = fuzz.trapmf(suhu.universe, [24, 24, 25, 27])
suhu['normal'] = fuzz.trapmf(suhu.universe, [25, 27, 29, 31])
suhu['panas'] = fuzz.trapmf(suhu.universe, [29, 31, 34, 34])

kelembaban['kering'] = fuzz.trapmf(kelembaban.universe, [70, 70, 72, 80])
kelembaban['lembab'] = fuzz.trapmf(kelembaban.universe, [75, 78, 87, 90])
kelembaban['basah'] = fuzz.trapmf(kelembaban.universe, [85, 90, 95, 95])

angin['pelan'] = fuzz.trapmf(angin.universe, [0, 0, 2, 4])
angin['sedang'] = fuzz.trapmf(angin.universe, [2, 4, 6, 8])
angin['kencang'] = fuzz.trapmf(angin.universe, [6, 8, 10, 10])

penyinaran['rendah'] = fuzz.trapmf(penyinaran.universe, [0, 0, 20, 40])
penyinaran['sedang'] = fuzz.trapmf(penyinaran.universe, [20, 35, 65, 80])
penyinaran['tinggi'] = fuzz.trapmf(penyinaran.universe, [60, 80, 100, 100])

# ======== Fungsi Keanggotaan Output ========
cuaca['cerah_berawan'] = fuzz.trapmf(cuaca.universe, [0, 0, 2.5, 5])
cuaca['hujan_ringan'] = fuzz.trapmf(cuaca.universe, [2.5, 5, 15, 20])
cuaca['hujan_sedang'] = fuzz.trapmf(cuaca.universe, [15, 20, 45, 50])
cuaca['hujan_lebat'] = fuzz.trapmf(cuaca.universe, [45, 50, 100, 100])

# ======== Aturan Fuzzy ========
rules = [
    ctrl.Rule(suhu['normal'] & kelembaban['lembab'] & angin['pelan'] & penyinaran['sedang'], cuaca['hujan_ringan']),
    ctrl.Rule(suhu['normal'] & kelembaban['lembab'] & angin['pelan'] & penyinaran['tinggi'], cuaca['cerah_berawan']),
    ctrl.Rule(suhu['normal'] & kelembaban['lembab'] & angin['sedang'] & penyinaran['sedang'], cuaca['hujan_ringan']),
    ctrl.Rule(suhu['normal'] & kelembaban['lembab'] & angin['sedang'] & penyinaran['tinggi'], cuaca['cerah_berawan']),
    ctrl.Rule(suhu['panas'] & kelembaban['lembab'] & angin['pelan'] & penyinaran['sedang'], cuaca['hujan_ringan']),
    ctrl.Rule(suhu['panas'] & kelembaban['lembab'] & angin['pelan'] & penyinaran['tinggi'], cuaca['cerah_berawan']),
    ctrl.Rule(suhu['panas'] & kelembaban['lembab'] & angin['sedang'] & penyinaran['sedang'], cuaca['hujan_ringan']),
    ctrl.Rule(suhu['panas'] & kelembaban['lembab'] & angin['sedang'] & penyinaran['tinggi'], cuaca['hujan_ringan']),
    ctrl.Rule(suhu['normal'] & kelembaban['lembab'] & angin['kencang'] & penyinaran['tinggi'], cuaca['cerah_berawan']),
    ctrl.Rule(suhu['panas'] & kelembaban['lembab'] & angin['kencang'] & penyinaran['sedang'], cuaca['hujan_ringan']),
    ctrl.Rule(suhu['normal'] & kelembaban['lembab'] & angin['kencang'] & penyinaran['sedang'], cuaca['hujan_ringan']),
    ctrl.Rule(suhu['panas'] & kelembaban['lembab'] & angin['kencang'] & penyinaran['tinggi'], cuaca['cerah_berawan']),
    ctrl.Rule(suhu['dingin'] & kelembaban['kering'] & angin['pelan'] & penyinaran['sedang'], cuaca['cerah_berawan']),
    ctrl.Rule(suhu['dingin'] & kelembaban['kering'] & angin['kencang'] & penyinaran['tinggi'], cuaca['cerah_berawan']),
    ctrl.Rule(suhu['normal'] & kelembaban['kering'] & angin['pelan'] & penyinaran['tinggi'], cuaca['cerah_berawan']),
    ctrl.Rule(suhu['panas'] & kelembaban['kering'] & angin['sedang'] & penyinaran['rendah'], cuaca['hujan_ringan']),
    ctrl.Rule(suhu['normal'] & kelembaban['basah'] & angin['pelan'] & penyinaran['rendah'], cuaca['hujan_sedang']),
    ctrl.Rule(suhu['normal'] & kelembaban['basah'] & angin['sedang'] & penyinaran['sedang'], cuaca['hujan_sedang']),
    ctrl.Rule(suhu['panas'] & kelembaban['basah'] & angin['kencang'] & penyinaran['rendah'], cuaca['hujan_sedang']),
    ctrl.Rule(suhu['dingin'] & kelembaban['basah'] & angin['sedang'] & penyinaran['tinggi'], cuaca['hujan_lebat']),
]

# Aturan tambahan catch-all agar sistem tetap menghasilkan output
rules.append(ctrl.Rule(suhu['dingin'] | suhu['normal'] | suhu['panas'], cuaca['cerah_berawan']))

# ======== Sistem Inferensi Fuzzy ========
cuaca_ctrl = ctrl.ControlSystem(rules)

# ======== Fungsi Prediksi ========
def predict_weather(s, k, a, p):
    sim = ctrl.ControlSystemSimulation(cuaca_ctrl)
    sim.input['suhu'] = s
    sim.input['kelembaban'] = k
    sim.input['angin'] = a
    sim.input['penyinaran'] = p

    try:
        sim.compute()
        hasil = sim.output['cuaca']
    except Exception as e:
        print("Gagal menghitung fuzzy:", e)
        return ("Tidak dapat memprediksi", 0)

    print(f"Hasil defuzzifikasi: {hasil:.2f}")

    if hasil <= 5:
        prediksi = 'Cerah Berawan'
    elif hasil <= 20:
        prediksi = 'Hujan Ringan'
    elif hasil <= 50:
        prediksi = 'Hujan Sedang'
    else:
        prediksi = 'Hujan Lebat'

    return (prediksi, hasil)
