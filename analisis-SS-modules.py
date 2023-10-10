"""
Script untuk analisis Shift-Share (SS) level kabupaten/kota dan provinsi

@author: fawdywahyu
"""

import pandas as pd

def cleaning_data(tahun, kode_kk):
    # tahun: str, contoh 2016
    # kode_kk: list berisi str, contoh kode_kepri
    
    # tahun = '2016'
    # kode_kk = kode_sulsel
    
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


def creating_SS_df(list_tahun, kode_kk_cd):
    # list_tahun: list, berisi list tahun dari tahun awal sampai tahun akhir
    # kode_kk: list berisi str, contoh kode_kepri
    
    # list_tahun = ['2016', '2019', '2020']
    # kode_kk_cd = kode_sulsel
    
    if len(list_tahun)<2:
        raise ValueError('Minimal harus ada 2 tahun di dalam list_tahun')
    
    pdrb_merge = cleaning_data(list_tahun[0], kode_kk_cd)['PDRB DF']
    for t in list_tahun[1:]:
        pdrb_t = cleaning_data(t, kode_kk_cd)['PDRB DF']
        pdrb_merge = pd.merge(pdrb_merge, pdrb_t,
                              on=['Nama Kab/Kota', 'Lapangan Usaha'],
                              how='inner')
    return pdrb_merge

def analisis_SS(pdrb_ss, list_lu, index_kolom_estimasi=4):
    # pdrb_df: dataframe, contoh pdrb_merge hasil dari function creating_SS_df
    # list_lu: list, contoh 'Lapangan Usaha' hasil dari function cleaning_data
    # index_kolom_estimasi=5, int, 0 sampai 4
    # 0 sampai 4 secara berurutan adalah 'ri - Ri', 'PNij', 'Ppij', 'PPWij', 'PBij'
    
    # pdrb_ss = pdrb_ss_sulsel
    # list_lu = lu_sulsel
    
    nama_kabkot = pdrb_ss['Nama Kab/Kota'].unique()
    
    num_columns = pdrb_ss.shape[1]
    i_initial = 2
    i_end = i_initial + 1
    while i_end <= (num_columns-1):
        pdrb_selected = pdrb_ss.iloc[:,[0, 1, i_initial, i_end]]
        
        colnames_list = list(pdrb_selected.columns)[2:]
        tahun_awal = colnames_list[0][-4:]
        tahun_akhir = colnames_list[1][-4:]
        
        pdrb_selected['selisih'] = (pdrb_selected.iloc[:,-1] - pdrb_selected.iloc[:,-2]) / pdrb_selected.iloc[:,-2]
        Ra = pdrb_selected[(pdrb_selected['Nama Kab/Kota']==nama_kabkot[0]) & (pdrb_selected['Lapangan Usaha']==list_lu[0])]['selisih'][0]
        Ri = pdrb_selected[(pdrb_selected['Nama Kab/Kota']==nama_kabkot[0]) & (pdrb_selected['Lapangan Usaha']!=list_lu[0])]
        Ri['Ra'] = Ra
        Ri['Ri - Ra'] = Ri['selisih'] - Ri['Ra']
        
        df_kabkot = pdrb_selected[(pdrb_selected['Nama Kab/Kota']!=nama_kabkot[0]) & (pdrb_selected['Lapangan Usaha']!=list_lu[0])] 
        
        df_merge = pd.merge(df_kabkot, Ri,
                            on='Lapangan Usaha',
                            how='right')
        
        # selisih_y adalah Ri
        # selisih_x adalah ri
        df_merge['ri - Ri'] = df_merge['selisih_x'] - df_merge['selisih_y']
        df_merge['PNij'] = df_merge.iloc[:,2] * df_merge['Ra']
        df_merge['Ppij'] = df_merge.iloc[:,2] * df_merge['Ri - Ra'] # Ppij : Komponen pertumbuhan proporsional sektor i wilayah j
        df_merge['PPWij'] = df_merge.iloc[:,2] * df_merge['ri - Ri'] # PPWij : Komponen Pertumbuhan Pangsa Wilayah sektor i wilayah j
        df_merge['PBij'] = df_merge['Ppij'] + df_merge['PPWij'] # PBij : Pergeseran Bersih sektor i pada wilayah j
        
        # select columns
        kolom_estimasi = ['ri - Ri', 'PNij', 'Ppij', 'PPWij', 'PBij']
        kolom_keluar = index_kolom_estimasi
        
        df_merge_selected = df_merge[['Nama Kab/Kota_x', 'Lapangan Usaha', kolom_estimasi[kolom_keluar]]]
        nama_kolom = [kolom_estimasi[kolom_keluar], 'dari', str(tahun_awal),'ke', str(tahun_akhir)]
        kombinasi_str = " ".join(nama_kolom)
        
        df_merge_selected.columns = ['Nama Kab/Kota', 'Lapangan Usaha', kombinasi_str]
        
        if i_initial == 2:
            df_merge_final = df_merge_selected.copy()
        else:
            df_merge_final = pd.merge(df_merge_final, df_merge_selected,
                                      on=['Nama Kab/Kota', 'Lapangan Usaha'],
                                      how='inner')
        i_initial += 1
        i_end = i_initial + 1
    
    colnames_merge = list(df_merge_final.columns)
    df_merge_final['Median'] = df_merge_final[colnames_merge[2:]].median(axis=1)
    
    return df_merge_final

def ranking_kabkot(shift_share_kabkot=None, list_lu=None):
    
    # shift_share_kabkot = shift_share_sulsel
    # list_lu = lu_sulsel
    
    df_colnames = shift_share_kabkot.columns
    list_lu_subset = list_lu[1:]
    
    for l in list_lu_subset:
        df_subset_col = shift_share_kabkot.iloc[:,[0,1,-1]]
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
