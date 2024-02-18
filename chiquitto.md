# Criar o ambiente CONDA

```bash
conda create python=3.10.9 --name TEclass2Chiquitto -y

conda activate TEclass2Chiquitto

conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

conda install anaconda::biopython
pip install matplotlib==3.5.1
pip install numpy==1.22.3
pip install pandas==1.4.2
pip install PyYAML==6.0
pip install scikit-learn==1.0.2
pip install scipy==1.8.0
pip install tokenizers==0.11.6
pip install tqdm==4.63.0
pip install transformers==4.17.0
pip install tensorboardX==2.5

apt-get install libssl-dev libffi-dev
pip install pyyaml

# To resolve the Error:
# If you cannot immediately regenerate your protos, some other possible workarounds are:
# 1. Downgrade the protobuf package to 3.20.x or lower.
# 2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).
pip install protobuf==3.20.*
```
# Download from DFAM

```bash
wget https://www.dfam.org/releases/Dfam_3.7/families/Dfam.embl.gz -P data/downloaded
gzip -dck data/downloaded/Dfam.embl.gz > data/Dfam.embl
```

# Download from REPBASE

```bash
wget https://www.girinst.org/server/RepBase/protected/RepBase28.12.fasta.tar.gz -P data/downloaded
```

But didnt work

# Criar copia do arquivo de configuração

```bash
cp config.yml config_chiquitto.yml
```

# Amostragem do conjunto de dados

Pegar as primeiras 25k sequencias
```bash
cat -n data/Dfam.embl | grep "ID   " | head -n 15000 | tail
```
linha 943151

```bash
head -n 943150 data/Dfam.embl > data/Dfam_head.embl
```

# Preparar o arquivo Dfam para o TEclass2_database

```bash
python utils/dfam_embl2embl.py data/Dfam_head.embl data/Dfam_corrected.embl
```

# Filtrar dataset *.embl

```bash
python utils/embl_filter.py data/Dfam.embl data/Dfam_Mammalia.embl "Mammalia.*"
python utils/embl_filter.py data/Dfam.embl data/Dfam_Drosophila.embl "Drosophila.*"
python utils/embl_filter.py data/Dfam.embl data/Dfam_Timema.embl "Timema.*"
python utils/embl_filter.py data/Dfam.embl data/Dfam_Lysandra.embl "Lysandra.*"
```

# Criar o database

```bash
mkdir data/databases
python TEclass2.py --database -c config_chiquitto.yml > log_database.txt
```

# Treinamento

```bash
mkdir models
nohup python TEclass2.py --train -c config_chiquitto.yml &> log_train.txt &
```
[1] 345658

Para acompanhar os logs do treinamento

```bash
tail -f log_train.txt
```

Para resolver o problema (warning) `" of type <class 'str'> for key "eval/report" as a scalar. This invocation of Tensorboard's writer.add_scalar() is incorrect so we dropped this attribute.`, use esta página:

https://discuss.huggingface.co/t/trainer-gives-error-after-1st-epoch-and-evaluation/4006/2
https://huggingface.co/docs/transformers/training?highlight=compute_metrics

# Classificar sequencias

```bash
python TEclass2.py --classify -c config_chiquitto.yml -f tests/drosophila.final.TEs.fa -o outfile.log &> ./classified.log
```

# Tricks - Data analysis

Obter a quantidade de dados por especie do dataset:

```bash
grep "^OS" < data/Dfam.embl | awk '{print substr($0,6) }' | sort | uniq -c | sort -nr > data/count_OS1.txt
grep "^OS" < data/Dfam.embl | awk '{print $2 }' | sort | uniq -c | sort -nr > data/count_OS2.txt

grep "^ID   " < data/Dfam.embl | wc -l
grep "^ID   " < data/Dfam_Mammalia.embl | wc -l
grep "^ID   " < data/Dfam_Drosophila.embl | wc -l
grep "^ID   " < data/Dfam_Timema.embl | wc -l
grep "^ID   " < data/Dfam_Lysandra.embl | wc -l
ls -alh data/Dfam.embl data/Dfam_*
```

# Modelo TEclass2
```bash
mkdir models/teclass2
cd models/teclass2
wget https://www.bioinformatics.uni-muenster.de/share/TEclass2/model/config.json
wget https://www.bioinformatics.uni-muenster.de/share/TEclass2/model/optimizer.pt
wget https://www.bioinformatics.uni-muenster.de/share/TEclass2/model/pytorch_model.bin
wget https://www.bioinformatics.uni-muenster.de/share/TEclass2/model/rng_state.pth
wget https://www.bioinformatics.uni-muenster.de/share/TEclass2/model/scheduler.pt
wget https://www.bioinformatics.uni-muenster.de/share/TEclass2/model/trainer_state.json
wget https://www.bioinformatics.uni-muenster.de/share/TEclass2/model/training_args.bin
```

# Para executar com Drosophila

Execute os comandos a seguir.
Há instruções para serem executadas manualmente.

```bash
# cd TEClass_folder
# Ativar ambiente conda (conda activate TEclass2Chiquitto)
cp config_chiquitto.yml config_Drosophila.yml
# Editar o config_Drosophila.yml e alterar model_name=Drosophila
python utils/dfam_embl2embl.py data/Dfam.embl data/Dfam_corrected.embl
python utils/embl_filter.py data/Dfam_corrected.embl data/Dfam_Drosophila.embl "Drosophila.*"
# Editar o config_Drosophila.yml e alterar te_db_path=data/Dfam_Drosophila.embl
# Editar o config_Drosophila.yml e alterar dataset_path=data/databases/Dfam_Drosophila
python TEclass2.py --database -c config_Drosophila.yml > log_database_Drosophila.txt
# Conferir no log_database_Drosophila se o total foi de 62191
# Observar o log_database_Drosophila e identificar os elementos com contagem igual a zero,
# e remover do config os te_keywords esses com contagem zero
nohup python TEclass2.py --train -c config_Drosophila.yml &> log_train_Drosophila.txt &
```

```bash
# cd TEClass_folder
# Ativar ambiente conda (conda activate TEclass2Chiquitto)
cp config_chiquitto.yml config_Danio.yml
# Editar o config_Danio.yml e alterar model_name=Danio
python utils/dfam_embl2embl.py data/Dfam.embl data/Dfam_corrected.embl
python utils/embl_filter.py data/Dfam_corrected.embl data/Dfam_Danio.embl "Danio.*"
# Editar o config_Danio.yml e alterar te_db_path=data/Dfam_Danio.embl
# Editar o config_Danio.yml e alterar dataset_path=data/databases/Dfam_Danio
python TEclass2.py --database -c config_Danio.yml > log_database_Danio.txt
# Conferir no log_database_Danio se o total foi de 62191
# Observar o log_database_Danio e identificar os elementos com contagem igual a zero,
# e remover do config os te_keywords esses com contagem zero
nohup python TEclass2.py --train -c config_Danio.yml &> log_train_Danio.txt &
```

```bash
# cd TEClass_folder
# Ativar ambiente conda (conda activate TEclass2Chiquitto)
cp config_chiquitto.yml config_Oncorhynchus.yml
# Editar o config_Oncorhynchus.yml e alterar model_name=Oncorhynchus
python utils/dfam_embl2embl.py data/Dfam.embl data/Dfam_corrected.embl
python utils/embl_filter.py data/Dfam_corrected.embl data/Dfam_Oncorhynchus.embl "Oncorhynchus.*"
# Editar o config_Oncorhynchus.yml e alterar te_db_path=data/Dfam_Oncorhynchus.embl
# Editar o config_Oncorhynchus.yml e alterar dataset_path=data/databases/Dfam_Oncorhynchus
python TEclass2.py --database -c config_Oncorhynchus.yml > log_database_Oncorhynchus.txt
# Conferir no log_database_Oncorhynchus se o total foi de 62191
# Observar o log_database_Oncorhynchus e identificar os elementos com contagem igual a zero,
# e remover do config os te_keywords esses com contagem zero
nohup python TEclass2.py --train -c config_Oncorhynchus.yml &> log_train_Oncorhynchus.txt &
```

```bash
# cd TEClass_folder
# Ativar ambiente conda (conda activate TEclass2Chiquitto)
cp config_chiquitto.yml config_Heliconius.yml
# Editar o config_Heliconius.yml e alterar model_name=Heliconius
python utils/dfam_embl2embl.py data/Dfam.embl data/Dfam_corrected.embl
python utils/embl_filter.py data/Dfam_corrected.embl data/Dfam_Heliconius.embl "Heliconius.*"
# Editar o config_Heliconius.yml e alterar te_db_path=data/Dfam_Heliconius.embl
# Editar o config_Heliconius.yml e alterar dataset_path=data/databases/Dfam_Heliconius
python TEclass2.py --database -c config_Heliconius.yml > log_database_Heliconius.txt
# Conferir no log_database_Heliconius se o total foi de 62191
# Observar o log_database_Heliconius e identificar os elementos com contagem igual a zero,
# e remover do config os te_keywords esses com contagem zero
nohup python TEclass2.py --train -c config_Heliconius.yml &> log_train_Heliconius.txt &
```

```bash
# cd TEClass_folder
# Ativar ambiente conda (conda activate TEclass2Chiquitto)
cp config_chiquitto.yml config_Timema.yml
# Editar o config_Timema.yml e alterar model_name=Timema
python utils/dfam_embl2embl.py data/Dfam.embl data/Dfam_corrected.embl
python utils/embl_filter.py data/Dfam_corrected.embl data/Dfam_Timema.embl "Timema.*"
# Editar o config_Timema.yml e alterar te_db_path=data/Dfam_Timema.embl
# Editar o config_Timema.yml e alterar dataset_path=data/databases/Dfam_Timema
python TEclass2.py --database -c config_Timema.yml > log_database_Timema.txt
# Conferir no log_database_Timema se o total foi de 62191
# Observar o log_database_Timema e identificar os elementos com contagem igual a zero,
# e remover do config os te_keywords esses com contagem zero
nohup python TEclass2.py --train -c config_Timema.yml &> log_train_Timema.txt &
```