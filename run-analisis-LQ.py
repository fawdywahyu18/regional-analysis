# script untuk running modul analisis-LQ-modules.py
from Modules.analisis_LQ_modules import *

# Running the function
kode_kepri = ['2100', '2101', '2102', '2103', '2104', '2105', '2171', '2172']
kode_sulsel = ['7300', '7301', '7302', '7303', '7304', '7305', '7306', '7307',
               '7308', '7309', '7310', '7311', '7312', '7313', '7314', '7315',
               '7316', '7317', '7318', '7322', '7325', '7326', '7371', '7372',
               '7373']
kode_papbar = ['9100', '9101', '9102', '9103', '9104', '9105', '9106', '9107',
               '9108', '9109', '9110', '9111', '9112', '9171']

kode_analisis_prov = ['9999', '2100', '7300', '9100'] # 9999 adalah kode nasional/pdb nasional

# papua barat untuk analisis kab/kota jangan memasukkan tahun 2013
daftar_tahun = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

lu_all = cleaning_data(daftar_tahun[0], kode_sulsel)['Lapangan Usaha']


pdrb_sulsel = creating_LQ_df(daftar_tahun, kode_sulsel)
pdrb_kepri = creating_LQ_df(daftar_tahun, kode_kepri)
pdrb_papbar = creating_LQ_df(daftar_tahun, kode_papbar)
pdrb_provinsi = creating_LQ_df(daftar_tahun, kode_analisis_prov)

avg_lq_sulsel = rata_rata_LQ(daftar_tahun, pdrb_sulsel, lu_all)
avg_lq_kepri = rata_rata_LQ(daftar_tahun, pdrb_kepri, lu_all)
avg_lq_papbar = rata_rata_LQ(daftar_tahun, pdrb_papbar, lu_all)
avg_lq_provinsi = rata_rata_LQ(daftar_tahun, pdrb_provinsi, lu_all)

# Sulawesi Selatan
top3_sulsel = ranking_kabkot(avg_lq_sulsel, lu_all)['Data Append']
tabel_frek_sulsel = ranking_kabkot(avg_lq_sulsel, lu_all)['Tabel Frekuensi']

# Papua Barat
top3_papbar = ranking_kabkot(avg_lq_papbar, lu_all)['Data Append']
tabel_frek_papbar = ranking_kabkot(avg_lq_papbar, lu_all)['Tabel Frekuensi']

# Kepualauan Riau
top3_kepri = ranking_kabkot(avg_lq_kepri, lu_all)['Data Append']
tabel_frek_kepri = ranking_kabkot(avg_lq_kepri, lu_all)['Tabel Frekuensi']


avg_lq_provinsi.to_excel('Data Export/LQ Level Provinsi 2013 2020.xlsx', index=False)
avg_lq_sulsel.to_excel('Data Export/Sulawesi Selatan/LQ Level Kab Kota Sulawesi Selatan 2013 2020.xlsx', index=False)
avg_lq_papbar.to_excel('Data Export/Papua Barat/LQ Level Kab Kota Papua Barat 2013 2020.xlsx', index=False)
avg_lq_kepri.to_excel('Data Export/Kepulauan Riau/LQ Level Kab Kota Kepulauan Riau 2013 2020.xlsx', index=False)

top3_sulsel.to_excel('Data Export/Sulawesi Selatan/Top 3 LQ per Lapangan Usaha di Kab Kota Sulawesi Selatan 2013 2020.xlsx', index=False)
tabel_frek_sulsel.to_excel('Data Export/Sulawesi Selatan/Tabel Frekuensi Top 3 LQ per Lapangan Usaha di Kab Kota Sulawesi Selatan 2013 2020.xlsx', index=False)

top3_papbar.to_excel('Data Export/Papua Barat/Top 3 LQ per Lapangan Usaha di Kab Kota Papua Barat 2013 2020.xlsx', index=False)
tabel_frek_papbar.to_excel('Data Export/Papua Barat/Tabel Frekuensi Top 3 LQ per Lapangan Usaha di Kab Kota Papua Barat 2013 2020.xlsx', index=False)

top3_kepri.to_excel('Data Export/Kepulauan Riau/Top 3 LQ per Lapangan Usaha di Kab Kota Kepulauan Riau 2013 2020.xlsx', index=False)
tabel_frek_kepri.to_excel('Data Export/Kepulauan Riau/Tabel Frekuensi Top 3 LQ per Lapangan Usaha di Kab Kota Kepulauan Riau 2013 2020.xlsx', index=False)
