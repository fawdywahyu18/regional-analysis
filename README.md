# regional-analysis
Panduan Analisis Regional kerjasama dengan Bappenas. Berisi modul LQ, SS, IO, dan Pembaruan tabel IO menggunakan algoritma IPF.

## Panduan melakukan instalasi menggunakan Anaconda Prompt (Miniconda)
1. Download dan install miniconda3
2. Buka Anaconda Prompt
3. Ubah direktori kerja sesuai keinginan. Contohnya adalah `cd C:\Fawdy`
4. Buat virtual environment dengan command `conda create -n venv_name` kemudian muncul 'Proceed?' ketik `y`
5. Aktifkan virtual environment dengan cara `conda activate venv_name`
6. Install git untuk bisa akses github dengan cara `conda install -c anaconda git` kemudian muncul 'Proceed?' ketik `y`

## Cara Melakukan Instalasi Package regional-analysis
1. Mengunduh file dengan cara `git clone https://github.com/fawdywahyu18/regional-analysis.git`
2. cd ke folder yang memiliki file `setup.py'
3. buat dan aktifkan virtual environment
4. pastikan virtual environment dalam kondisi aktif, kemudian ketik `pip install -e .` di terminal. Tunggu instalasi sampai selesai dan sukses.

## Panduan contoh hasil
1. Contoh cara melakukan running script ada di folder 'Example'
2. Contoh hasil output package ada di folder 'Example Output'

## Apabila Anda ingin running menggunakan contoh data yang sama dengan riset
1. Pindah direktori ke folder example dengan cara `cd C:\Fawdy\regional-analysis`
2. Pastikan virtual environment tetap aktif. Kemudian ketik pada terminal `python run_growth_accounting.py`

## Mengubah script untuk running modul LQ, SS, IO, dan Pembaruan (updating) IO
1. Aktifkan virtual environment
2. Install jupyter notebook dengan cara `conda install -c conda-forge notebook`
3. Install nb_conda dengan cara `conda install -c conda-forge nb_conda_kernels`
4. Pastikan modul growth_accounting dan notebook sudah terinstall dengan cara `conda list`
5. Buka jupyter notebook dengan cara `jupyter-notebook`

