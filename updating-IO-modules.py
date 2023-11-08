"""
Updating IO berdasarkan tabel IO 17 Lapangan usaha di level provinsi

@author: fawdywahyu
"""

import pandas as pd
import numpy as np
import math
from ipfn import ipfn


# Initial Identification
def initial_identification(tabel_input=None):
    
    # tabel_input: df
    
    # IO 17 sectors dimension is 26,31
    # IO 52 sectors dimension is 61,66
    
    # tabel_input = df_io
    
    shape = tabel_input.shape
    product = 1
    for i in range(len(shape)):
        product *= shape[i]
    
    if product==4026:
        shape_id = '52 sectors'
    elif product==806:
        shape_id = '17 sectors'
    else:
        raise Exception('Table size is unrecognized')
        
    # Industry Name Identification
    max_row = shape[0] - 6
    industry_name = tabel_input.iloc[3:max_row, 1].tolist()
    industry_name_clean = [l.rstrip() for l in industry_name]
    
    dict_initial_id = {
        'Shape Identification': shape_id,
        'Industry Name': industry_name_clean
        }
    
    return dict_initial_id

# Cleaning Matrix
def cleaning_matrix(tabel_input=None):
    # tabel_input = df_io
    # shape_id = '52 sectors'
    
    df_to_clean = tabel_input.copy()
    
    shape_mat = df_to_clean.shape
    max_row_mat = shape_mat[0]-6
    max_col_mat = shape_mat[1]-11
    
    # Demand Side
    mat_Z = df_to_clean.iloc[3:max_row_mat, 3:max_col_mat].to_numpy(dtype=float)
    vec_fd = df_to_clean.iloc[3:max_row_mat, -2].to_numpy(dtype=float)
    vec_output = df_to_clean.iloc[3:max_row_mat, -1].to_numpy(dtype=float)
    
    # vec_output = np.sum(mat_Z, axis=1) + vec_fd
    # mat_output = vec_output * np.identity(len(vec_output))
    mat_output = vec_output * np.identity(len(vec_output))
    inv_x = np.linalg.pinv(mat_output)
    
    mat_A = np.matmul(mat_Z, inv_x)
    mat_L = np.identity(len(mat_A)) - mat_A
    mat_L_inv = np.linalg.inv(mat_L)
    
    # Supply Side
    mat_B = np.matmul(inv_x, mat_Z) # allocation coefficient
    mat_G = np.identity(len(mat_B)) - mat_B
    mat_G_inv = np.linalg.inv(mat_G) # the output inverse
    vec_va = df_to_clean.iloc[-2,3:max_col_mat].to_numpy(dtype=float)
    # vec_input = df_to_clean.iloc[-1, 3:max_col_mat].to_numpy(dtype=float)
    
    cleaning_result = {
        'Matrix Z': mat_Z,
        'Matrix A': mat_A,
        'Matrix L': mat_L,
        'Matrix Leontief Inverse': mat_L_inv,
        'Matrix B': mat_B,
        'Matrix G': mat_G,
        'Matrix G Inverse': mat_G_inv,
        'Vector Output': vec_output,
        'Vector Value Add': vec_va,
        'Vector Final Demand': vec_fd
        }
    
    return cleaning_result

# Updating IO
# Cara Manual
# Classical IPF Algorithm
def ipf_update(M, u, v):
    
    # M adalah matrix Z
    # u adalah row target
    # v adalah col target
    
    # M = mat_update_new
    # u = u_target
    # v = v_target
    
    r_sums = M.sum(axis=1)
    N = np.array([[M[r,c] * u[r] / r_sums[r] for c in range(M.shape[1])]
                  for r in range(M.shape[0])])
    
    # Replace nan in N with 0
    mask = np.isnan(N)
    N[mask] = 0


    c_sums = N.sum(axis=0)
    zero = np.array([[N[r, c] * v[c] / c_sums[c] for c in range(N.shape[1])]
                     for r in range(N.shape[0])])
    
    # Replace nan in N with 0
    mask = np.isnan(zero)
    zero[mask] = 0


    d_u = np.linalg.norm(u - zero.sum(axis=1), 2)
    d_v = np.linalg.norm(v - zero.sum(axis=0), 2)
    return zero, d_u, d_v

# Factor estimation Algorithm
def factor_update(X, u, v, b):
    
    # X = mat_Z.copy()
    # b = np.ones(X.shape[1])
    # u = rt
    # v = ct

    a = [u[i] / sum([X[i, j] * b[j] for j in range(X.shape[1])]) for i in range(X.shape[0])]
    a_nn = [0 if math.isnan(x) else x for x in a]
    
    b = [v[j] / sum([X[i, j] * a[i] for i in range(X.shape[0])]) for j in range(X.shape[1])]
    b_nn = [0 if math.isnan(x) else x for x in b]

    M = np.array([[X[i, j] * a_nn[i] * b_nn[j] for j in range(X.shape[1])] for i in range(X.shape[0])])
    
    # Replace nan in N with 0
    mask = np.isnan(M)
    M[mask] = 0

    d_u = np.linalg.norm(u - M.sum(axis=1), 2)
    d_v = np.linalg.norm(v - M.sum(axis=0), 2)

    return M, a, b, d_u, d_v

def updating_IO(mat_update_input, u_target_input, v_target_input, iteration_input=1000):
    
    # mat_updated_input: matrix, contoh mat_update
    # u_target_input: vector, 
    # v_target_input: vector,
    # iteration_input: int, default=1000
    
    
    for _ in range(iteration_input):
        mat_classic_result, d_u, d_v = ipf_update(mat_update_input, u_target_input, v_target_input)
        if d_u <= 0.0001 and d_v <= 0.0001:
            break

    b_ideal = np.ones(mat_update_input.shape[1])
    for _ in range(iteration_input):
        mat_factor_result, a, b, d_u_factor, d_v_factor = factor_update(mat_update_input, u_target_input, v_target_input, b_ideal)
        if d_u <= 0.0001 and d_v <= 0.0001:
            break

    # Using ipfn to update the Input-Output table
    aggregates = [u_target_input, v_target_input]
    dimensions = [[0], [1]]
    IPF = ipfn.ipfn(mat_update_input, aggregates, dimensions, convergence_rate=1e-6)
    mat_ipf_result = IPF.iteration()

    # Check the convergance based on L2 norm
    d_u_ipfn = np.linalg.norm(u_target_input - mat_ipf_result.sum(axis=1), 2)
    d_v_ipfn = np.linalg.norm(v_target_input - mat_ipf_result.sum(axis=0), 2)
    
    # select which method is the best by using the comination of d_u and d_v
    classic_indicator = d_u + d_v
    factor_indicator = d_u_factor + d_v_factor
    ipfn_indicator = d_u_ipfn + d_v_ipfn
    
    list_indicator = [classic_indicator, factor_indicator, ipfn_indicator]
    index_min = np.argmin(list_indicator)
    
    if index_min==0:
        mat_updated_result = mat_classic_result
    elif index_min==1:
        mat_updated_result = mat_factor_result
    else:
        mat_updated_result = mat_ipf_result
    
    dict_result_update = {
        'Matrix Result': mat_updated_result,
        'Index Minimum': index_min
        }
    return dict_result_update

# Functions to prepare the column and row target of matrix scalling process
def cleaning_df(tahun, kode_kk):
    # tahun: str, contoh 2016
    # kode_kk: list berisi str, contoh kode_kepri
    
    # tahun = '2016'
    # kode_kk = kode_sulsel
    
    pdrb = pd.read_excel(f'Data/PDRB Lapangan Usaha Kab Kota Dalam Milyar Seluruh Indonesia ADHK tahun {tahun}.xlsx')

    lapangan_usaha = list(pdrb.iloc[0,6:])
    index_kk = list(pdrb[pdrb['Unnamed: 4'].isin(kode_kk)].index)
    nama_kk = list(pdrb['Unnamed: 5'].iloc[index_kk])
    pdrb_kk = pdrb.iloc[index_kk[0]:(index_kk[-1]+1), 6:]
    
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

def creating_panel_df(list_tahun_input, kode_kk_cd):
    # list_tahun: list, berisi list tahun dari tahun awal sampai tahun akhir
    # kode_kk: list berisi str, contoh kode_kepri
    
    # list_tahun = ['2016', '2019', '2020']
    # kode_kk_cd = kode_sulsel
    
    for t in list_tahun_input:
        pdrb_t = cleaning_df(t, kode_kk_cd)['PDRB DF']
        
        if t==list_tahun_input[0]:
            pdrb_merge = cleaning_df(list_tahun_input[0], kode_kk_cd)['PDRB DF']
        else:
            pdrb_merge = pd.merge(pdrb_merge, pdrb_t,
                                  on=['Nama Kab/Kota', 'Lapangan Usaha'],
                                  how='inner')
    return pdrb_merge


def target_col_row(matrix_update=None, panel_df=None, industry_name_input=None,
                   adjusment_vector=True):
    
    # Masih dalam konstruksi!!!
    
    # Fungsi ini hanya berlaku untuk Tabel Input-Output 17 Lapangan Usaha.
    # matrix_update: mat, matrix yang akan diupdate.
    # panel_df: dataframe, dataframe berbentuk panel hasil dari function creating_panel_df.
    # industry_name_input: list, list yang berisi nama industri/lapangan usaha hasil dari function initial_identification.
    
    
    # matrix_update = matZ_before_update
    # panel_df = pdrb_papbar
    # industry_name_input = industry_name
    # adjusment_vector=False
    
    panel_df = panel_df.drop('pertumbuhan', axis=1)
    # Mengganti nama lapangan usaha di panel_df agar sesuai dengan industry_name_input
    panel_edited = panel_df.drop(panel_df.index[0])
    pattern_removed = ['PDRB ADHK Tahun Dasar 2010 Berdasarkan Lapangan Usaha - ', 'PDRB ADHK Tahun Dasar 2010 Berdasarkan Lapangan Usaha -', ',', ';']
    
    for p in pattern_removed:
        panel_edited['Lapangan Usaha'] = panel_edited['Lapangan Usaha'].str.replace(p, '')
    
    for p2 in pattern_removed[-2:]:
        industry_name_input = [x.replace(p2, '') for x in industry_name_input]
    
    # estimasi pertumbuhan per lapangan usaha
    colnames = list(panel_edited.columns)
    panel_edited['Pertumbuhan'] = (panel_edited[colnames[-1]] - panel_edited[colnames[-2]])/panel_edited[colnames[-2]]
    panel_final = panel_edited[['Lapangan Usaha', 'Pertumbuhan']]
    panel_final['Lapangan Usaha'] = panel_final['Lapangan Usaha'].replace('Real Estat', 'Real Estate') 
    
    industry_name_df = pd.DataFrame({'Lapangan Usaha':industry_name_input})
    df_merge = pd.merge(industry_name_df, panel_final,
                        on='Lapangan Usaha',
                        how='inner')
    
    rs = matrix_update.sum(axis=1) # rs = row sum
    cs = matrix_update.sum(axis=0) # cs = col sum

    # Row and Column Target
    vec_growth1 = 1 + df_merge['Pertumbuhan'].to_numpy(dtype=float)
    u_target = rs * vec_growth1 # row target

    vec_growth2 = 1 + df_merge['Pertumbuhan'].to_numpy(dtype=float)
    v_target = cs * vec_growth2 # col target

    # Adjust the values to ensure the same sum
    diff = np.sum(u_target) - np.sum(v_target)

    # Spread out the difference across all the elements equally
    if adjusment_vector==True:
        diff_spread = diff / len(v_target)
        for i in range(len(v_target)): v_target[i] += diff_spread
    
    dict_result = {'u_target':u_target,
                   'v_target':v_target}
    
    return dict_result

def io_analysis(clean_matrix=None, list_industry=None, 
                input_industry_name=None,
                delta_fd_input=None,
                delta_va_input=None,
                first_round_id=None):
    
    # clean_matrix = matrix_clean_papbar
    # list_industry = industry_name_papbar
    # input_industry_name = sektor_unggulan_lq_papbar[2]
    # delta_fd_input = 1
    # delta_va_input = 1
    # first_round_id='Demand'
    # first_round_id='Demand' or 'Supply'
    
    # Multiplier and Linkage Analysis
    # Demand-Side Multiplier
    indeks_bb = list_industry.index(input_industry_name)
    delta_fd = pd.DataFrame([0] * len(clean_matrix['Vector Final Demand']))
    vec_dfd = delta_fd.to_numpy(dtype=int)
    vec_dfd[indeks_bb] = delta_fd_input #disesuaikan dengan nilai impor industri
    new_output = np.matmul(clean_matrix['Matrix Leontief Inverse'], vec_dfd)
    multiplier_demand = np.sum(new_output)
    
    # Supply Side Multiplier
    delta_va = pd.DataFrame([0] * len(clean_matrix['Vector Value Add']))
    vec_dva = delta_va.to_numpy(dtype=int)
    vec_dva[indeks_bb] = delta_va_input #disesuaikan dengan tambahan value added idustri
    new_output_supply = np.matmul(clean_matrix['Matrix G Inverse'], vec_dva)
    multiplier_supply = np.sum(new_output_supply)
    
    # Linkage (Source: Miller and Blair)
    # Backward Linkage
    colsum_A = np.sum(clean_matrix['Matrix A'], axis=0)
    rowsum_A = np.sum(clean_matrix['Matrix A'], axis=1)
    nrow_A = clean_matrix['Matrix A'].shape[0]
    # ncol_A = mat_A.shape[1]
    denominator_BL = np.matmul(colsum_A, rowsum_A)
    numerator_BL = nrow_A * colsum_A
    backward_linkage = numerator_BL/denominator_BL # Normalized backward linkage
    bl_j = backward_linkage[indeks_bb] # Normalized Direct Backward Linkage for [Industry_Name]
    # Angka BL menunjukkan bahwa [Industry_Name] memliki kategori (above average atau below average)
    # atau linkage yang kuat/lemah sebagai pembeli
    
    # Direct Backward Linkage
    direct_bl_j = colsum_A[indeks_bb]
    
    # Indirect Backward Linkage
    colsum_L = np.sum(clean_matrix['Matrix L'], axis=0)
    total_bl_j = colsum_L[indeks_bb]
    indirect_bl_j = total_bl_j - direct_bl_j
    
    
    # Direct Forward Linkage
    colsum_B = np.sum(clean_matrix['Matrix B'], axis=0)
    rowsum_B = np.sum(clean_matrix['Matrix B'], axis=1)
    nrow_B = clean_matrix['Matrix B'].shape[0]
    denominator_FL = np.matmul(colsum_B, rowsum_B)
    numerator_FL = nrow_B * colsum_B
    forward_linkage = numerator_FL/denominator_FL # Normalized forward linkage
    fl_j = forward_linkage[indeks_bb] # Normalized Direct Forward Linkage for [Industry_Name]
    # Angka BL menunjukkan bahwa [Industry_Name] memliki kategori (above average/below average)
    # atau linkage yang kuat/lemah sebagai suplier
    
    # Direct Forward Linkage
    direct_fl_j = rowsum_B[indeks_bb]
    
    # Indirect Forward Linkage
    rowsum_G = np.sum(clean_matrix['Matrix G'], axis=1)
    total_fl_j = rowsum_G[indeks_bb]
    indirect_fl_j = total_fl_j - direct_fl_j
    
    
    # Indeks Daya Penyebaran dan Indeks Derajat Kepekaan
    colsum_L = np.sum(clean_matrix['Matrix Leontief Inverse'], axis=0)
    rowsum_L = np.sum(clean_matrix['Matrix Leontief Inverse'], axis=1)
    sumcolsum_L = np.sum(colsum_L)
    sumrowsum_L = np.sum(rowsum_L)
    jumlah_industri = len(list_industry)
    idk = (jumlah_industri/sumrowsum_L)*rowsum_L # indeks daya penyebaran
    idp = (jumlah_industri/sumcolsum_L)*colsum_L # indeks derajat kepekaan
    idp_j = idp[indeks_bb]
    idk_j = idk[indeks_bb]
    
    # Industry Effect
    list_result_multiplier_output = [np.round(multiplier_demand,2), 
                                     np.round(multiplier_supply,2)]
    initial_effect = 1
    if first_round_id=='Demand':
        sum_indikator = rowsum_A
        indeks_multiplier = 0
    elif first_round_id=='Supply':
        sum_indikator = rowsum_B
        indeks_multiplier = 1
    first_round_effect = sum_indikator[indeks_bb]
    industrial_support_effect = list_result_multiplier_output[indeks_multiplier] - initial_effect - first_round_effect
    production_induced_effect = first_round_effect + industrial_support_effect
    
    
    analysis_result = {
        'Multiplier Output Demand': np.round(multiplier_demand,4),
        'Multiplier Output Supply': np.round(multiplier_supply,4),
        'Normalized Direct Backward Linkage': np.round(bl_j, 4),
        'Indirect Backward Linkage': np.round(indirect_bl_j, 4),
        'Direct Backward Linkage': np.round(direct_bl_j, 4),
        'Total Backward Linkage' : np.round(total_bl_j, 4),
        'Normalized Direct Forward Linkage': np.round(fl_j, 4),
        'Indirect Forward Linkage': np.round(indirect_fl_j, 4),
        'Direct Forward Linkage': np.round(direct_fl_j, 4),
        'Total Forward Linkage' : np.round(total_fl_j, 4),
        'Indeks Daya Penyebaran': np.round(idp_j, 4),
        'Indeks Derajat Kepekaan': np.round(idk_j, 4),
        'First Round Effect': np.round(first_round_effect, 4),
        'Industrial Support Effect': np.round(industrial_support_effect, 4),
        'Production Induced Effect': np.round(production_induced_effect, 4)
        }
    
    df_analisis_io = pd.DataFrame(analysis_result, index=[0]).reset_index()
    df_melt = pd.melt(df_analisis_io, id_vars=['index'], value_vars=df_analisis_io.columns)
    list_rename = ['Nama Industri', 'Jenis Analisis', 'Nilai']
    df_melt.columns = list_rename
    df_melt['Nama Industri'] = input_industry_name

    return df_melt

# Updating old Matrix based on new matrix Z
def updating_old_matrix(matZ_hasil_update_input=None, matrix_clean_old=None):
    # matZ_hasil_update_input = matZ_hasil_update
    # matrix_clean_old = matrix_clean
    
    # matZ_hasil_update_input = matZ_hasil_update
    # matrix_clean_old = matrix_clean
    
    # Demand Side
    mat_Z = matZ_hasil_update_input
    vec_fd = matrix_clean_old['Vector Final Demand']
    vec_output = np.sum(mat_Z, axis=1) + vec_fd
    
    # vec_output = np.sum(mat_Z, axis=1) + vec_fd
    # mat_output = vec_output * np.identity(len(vec_output))
    mat_output = vec_output * np.identity(len(vec_output))
    inv_x = np.linalg.pinv(mat_output)
    
    mat_A = np.matmul(mat_Z, inv_x)
    mat_L = np.identity(len(mat_A)) - mat_A
    mat_L_inv = np.linalg.inv(mat_L)
    
    # Supply Side
    mat_B = np.matmul(inv_x, mat_Z) # allocation coefficient
    mat_G = np.identity(len(mat_B)) - mat_B
    mat_G_inv = np.linalg.inv(mat_G) # the output inverse
    vec_va = matrix_clean_old['Vector Value Add']
    # vec_input = df_to_clean.iloc[-1, 3:max_col_mat].to_numpy(dtype=float)
    
    updating_result = {
        'Matrix Z': mat_Z,
        'Matrix A': mat_A,
        'Matrix L': mat_L,
        'Matrix Leontief Inverse': mat_L_inv,
        'Matrix B': mat_B,
        'Matrix G': mat_G,
        'Matrix G Inverse': mat_G_inv,
        'Vector Output': vec_output,
        'Vector Value Add': vec_va,
        'Vector Final Demand': vec_fd
        }
    
    return updating_result

def run_update_provinsi(file_name_prov=None, kode_prov=None, tahun_list=None,
                        list_lu_lq=None, list_lu_ss=None):
    
    # file_name_prov: str, 'Data/Tabel Input-Output Provinsi Sulawesi Selatan Transaksi Domestik Atas Dasar Harga Produsen (17 Lapangan Usaha) 2016 (Juta Rupiah).xlsx'
    # kode_prov: list
    # tahun_list: list
    # list_lu_lq: list
    # list_lu_ss: list
    
    # file_name_prov = file_name_17_sulsel
    # kode_prov = kode_sulsel
    # tahun_list = list_tahun
    # list_lu_lq = sektor_unggulan_lq_sulsel
    # list_lu_ss = sektor_unggulan_ss_sulsel
    
    df_io = pd.read_excel(file_name_prov)
    matrix_id = initial_identification(df_io)
    matrix_clean = cleaning_matrix(df_io)
    industry_name = matrix_id['Industry Name']
    
    # Mendefinisikan row dan col target
    matA_before_update = matrix_clean['Matrix A']
    matZ_before_update = matrix_clean['Matrix Z']

    pdrb_prov = creating_panel_df(list_tahun_input=tahun_list, kode_kk_cd=kode_prov)
    pdrb_prov_col = pdrb_prov.columns
    pdrb_prov['pertumbuhan'] = (pdrb_prov[pdrb_prov_col[-1]] - pdrb_prov[pdrb_prov_col[-2]])/pdrb_prov[pdrb_prov_col[-2]]
    
    u_targetA = target_col_row(matA_before_update, pdrb_prov, industry_name, adjusment_vector=False)['u_target']
    v_targetA = target_col_row(matA_before_update, pdrb_prov, industry_name, adjusment_vector=False)['v_target']

    u_targetZ = target_col_row(matZ_before_update, pdrb_prov, industry_name, adjusment_vector=False)['u_target']
    v_targetZ = target_col_row(matZ_before_update, pdrb_prov, industry_name, adjusment_vector=False)['v_target']

    hasil_updateA = updating_IO(matA_before_update, u_targetA, v_targetA, 10000)
    hasil_updateZ = updating_IO(matZ_before_update, u_targetZ, v_targetZ, 10000)
    
    indeks_min = hasil_updateA['Index Minimum']
    # Hasil indeks_min = 0 artinya metode classic ipf adalah yg terbaik
    # hasil indeks_min = 1 artinya metode factor ipf adalah yg terbaik
    # hasil indeks_min = 2 artinya metode ipfn dari github adalah yg terbaik

    matA_hasil_update = hasil_updateA['Matrix Result']
    matZ_hasil_update = hasil_updateZ['Matrix Result']

    matrix_clean_prov_updated = updating_old_matrix(matZ_hasil_update,
                                                    matrix_clean)
    
    for l in range(len(list_lu_lq)):
        analisis_io_prov_lq = io_analysis(clean_matrix=matrix_clean_prov_updated,
                                          list_industry=industry_name,
                                          input_industry_name=list_lu_lq[l],
                                          delta_fd_input=1,
                                          delta_va_input=1,
                                          first_round_id='Demand')
        
        analisis_io_prov_ss = io_analysis(clean_matrix=matrix_clean_prov_updated,
                                          list_industry=industry_name,
                                          input_industry_name=list_lu_ss[l],
                                          delta_fd_input=1,
                                          delta_va_input=1,
                                          first_round_id='Demand')
        if l==0:
            df_concat_lq = analisis_io_prov_lq
            df_concat_ss = analisis_io_prov_ss
        else:
            df_concat_lq = pd.concat([df_concat_lq, analisis_io_prov_lq], axis=0)
            df_concat_ss = pd.concat([df_concat_ss, analisis_io_prov_ss], axis=0)
        
    dict_run_results = {
        'PDRB Prov Growth': pdrb_prov,
        'Algoritma Terbaik': indeks_min,
        'Matrix A Hasil Update': matA_hasil_update,
        'Matrix Z Hasil Update': matZ_hasil_update,
        'Hasil Analisis IO Hasil Update LQ': df_concat_lq,
        'Hasil Analisis IO Hasil Update SS': df_concat_ss
        }
    
    return dict_run_results

# Running function
# Hati2 matrix before update keubah sendiri mengikuti hasil update, perlu load ulang

kode_sulsel = ['7300']
kode_kepri = ['2100']
kode_papbar = ['9100']
list_tahun = ['2016', '2020'] # tahun awal harus 2016, sedangkan tahun akhir harus setelag 2016

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

