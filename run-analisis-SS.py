# script untuk run analisis-SS-modules.py
import sys
sys.path.append('/Modules')
from analisis_SS_modules import *


# Perlu diperhatikan bahwa kode provinsi selalu paling awal, setelah itu, urutannya gak penting
kode_kepri = ['2100', '2101', '2102', '2103', '2104', '2105', '2171', '2172']
kode_sulsel = ['7300', '7301', '7302', '7303', '7304', '7305', '7306', '7307',
               '7308', '7309', '7310', '7311', '7312', '7313', '7314', '7315',
               '7316', '7317', '7318', '7322', '7325', '7326', '7371', '7372',
               '7373']
kode_papbar = ['9100', '9101', '9102', '9103', '9104', '9105', '9106', '9107',
               '9108', '9109', '9110', '9111', '9112', '9171']

tahun_list = ['2013','2014','2015','2016', '2017', '2018', '2019', '2020']


# Sulawesi Selatan
pdrb_sulsel = cleaning_data('2016', kode_sulsel)['PDRB DF']
lu_sulsel = cleaning_data('2016', kode_sulsel)['Lapangan Usaha']
pdrb_ss_sulsel = creating_SS_df(tahun_list, kode_sulsel)
shift_share_sulsel = analisis_SS(pdrb_ss_sulsel, lu_sulsel)
top3_sulsel = ranking_kabkot(shift_share_sulsel, lu_sulsel)['Data Append']
tabel_frek_sulsel = ranking_kabkot(shift_share_sulsel, lu_sulsel)['Tabel Frekuensi']

shift_share_sulsel.to_excel('Data Export/Sulawesi Selatan/Shift Share Dinamis Level Kab Kota Sulawesi Selatan 2014 2020.xlsx', 
                            index=False)
top3_sulsel.to_excel('Data Export/Sulawesi Selatan/Top 3 SS Dinamis per Lapangan Usaha di Kab Kota Sulawesi Selatan 2013 2020.xlsx', index=False)
tabel_frek_sulsel.to_excel('Data Export/Sulawesi Selatan/Tabel Frekuensi Top 3 SS Dinamis per Lapangan Usaha di Kab Kota Sulawesi Selatan 2013 2020.xlsx', index=False)


# Papua Barat
lu_papbar = cleaning_data('2013', kode_papbar)['Lapangan Usaha']
pdrb_ss_papbar = creating_SS_df(tahun_list, kode_papbar)
shift_share_papbar = analisis_SS(pdrb_ss_papbar, lu_papbar)
top3_papbar = ranking_kabkot(shift_share_papbar, lu_papbar)['Data Append']
tabel_frek_papbar = ranking_kabkot(shift_share_papbar, lu_papbar)['Tabel Frekuensi']

shift_share_papbar.to_excel('Data Export/Papua Barat/Shift Share Dinamis Level Kab Kota Papua Barat 2014 2020.xlsx', 
                            index=False)
top3_papbar.to_excel('Data Export/Papua Barat/Top 3 SS Dinamis per Lapangan Usaha di Kab Kota Papua Barat 2013 2020.xlsx', index=False)
tabel_frek_papbar.to_excel('Data Export/Papua Barat/Tabel Frekuensi Top 3 SS Dinamis per Lapangan Usaha di Kab Kota Papua Barat 2013 2020.xlsx', index=False)

# Kepulauan Riau
lu_kepri = cleaning_data('2013', kode_kepri)['Lapangan Usaha']
pdrb_ss_kepri = creating_SS_df(tahun_list, kode_kepri)
shift_share_kepri = analisis_SS(pdrb_ss_kepri, lu_kepri)
top3_kepri = ranking_kabkot(shift_share_kepri, lu_kepri)['Data Append']
tabel_frek_kepri = ranking_kabkot(shift_share_kepri, lu_kepri)['Tabel Frekuensi']

shift_share_kepri.to_excel('Data Export/Kepulauan Riau/Shift Share Dinamis Level Kab Kota Kepulauan Riau 2014 2020.xlsx', 
                            index=False)
top3_kepri.to_excel('Data Export/Kepulauan Riau/Top 3 SS Dinamis per Lapangan Usaha di Kab Kota Kepulauan Riau 2014 2020.xlsx', index=False)
tabel_frek_kepri.to_excel('Data Export/Kepulauan Riau/Tabel Frekuensi Top 3 SS Dinamis per Lapangan Usaha di Kab Kota Kepulauan Riau 2014 2020.xlsx', index=False)



# analisis per provinsi
kode_analisis_prov = ['9999', '2100', '7300', '9100'] # 9999 adalah kode nasional/pdb nasional
pdrb_ss_provinsi = creating_SS_df(tahun_list, kode_analisis_prov)
lu_provinsi = cleaning_data('2016', kode_analisis_prov)['Lapangan Usaha']

shift_share_provinsi = analisis_SS(pdrb_ss_provinsi, lu_provinsi, 4)
shift_share_provinsi.to_excel('Data Export/Shift Share per Provinsi 2013 2020.xlsx',
                              index=False)

# Pergeseran Proporsional (PP) per provinsi
pp_provinsi = analisis_SS(pdrb_ss_provinsi, lu_provinsi, 5)
pp_provinsi.to_excel('Data Export/Pergeseran Proporsional (PP) per Provinsi 2013 2020.xlsx',
                     index=False)

# Pertumbuhan Pangsa Wilayah
ppw_provinsi = analisis_SS(pdrb_ss_provinsi, lu_provinsi, 6)
ppw_provinsi.to_excel('Data Export/Pertumbuhan Pangsa Wilayah (PPW) per Provinsi 2013 2020.xlsx',
                      index=False)
