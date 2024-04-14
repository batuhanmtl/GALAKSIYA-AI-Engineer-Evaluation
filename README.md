# Tool-Based Agent REST API

Bu proje, bir araç tabanlı ajanın sunulduğu bir REST API geliştirmeyi amaçlamaktadır. Ajan, kullanıcı mesajı üzerinde vektör benzerlik araması yapabilen, temel matematik işlemi gerçekleştirebilen ve base64 formatta verilen bir özgeçmiş(pdf,docx,txt) içerisinden belirli bilgilerin(name,about,skills,experience,education,languages,certificates) çıkarımını yapabilen(geliştiriciye bırakılan kısım) araçlara sahiptir.

## Tools

### 1. similarity_search

Bu araç ile SOURCE_DOCUMENTS içerisindeki dokümanlar üzerinde(pdf,docx,txt) prompt based bir şekilde belgeler içerisinden yazdığınız query ile ilgili kısmı(bu çalışmada ilgili bir adet chunk return ediliyor) benzerlik skoru(similarity_L2_score) ile birlikte return eder.

**Request body:**
```json
{
  "query": "sorgu cümlesi"
}
```
	
**Response body:**
```json
[
  {
    "source": ".\\lib\\SOURCE_DOCUMENTS\\ilgili_doküman.(pdf,docx,txt)",
    "content": "Query'e yanıt içermesi muhtemel olan dokümandaki kısmın içeriği",
    "similarity_L2_score": 0.20954060554504395 
  }
]
```
**curl:**

```powershell
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/similarity_search' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "sorgu cümlesi"
}'
```


### 2. math_solver
math_solver aracı ile yapılması istenen temel matematik işleminin sözel(üç artı dört) veya matematiksel temsili(3+4)  olan query'si girilir ve işlem sonucu(örneğin 7) return edilir.


**Request body:**
```json
{
  "query": "yüzyirmibeş bölü beş artı -20 işleminin sonucunun eksi bir ile çarpımının sonucu nedir? "
}
```

**Response body:**
```
"-5.0"
```
**curl:**

```powershell
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/math_solver' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "yüzyirmibeş bölü beş artı -20 işleminin sonucunun eksi bir ile çarpımının sonucu nedir? "
}'
```

### 3. data_extractor

data_extractor aracı ile pdf,docx veya txt dosya tipindeki bir özgeçmiş içerisinden name,about,skills,experience,education,languages,certificates bilgileri extract edilebilir(dokumanda mevcut ise).
Bu aracı kullanmak için belgenin içeriğinin base64 formata çevrilmiş olması gerekmektedir.
Geliştirme aşamasında base64'e converter olarak kullanılan [araç1](https://base64.guru/converter/encode/pdf)(PDF to Base64), [araç2](https://base64.guru/converter/encode/file)(DOCX to Base64)

**Request body:**
```json
{
  "base64": "JVBERi0xLjMKMSAwIG9....",
  "filename": "örnek cv",
  "filetype": "pdf | docx | txt"
}
```
	
**Response body:**
```json
{
  "name": "",
  "about": "",
  "skills": [],
  "experience": [],
  "education": [],
  "languages": [],
  "certificates": []
}
```
**curl:**

```powershell
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/data_extractor' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
   "base64": "JVBERi0xLjMKMSAwIG9...."
   "filename": "örnek cv",
   "filetype": "pdf | docx | txt"
}'
```

## USAGE
### 1. Git'i kullanarak repoyu klonlayın:

```bash
git clone https://github.com/batuhanmtl/GALAKSIYA-AI-Engineer-Evaluation.git
```
### 2. Environment Setup
- #### 2.1. Yeni bir sanal ortam oluşturun ve etkinleştirin.

```powershell
python -m venv .venv

.\.venv\Scripts\activate            
```
- #### 2.2. Install the dependencies using pip

Ortamınızı kodu çalıştıracak şekilde ayarlamak için öncelikle tüm gereksinimleri yükleyin:

```powershell
pip install -r requirements.txt
```
- #### 2.3. ".env" Dosyasında Openai API Key Belirtilmesi
```powershell
OPENAI_API_KEY = "Size ait Openai API key"
```


### 3. START API
 
```powershell
python .\main.py
```

# KAYNAKLAR
- [Langchain Community](https://api.python.langchain.com/en/latest/community_api_reference.html)
- [FAISS](https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.faiss.FAISS.html) 
- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/docs/quickstart?context=python)




