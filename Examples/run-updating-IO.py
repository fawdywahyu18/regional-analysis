# script untuk run updating-IO-modules.py

from updating-IO-modules import *

kode_sulsel = ['7300']
kode_kepri = ['2100']
kode_papbar = ['9100']
list_tahun = ['2016', '2020'] # tahun awal harus 2016, sedangkan tahun akhir harus setelah 2016

# Sulawesi Selatan
sektor_unggulan_lq_sulsel = ['Jasa Kesehatan dan Kegiatan Sosial',
                             'Jasa Pendidikan',
                             'Pertanian, Kehutanan, dan Perikanan']

sektor_unggulan_ss_sulsel = ['Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor',
                             'Konstruksi',
                             'Informasi dan Komunikasi']

file_name_52_sulsel = 'Data/Tabel Input-Output Provinsi Sulawesi Selatan Transaksi Domestik Atas Dasar Harga Produsen (52 Industri) 2016 (Juta Rupiah).xlsx'
file_name_17_sulsel = 'Data/Tabel Input-Output Provinsi Sulawesi Selatan Transaksi Domestik Atas Dasar Harga Produsen (17 Lapangan Usaha) 2016 (Juta Rupiah).xlsx'

hasil_update_sulsel = run_update_provinsi(file_name_17_sulsel, kode_sulsel,
                                          list_tahun, sektor_unggulan_lq_sulsel,
                                          sektor_unggulan_ss_sulsel)

hasil_update_sulsel['PDRB Prov Growth'].to_excel(f'Data Export/Sulawesi Selatan/Pertumbuhan per Lapangan Usaha Sulsel {list_tahun[0]} ke {list_tahun[1]}.xlsx')
hasil_update_sulsel['Hasil Analisis IO Hasil Update LQ'].to_excel('Data Export/Sulawesi Selatan/Hasil Update Analisis IO sektor unggulan LQ Sulawesi Selatan.xlsx',
                                                                  index=False)
hasil_update_sulsel['Hasil Analisis IO Hasil Update SS'].to_excel('Data Export/Sulawesi Selatan/Hasil Update Analisis IO sektor unggulan SS Dinamis Sulawesi Selatan.xlsx',
                                                                  index=False)

# Papua Barat
file_name_52_papbar = 'Data/Tabel Input-Output Provinsi Papua Barat Transaksi Domestik Atas Dasar Harga Produsen (52 Industri) 2016 (Juta Rupiah).xlsx'
file_name_17_papbar = 'Data/Tabel Input-Output Provinsi Papua Barat Transaksi Domestik Atas Dasar Harga Produsen (17 Lapangan Usaha) 2016 (Juta Rupiah).xlsx'

sektor_unggulan_lq_papbar = ['Administrasi Pemerintahan, Pertahanan dan Jaminan Sosial Wajib',
                             'Pertambangan dan Penggalian',
                             'Industri Pengolahan']

sektor_unggulan_ss_papbar = ['Konstruksi',
                             'Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor',
                             'Administrasi Pemerintahan, Pertahanan dan Jaminan Sosial Wajib']

hasil_update_papbar = run_update_provinsi(file_name_17_papbar, kode_papbar,
                                          list_tahun, sektor_unggulan_lq_papbar,
                                          sektor_unggulan_ss_papbar)

hasil_update_papbar['PDRB Prov Growth'].to_excel(f'Data Export/Papua Barat/Pertumbuhan per Lapangan Usaha Papbar {list_tahun[0]} ke {list_tahun[1]}.xlsx')
hasil_update_papbar['Hasil Analisis IO Hasil Update LQ'].to_excel('Data Export/Papua Barat/Hasil Update Analisis IO sektor unggulan LQ Papua Barat.xlsx',
                                                                  index=False)
hasil_update_papbar['Hasil Analisis IO Hasil Update SS'].to_excel('Data Export/Papua Barat/Hasil Update Analisis IO sektor unggulan SS Dinamis Papua Barat.xlsx',
                                                                  index=False)

# Kepulauan Riau
file_name_52_kepri = 'Data/Tabel Input-Output Provinsi Kepulauan Riau Transaksi Domestik Atas Dasar Harga Produsen (52 Industri) 2016 (Juta Rupiah).xlsx'
file_name_17_kepri = 'Data/Tabel Input-Output Provinsi Kepulauan Riau Transaksi Domestik Atas Dasar Harga Produsen (17 Lapangan Usaha) 2016 (Juta Rupiah).xlsx'

sektor_unggulan_lq_kepri = ['Pertambangan dan Penggalian',
                            'Industri Pengolahan',
                            'Konstruksi']

sektor_unggulan_ss_kepri = ['Industri Pengolahan',
                            'Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor',
                            'Informasi dan Komunikasi']

hasil_update_kepri = run_update_provinsi(file_name_17_kepri, kode_kepri,
                                         list_tahun, sektor_unggulan_lq_kepri,
                                         sektor_unggulan_ss_kepri)

hasil_update_kepri['PDRB Prov Growth'].to_excel(f'Data Export/Kepulauan Riau/Pertumbuhan per Lapangan Usaha Kepri {list_tahun[0]} ke {list_tahun[1]}.xlsx')
hasil_update_kepri['Hasil Analisis IO Hasil Update LQ'].to_excel('Data Export/Kepulauan Riau/Hasil Update Analisis IO sektor unggulan LQ Kepulauan Riau.xlsx',
                                                                 index=False)
hasil_update_kepri['Hasil Analisis IO Hasil Update SS'].to_excel('Data Export/Kepulauan Riau/Hasil Update Analisis IO sektor unggulan SS Dinamis Kepulauan Riau.xlsx',
                                                                 index=False)
