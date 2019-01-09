## Chinese Open Entity Relation Extraction

### Extraction Example

> "中国国家主席习近平访问韩国，并在首尔大学发表演讲"

We can extract knowledge triples from the sentence as follows:

- (中国, 国家主席, 习近平)
- (习近平, 访问, 韩国)
- (习近平, 发表演讲, 首尔大学)

### Project Structure

```
knowledge_extraction/
|-- code/  # code directory
|   |-- bean/
|   |-- core/
|   |-- demo/  # procedure entry
|   |-- tool/
|-- data/ # data directory
|   |-- input_text.txt  # input text file
|   |-- knowledge_triple.json  # output knowledge triples file
|-- ltp-models/  # ltp models, can be downloaded from http://ltp.ai/download.html, select ltp_data_v3.4.0.zip
|-- resource  # dictionaries dirctory
|-- requirements.txt  # dependent python libraries
|-- README.md  # project description
```

### Requirements

- Python>=3.6
- pynlpir>=0.5.2
- pyltp>=0.2.1

### Install Dependent libraries

```
pip install -r requirements.txt
```

### Entry procedure

```shell
cd ./code/demo/
python extract_demo.py
```

### Main Implementation Content

![DSNF](https://github-1251903863.cos.ap-shanghai.myqcloud.com/Two%20kinds%20of%20definitions%20of%20DSNFs%20and%20the%20triples%20are%20available%20to%20extract%20from%20DSNFs.png)

### Reference

If you use the code, please kindly cite the following paper:

Jia S, Li M, Xiang Y. Chinese Open Relation Extraction and Knowledge Base Establishment[J]. ACM Transactions on Asian and Low-Resource Language Information Processing (TALLIP), 2018, 17(3): 15.
