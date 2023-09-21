"""
Analisis Tabel Input-Output Provinsi di Indonesia
@author: fawdywahyu
"""

import pandas as pd
import numpy as np

# Initial identification and cleaning matrix
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

def io_analysis(clean_matrix=None, list_industry=None, 
                input_industry_name=None,
                delta_fd_input=None,
                delta_va_input=None,
                first_round_id=None):
    
    # clean_matrix = matrix_clean_sulsel
    # list_industry = industry_name
    # input_industry_name = list_industry[0]
    # delta_fd_input = 1
    # delta_va_input = 1
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
    indirect_bl_j = colsum_L[indeks_bb]
    
    
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
    
    # Indirect Backward Linkage
    rowsum_G = np.sum(clean_matrix['Matrix G'], axis=1)
    indirect_fl_j = rowsum_G[indeks_bb]
    
    
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
        'Direct Backward Linkage': np.round(direct_bl_j, 4),
        'Indirect Backward Linkage': np.round(indirect_bl_j, 4),
        'Normalized Direct Forward Linkage': np.round(fl_j, 4),
        'Direct Forward Linkage': np.round(direct_fl_j, 4),
        'Indirect Forward Linkage': np.round(indirect_fl_j, 4),
        'Indeks Daya Penyebaran': np.round(idp_j, 4),
        'Indeks Derajat Kepekaan': np.round(idk_j, 4),
        'First Round Effect': np.round(first_round_effect, 4),
        'Industrial Support Effect': np.round(industrial_support_effect, 4),
        'Production Induced Effect': np.round(production_induced_effect, 4)
        }
    
    return analysis_result
