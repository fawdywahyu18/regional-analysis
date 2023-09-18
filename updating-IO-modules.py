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
    
    # matrix_update = mat_update
    # panel_df = pdrb_sulsel
    # industry_name_input = industry_name
    # adjusment_vector=True
    
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
