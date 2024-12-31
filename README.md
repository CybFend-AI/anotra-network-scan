# network-scan
API'lerin guvenligi icin ortam degiskeni ile saklicaz apileri ortam degiskenini serverda ayarlamak icin assagidakileri yapman lazim

Kalıcı Ortam Değişkeni Ayarlamak
Eğer ortam değişkenini kalıcı hale getirmek istiyorsanız (yani, sunucu her yeniden başlatıldığında veya yeni bir terminal açıldığında değişkenin kaybolmaması için), bashrc veya zshrc dosyasına ekleyebilirsiniz.

Bash kullanıyorsanız:

~/.bashrc dosyasını açın:
bash
Copy code
nano ~/.bashrc
Dosyanın sonuna şu satırı ekleyin:
bash
Copy code
export API_KEY="YourSecureApiKey"
Dosyayı kaydedin ve kapatın (Ctrl + X, ardından Y ve Enter).
Zsh kullanıyorsanız (örneğin, macOS'ta varsayılan shell):

~/.zshrc dosyasını açın:
bash
Copy code
nano ~/.zshrc
Dosyanın sonuna şu satırı ekleyin:
bash
Copy code
export API_KEY="YourSecureApiKey"
Dosyayı kaydedin ve kapatın.
Terminali yeniden başlatın ya da şu komutu çalıştırarak ortam değişkenlerini yükleyin:

bash
Copy code
source ~/.bashrc    # Bash için
source ~/.zshrc     # Zsh için
