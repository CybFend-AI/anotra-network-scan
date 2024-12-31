# network-scan
API'lerin guvenligi icin ortam degiskeni ile saklicaz apileri ortam degiskenini serverda ayarlamak icin assagidakileri yapman lazim

Kalıcı Ortam Değişkeni Ayarlamak
Eğer ortam değişkenini kalıcı hale getirmek istiyorsanız (yani, sunucu her yeniden başlatıldığında veya yeni bir terminal açıldığında değişkenin kaybolmaması için), bashrc veya zshrc dosyasına ekleyebilirsiniz.

Bash kullanıyorsanız:

Profil dosyasını açın (örneğin .bashrc veya .bash_profile):

nano ~/.bashrc

Her API için ortam değişkenlerini ekleyin:

# API 1
export API1_KEY="YourAPI1Key"
export API1_URL="https://api1.example.com"

# API 2
export API2_KEY="YourAPI2Key"
export API2_URL="https://api2.example.com"

# API 3
export API3_KEY="YourAPI3Key"
export API3_URL="https://api3.example.com"

Değişiklikleri kaydedin ve çıkın.

Değişiklikleri uygulayın:
source ~/.bashrc

Evet, eğer birden fazla API kullanıyorsanız, her bir API için ayrı bir ortam değişkeni tanımlamanız gerekir. Bu durumda, .bashrc veya .bash_profile dosyanıza her API için ayrı bir export komutu eklemeniz gerekecektir.

Örnek:
Diyelim ki üç farklı API kullanıyorsunuz ve her biri için bir API Key ve API URL'si var. Bu durumda, her bir API'nin bilgilerini ortam değişkenleri olarak .bashrc dosyanıza eklemeniz gerekir.

Adımlar:
Profil dosyasını açın (örneğin .bashrc veya .bash_profile):

bash
Copy code
nano ~/.bashrc
Her API için ortam değişkenlerini ekleyin:

bash
Copy code
# API 1
export API1_KEY="YourAPI1Key"
export API1_URL="https://api1.example.com"

# API 2
export API2_KEY="YourAPI2Key"
export API2_URL="https://api2.example.com"

# API 3
export API3_KEY="YourAPI3Key"
export API3_URL="https://api3.example.com"
Değişiklikleri kaydedin ve çıkın.

Değişiklikleri uygulayın:

source ~/.bashrc

Python'da Her API'yi Kullanmak
Her bir API'yi kullanırken, ortam değişkenlerinden uygun olanları şu şekilde alabilirsiniz:

import os

# API 1
api1_key = os.getenv("API1_KEY")
api1_url = os.getenv("API1_URL")

# API 2
api2_key = os.getenv("API2_KEY")
api2_url = os.getenv("API2_URL")

# API 3
api3_key = os.getenv("API3_KEY")
api3_url = os.getenv("API3_URL")

# API'lerle işlem yapma
import requests

# Örnek API çağrısı - API 1
headers = {"Authorization": api1_key}
response = requests.post(api1_url, headers=headers)
if response.status_code == 200:
    data = response.json()
    print("API 1 sonuçları:", data)
