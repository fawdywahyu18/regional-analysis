"""
Script untuk analisis Location Quotient (LQ)
level kabupaten/kota dan provinsi

@author: fawdywahyu
"""

import pandas as pd

def cleaning_data(tahun, kode_kk):
    # tahun: str, contoh 2016
    # kode_kk: list berisi str, contoh kode_kepri
    
    # tahun = '2016'
    # kode_kk = kode_analisis_prov
    
    pdrb = pd.read_excel(f'Data/PDRB Lapangan Usaha Kab Kota Dalam Milyar Seluruh Indonesia ADHK tahun {tahun}.xlsx')

    lapangan_usaha = list(pdrb.iloc[0,6:])
    index_kk = list(pdrb[pdrb['Unnamed: 4'].isin(kode_kk)].index)
    
    if '9999' in kode_kk:
        index_kk.sort(reverse=True)
    
    nama_kk = list(pdrb['Unnamed: 5'].iloc[index_kk])
    pdrb_kk = pdrb.iloc[index_kk, 6:]
    
    # pdrb_kk = pdrb.iloc[index_kk[0]:(index_kk[-1]+1), 6:]
    
    pdrb_kk.columns = lapangan_usaha
    pdrb_kk['Nama Kab/Kota'] = nama_kk
    pdrb_kk_melt = pd.melt(pdrb_kk, id_vars=['Nama Kab/Kota'], value_vars=lapangan_usaha)
    
    pdrb_kk_melt.columns = ['Nama Kab/Kota', 'Lapangan Usaha', f'Nilai PDRB {tahun}']
    pdrb_kk_melt[f'Nilai PDRB {tahun}'] = pdrb_kk_melt[f'Nilai PDRB {tahun}'].astype(float)
    
    dict_result_cleaning = {
        'PDRB DF':pdrb_kk_melt,
        'Lapangan Usaha': lapangan_usaha
        }
    return dict_result_cleaning

# Analisis Location Quotient (LQ)
def analisis_LQ(pdrb_df_input, list_lu, tahun):
    
    
    # pdrb_df_input = pdrb_provinsi
    # list_lu = lu_all
    # tahun = '2014'
    
    pdrb_df = pdrb_df_input[['Nama Kab/Kota', 'Lapangan Usaha', f'Nilai PDRB {tahun}']]
    total_pdrb = pdrb_df[pdrb_df['Lapangan Usaha']==list_lu[0]].reset_index(drop=True)
    
    pdrb_selected = pdrb_df[pdrb_df['Lapangan Usaha']==list_lu[1]].reset_index(drop=True)
    
    niter = len(pdrb_selected)
    lq = [ (pdrb_selected[f'Nilai PDRB {tahun}'].iloc[i]/total_pdrb[f'Nilai PDRB {tahun}'].iloc[i])/(pdrb_selected[f'Nilai PDRB {tahun}'].iloc[0]/total_pdrb[f'Nilai PDRB {tahun}'].iloc[0]) for i in range(1,niter)]
    
    lq_df = pdrb_selected.copy()
    lq_df = lq_df.drop([0])
    del lq_df[f'Nilai PDRB {tahun}']
    lq_df[f'LQ Koefisien {tahun}'] = lq
    
    for l in range(2, len(list_lu)):
        pdrb_selected_l = pdrb_df[pdrb_df['Lapangan Usaha']==list_lu[l]].reset_index(drop=True)
        
        niter_l = len(pdrb_selected_l)
        lq_l = [ (pdrb_selected_l[f'Nilai PDRB {tahun}'].iloc[i]/total_pdrb[f'Nilai PDRB {tahun}'].iloc[i])/(pdrb_selected_l[f'Nilai PDRB {tahun}'].iloc[0]/total_pdrb[f'Nilai PDRB {tahun}'].iloc[0]) for i in range(1,niter_l)]
        
        lq_df_l = pdrb_selected_l.copy()
        lq_df_l = lq_df_l.drop([0])
        del lq_df_l[f'Nilai PDRB {tahun}']
        lq_df_l[f'LQ Koefisien {tahun}'] = lq_l
        
        lq_df = pd.concat([lq_df, lq_df_l])
        
    return lq_df

def creating_LQ_df(list_tahun, kode_kk_cd):
    # list_tahun: list, berisi list tahun dari tahun awal sampai tahun akhir
    # kode_kk: list berisi str, contoh kode_kepri
    
    # list_tahun = ['2016', '2019', '2020']
    # kode_kk_cd = kode_sulsel
    
    for t in list_tahun:
        pdrb_t = cleaning_data(t, kode_kk_cd)['PDRB DF']
        
        if t==list_tahun[0]:
            pdrb_merge = cleaning_data(list_tahun[0], kode_kk_cd)['PDRB DF']
        else:
            pdrb_merge = pd.merge(pdrb_merge, pdrb_t,
                                  on=['Nama Kab/Kota', 'Lapangan Usaha'],
                                  how='inner')
    return pdrb_merge


def rata_rata_LQ(tahun_list, pdrb_df_input, list_lu_input):
    
    # tahun_list: list, contoh list_tahun
    # pdrb_df_input: dataframe, contoh pdrb_sulsel
    # list_lu_input: dataframe, contoh lu_sulsel
    
    # tahun_list = list_tahun
    # pdrb_df_input = pdrb_sulsel
    # list_lu_input = lu_sulsel
    
    for t in tahun_list:
        lq_t = analisis_LQ(pdrb_df_input, list_lu_input, t)
        
        if t==tahun_list[0]:
            lq_merge = lq_t
        elif len(tahun_list)>1:
            lq_merge = pd.merge(lq_merge, lq_t,
                                on=['Nama Kab/Kota', 'Lapangan Usaha'])
        
    colnames_lq = list(lq_merge.columns)
    
    tahun_awal = tahun_list[0]
    tahun_akhir = tahun_list[-1]
    lq_merge[f'Rata-rata Koefisien LQ {tahun_awal}-{tahun_akhir}'] = lq_merge[colnames_lq[2:]].mean(axis=1)
    
    return lq_merge

def ranking_kabkot(avg_lq_kabkot=None, list_lu=None):
    
    # avg_lq_kabkot = avg_lq_papbar
    # list_lu = lu_all[1:]
    
    df_colnames = avg_lq_kabkot.columns
    list_lu_subset = list_lu[1:]
    
    for l in list_lu_subset:
        df_subset_col = avg_lq_kabkot.iloc[:,[0,1,-1]]
        df_subset = df_subset_col[df_subset_col['Lapangan Usaha']==l]
        df_sort = df_subset.sort_values(by=[df_colnames[-1]], ascending=False)
        top_n = df_sort.iloc[:3, :] 
        
        if l==list_lu_subset[0]:
            df_append = top_n
        else:
            df_append = pd.concat([df_append, top_n], axis=0)
    
    series_frek = df_append['Nama Kab/Kota'].value_counts()
    df_frek = series_frek.to_frame()
    df_frek.reset_index(inplace=True)
    df_frek.columns = ['Nama Kabupaten/Kota yang masuk dalam daftar tiga teratas', 'Frekuensi']
    
    dict_rank = {'Data Append':df_append,
                 'Tabel Frekuensi': df_frek}
    return dict_rank

def symmetric_LQ(df_composite=None):
    # df_composite = avg_lq_provinsi
    
    df_concat = df_composite[['Nama Kab/Kota', 'Lapangan Usaha']]
    
    for c in range(2, len(df_composite.columns)):
        lq_t = df_composite.iloc[:,c]
        symmetric_lq = (lq_t - 1)/(lq_t + 1)
        df_concat = pd.concat([df_concat, symmetric_lq], axis=1, ignore_index=True)
        
    kolom_lama = df_composite.columns
    kolom_baru = []
    for k in kolom_lama:
        string_baru = k.replace('LQ Koefisien', 'Koefisien LQ Simetris')
        kolom_baru.append(string_baru)
        
    df_concat.columns = kolom_baru
    
    return df_concat

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


top3_papbar.to_excel('Data Export/Papua Barat/Top 3 LQ per Lapangan Usaha di Kab Kota Papua Barat 2013 2020.xlsx', index=False)
tabel_frek_papbar.to_excel('Data Export/Papua Barat/Tabel Frekuensi Top 3 LQ per Lapangan Usaha di Kab Kota Papua Barat 2013 2020.xlsx', index=False)

top3_kepri.to_excel('Data Export/Kepulauan Riau/Top 3 LQ per Lapangan Usaha di Kab Kota Kepulauan Riau 2013 2020.xlsx', index=False)
tabel_frek_kepri.to_excel('Data Export/Kepulauan Riau/Tabel Frekuensi Top 3 LQ per Lapangan Usaha di Kab Kota Kepulauan Riau 2013 2020.xlsx', index=False)


# LQ Simetris
lq_simetris_provinsi = symmetric_LQ(avg_lq_provinsi)
lq_simetris_provinsi.to_excel('Data Export/LQ Simetris Level Provinsi 2013 2020.xlsx', index=False)





