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
    
    for l in list_lu:
        df_subset_col = avg_lq_kabkot.iloc[:,[0,1,-1]]
        df_subset = df_subset_col[df_subset_col['Lapangan Usaha']==l]
        df_sort = df_subset.sort_values(by=[df_colnames[-1]], ascending=False)
        top_n = df_sort.iloc[:3, :] 
        
        if l==list_lu[0]:
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
