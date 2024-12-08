Subdomain Scanner - Proje Açıklaması
Bu Subdomain Scanner aracı, bir ana domain (veya hedef domain) üzerinde alt domain taraması yaparak, bulunan alt domainlerin IP adreslerini, status kodlarını (200, 403, 404 vb.), teknolojilerini ve sunucu bilgilerini listeler. Bu araç, güvenlik araştırmacıları ve penetrasyon test uzmanları için oldukça yararlı olabilir.

Özellikler
Alt Domain Tarama: Subdomain taraması için subfinder aracı kullanılır.
Status Kodu Filtreleme: Kullanıcıya, yalnızca belirli HTTP status kodlarını (200, 403 vb.) görme seçeneği sunulur.
Teknoloji Tespiti: Alt domainlerin kullandığı teknolojiler (örneğin, web server yazılımı, framework vs.) tespit edilir ve kullanıcıya sunulur.
Sunucu Bilgileri: Alt domainlere yapılan HTTP isteği sonrası, sunucu bilgileri alınır ve listelenir.
Detaylı Bilgi Görünümü: Kullanıcı, alt domainin üzerine tıklayarak, ilgili request ve response bilgilerini ayrıntılı olarak görebilir.
İlerleme Barı: Tarama ilerlemesi, her bir domainin taranıp taranmadığına dair bir ilerleme çubuğu ile gösterilir.
Kullanıcı Dostu Arayüz: PySimpleGUI kullanılarak geliştirilmiş kullanıcı dostu bir grafiksel arayüz.
Yeni Tarama Başlatma ve Yenileme: Kullanıcı, tarama bittikten sonra yeni bir tarama başlatabilir veya mevcut taramayı yenileyebilir.
Kullanıcı Özellikleri
Domain Seçimi: Kullanıcı, taramak istediği domaini girer ve tarama başlatılır.
Status Kodu Seçimi: Kullanıcı, görmek istediği status kodlarını seçebilir (200, 403 vb.).
Hızlı Tarama: Tarama işlemi, kullanıcı etkileşimi ve zaman kısıtlamalarını göz önünde bulundurarak hızlandırılmıştır.
Tarama Durdurma ve Sürdürme: Tarama başlatıldıktan sonra, kullanıcı taramayı durdurabilir veya devam ettirebilir.
Gereksinimler
Python 3.x: Python 3'ün yüklü olması gerekmektedir.
PySimpleGUI: GUI için PySimpleGUI kütüphanesi gereklidir.
Subfinder: Alt domain taraması yapmak için subfinder aracı yüklü olmalıdır.
Go (Opsiyonel): Subfinder aracını çalıştırmak için Go programlama dili yüklü olmalıdır.
Kurulum
Python 3.x yüklü olduğundan emin olun.
Projeyi klonlayın veya dosyaları indirin.
Gerekli bağımlılıkları yüklemek için şu komutu kullanın:

pip install -r requirements.txt
Subfinder'ı yükleyin (eğer daha önce yüklemediyseniz).
Kullanım

Python dosyasını çalıştırın:

python recon.py

GUI ekranı açılacak ve burada domain bilgilerini girerek taramayı başlatabilirsiniz.
Tarama tamamlandığında, bulunan alt domainlerin bilgileri ekranda görüntülenecektir.
