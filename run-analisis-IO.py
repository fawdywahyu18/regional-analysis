# script to run analisis-IO-modules.py untuk 3 contoh provinsi: Sulawesi Selatan, Papua Barat, dan Kepulauan Riau
import sys
sys.path.append('/Modules')
from analisis_IO_modules import *

# Sulawesi Selatan
# Load data
file_name_52_sulsel = 'Data/Tabel Input-Output Provinsi Sulawesi Selatan Transaksi Domestik Atas Dasar Harga Produsen (52 Industri) 2016 (Juta Rupiah).xlsx'
file_name_17_sulsel = 'Data/Tabel Input-Output Provinsi Sulawesi Selatan Transaksi Domestik Atas Dasar Harga Produsen (17 Lapangan Usaha) 2016 (Juta Rupiah).xlsx'

df_io_sulsel = pd.read_excel(file_name_17_sulsel)
df_io_sulsel.shape

matrix_id = initial_identification(df_io_sulsel)
matrix_clean_sulsel = cleaning_matrix(df_io_sulsel)
industry_name = matrix_id['Industry Name']

sektor_unggulan_lq = ['Jasa Kesehatan dan Kegiatan Sosial',
                      'Jasa Pendidikan',
                      'Pertanian, Kehutanan, dan Perikanan']

sektor_unggulan_ss = ['Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor',
                      'Konstruksi',
                      'Informasi dan Komunikasi']

nama_industri_target = sektor_unggulan_lq[2]
label_target = 'output'
struktur_input_sulsel = struktur_io(matrix_clean_sulsel['Matrix Z'], industry_name,
                                    lab_input=label_target, nama_industri=nama_industri_target)
struktur_input_sulsel.to_excel(f'Data Export/Struktur {label_target} {nama_industri_target} Sulsel.xlsx',
                               index=False)

analisis_io_sulsel1 = io_analysis(clean_matrix=matrix_clean_sulsel,
                                  list_industry=industry_name,
                                  input_industry_name=sektor_unggulan_ss[0],
                                  delta_fd_input=1,
                                  delta_va_input=1,
                                  first_round_id='Demand')

analisis_io_sulsel2 = io_analysis(clean_matrix=matrix_clean_sulsel,
                                  list_industry=industry_name,
                                  input_industry_name=sektor_unggulan_ss[1],
                                  delta_fd_input=1,
                                  delta_va_input=1,
                                  first_round_id='Demand')

analisis_io_sulsel3 = io_analysis(clean_matrix=matrix_clean_sulsel,
                                  list_industry=industry_name,
                                  input_industry_name=sektor_unggulan_ss[2],
                                  delta_fd_input=1,
                                  delta_va_input=1,
                                  first_round_id='Demand')

df_concat = pd.concat([analisis_io_sulsel1, analisis_io_sulsel2, analisis_io_sulsel3],
                      axis=0)

df_concat.to_excel('Data Export/Sulawesi Selatan/Analisis IO sektor unggulan SS Dinamis Sulawesi Selatan.xlsx',
                   index=False)

# Papua Barat
# Load data
file_name_52_papbar = 'Data/Tabel Input-Output Provinsi Papua Barat Transaksi Domestik Atas Dasar Harga Produsen (52 Industri) 2016 (Juta Rupiah).xlsx'
file_name_17_papbar = 'Data/Tabel Input-Output Provinsi Papua Barat Transaksi Domestik Atas Dasar Harga Produsen (17 Lapangan Usaha) 2016 (Juta Rupiah).xlsx'

df_io_papbar = pd.read_excel(file_name_17_papbar)
df_io_papbar.shape

matrix_id_papbar = initial_identification(df_io_papbar)
matrix_clean_papbar = cleaning_matrix(df_io_papbar)
industry_name_papbar = matrix_id_papbar['Industry Name']

sektor_unggulan_lq_papbar = ['Administrasi Pemerintahan, Pertahanan dan Jaminan Sosial Wajib',
                             'Pertambangan dan Penggalian',
                             'Industri Pengolahan']

sektor_unggulan_ss_papbar = ['Konstruksi',
                             'Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor',
                             'Administrasi Pemerintahan, Pertahanan dan Jaminan Sosial Wajib']

nama_industri_target_papbar = sektor_unggulan_ss_papbar[1]
label_target_papbar = 'output'
struktur_input_papbar = struktur_io(matrix_clean_papbar['Matrix Z'], industry_name_papbar,
                                    lab_input=label_target_papbar, nama_industri=nama_industri_target_papbar,
                                    top_berapa=10)
struktur_input_papbar.to_excel(f'Data Export/Papua Barat/Struktur {label_target_papbar} {nama_industri_target_papbar} Papbar.xlsx',
                               index=False)

analisis_io_papbar1 = io_analysis(clean_matrix=matrix_clean_papbar,
                                  list_industry=industry_name_papbar,
                                  input_industry_name=sektor_unggulan_ss_papbar[0],
                                  delta_fd_input=1,
                                  delta_va_input=1,
                                  first_round_id='Demand')

analisis_io_papbar2 = io_analysis(clean_matrix=matrix_clean_papbar,
                                  list_industry=industry_name_papbar,
                                  input_industry_name=sektor_unggulan_ss_papbar[1],
                                  delta_fd_input=1,
                                  delta_va_input=1,
                                  first_round_id='Demand')

analisis_io_papbar3 = io_analysis(clean_matrix=matrix_clean_papbar,
                                  list_industry=industry_name_papbar,
                                  input_industry_name=sektor_unggulan_ss_papbar[2],
                                  delta_fd_input=1,
                                  delta_va_input=1,
                                  first_round_id='Demand')

df_concat_papbar = pd.concat([analisis_io_papbar1, analisis_io_papbar2, analisis_io_papbar3],
                              axis=0)

df_concat_papbar.to_excel('Data Export/Papua Barat/Analisis IO sektor unggulan SS Dinamis Papua Barat.xlsx',
                          index=False)

# Kepulauan Riau
# Load data
file_name_52_kepri = 'Data/Tabel Input-Output Provinsi Kepulauan Riau Transaksi Domestik Atas Dasar Harga Produsen (52 Industri) 2016 (Juta Rupiah).xlsx'
file_name_17_kepri = 'Data/Tabel Input-Output Provinsi Kepulauan Riau Transaksi Domestik Atas Dasar Harga Produsen (17 Lapangan Usaha) 2016 (Juta Rupiah).xlsx'

df_io_kepri = pd.read_excel(file_name_17_kepri)
df_io_kepri.shape

matrix_id_kepri = initial_identification(df_io_kepri)
matrix_clean_kepri = cleaning_matrix(df_io_kepri)
industry_name_kepri = matrix_id_kepri['Industry Name']

sektor_unggulan_lq_kepri = ['Pertambangan dan Penggalian',
                            'Industri Pengolahan',
                            'Konstruksi']

sektor_unggulan_ss_kepri = ['Industri Pengolahan',
                            'Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor',
                            'Informasi dan Komunikasi']

nama_industri_target_kepri = sektor_unggulan_ss_kepri[2]
label_target_kepri = 'output'
struktur_input_kepri = struktur_io(matrix_clean_kepri['Matrix Z'], industry_name_kepri,
                                   lab_input=label_target_kepri, nama_industri=nama_industri_target_kepri,
                                   top_berapa=10)
struktur_input_kepri.to_excel(f'Data Export/Kepulauan Riau/Struktur {label_target_kepri} {nama_industri_target_kepri} Kepri.xlsx',
                              index=False)

analisis_io_kepri1 = io_analysis(clean_matrix=matrix_clean_kepri,
                                 list_industry=industry_name_kepri,
                                 input_industry_name=sektor_unggulan_lq_kepri[0],
                                 delta_fd_input=1,
                                 delta_va_input=1,
                                 first_round_id='Demand')

analisis_io_kepri2 = io_analysis(clean_matrix=matrix_clean_kepri,
                                 list_industry=industry_name_kepri,
                                 input_industry_name=sektor_unggulan_lq_kepri[1],
                                 delta_fd_input=1,
                                 delta_va_input=1,
                                 first_round_id='Demand')

analisis_io_kepri3 = io_analysis(clean_matrix=matrix_clean_kepri,
                                  list_industry=industry_name_kepri,
                                  input_industry_name=sektor_unggulan_lq_kepri[2],
                                  delta_fd_input=1,
                                  delta_va_input=1,
                                  first_round_id='Demand')

df_concat_kepri = pd.concat([analisis_io_kepri1, analisis_io_kepri2, analisis_io_kepri3],
                             axis=0)

df_concat_kepri.to_excel('Data Export/Kepulauan Riau/Analisis IO sektor unggulan LQ Kepulauan Riau.xlsx',
                          index=False)
