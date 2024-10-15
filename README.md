# Discord Kayıt Botu 🤖

<p align="center">
  <img src="https://avatars.githubusercontent.com/u/185111098?v=4" alt="Creator" width="200"/>
</p>

<p align="center">
  <a href="#özellikler">Özellikler</a> •
  <a href="#kurulum">Kurulum</a> •
  <a href="#kullanım">Kullanım</a> •
  <a href="#konfigürasyon">Konfigürasyon</a> •
  <a href="#katkıda-bulunma">Katkıda Bulunma</a> •
</p>

---

## 📝 Açıklama

Bu Discord botu, sunucunuza gelen yeni üyeleri kaydetmek, sunucu etkinliklerini izlemek ve kara liste yönetimi sağlamak için tasarlanmıştır. Gelişmiş kayıt sistemi, olay günlükleme ve özelleştirilebilir yapılandırma seçenekleriyle sunucunuzun yönetimini kolaylaştırır.

## ✨ Özellikler

- 📊 Gelişmiş üye kaydı sistemi
- 🚫 Kara liste yönetimi
- 📜 Detaylı olay günlükleme (giriş, çıkış, kick, ban)
- 🎨 Özelleştirilebilir hoş geldin ve veda mesajları
- 🔒 Rol tabanlı komut yetkilendirmesi
- 🗃️ SQL veritabanı entegrasyonu

## 🚀 Kurulum

1. Repoyu klonlayın:
   ```
   git clone https://github.com/BatuhanAramaz/Veles-Discord-Bot-Register.git
   ```

2. Proje dizinine gidin:
   ```
   cd Veles-Discord-Bot-Register
   ```

3. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

4. `config.json` dosyasını kendi sunucunuza göre düzenleyin.

5. Botu çalıştırın:
   ```
   python main.py
   ```

## 💻 Kullanım

### Kayıt Komutu

```
/register <id> <isim> [yaş]
```

### Kara Liste Komutu

```
/blacklist <@kullanıcı> <sebep>
```

## ⚙️ Konfigürasyon

Botun ayarlarını `config.json` dosyasından özelleştirebilirsiniz:

```json
{
    "token": "YOUR_BOT_TOKEN_HERE",
    "prefix": "!",
    "welcomeChannelId": "123456789012345678",
    "goodbyeChannelId": "123456789012345678",
    "logChannelId": "123456789012345678",
    "registerLogChannelId": "123456789012345678",
    "registerType": 1, //1: İsim|Yaş     2: İsim
    "registerPermissions": [
        "123456789012345678",
        "234567890123456789"
    ],
    "blacklistPermissions": [
        "345678901234567890",
        "456789012345678901"
    ],
    "welcomeRole": "567890123456789012",
    "manRole": "678901234567890123",
    "womanRole": "789012345678901234",
    "blacklistedRole": "890123456789012345",
    "databasePath": "database/bot_database.db",
    "embedColor": "0x3498db",
    "welcomeMessage": "Hoş geldin {user}! Sunucumuza katıldığın için teşekkürler.",
    "goodbyeMessage": "Görüşürüz {user}! Umarız tekrar görüşürüz.",
    "kickMessage": "{user} sunucudan atıldı.",
    "banMessage": "{user} sunucudan yasaklandı.",
    "registerChannels": [
        "901234567890123456",
        "012345678901234567"
    ]
}
```

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir özellik dalı oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: XYZ'`)
4. Dalınıza push yapın (`git push origin yeni-ozellik`)
5. Bir Pull Request oluşturun



---

<p align="center">
  Geliştirici: <a href="https://github.com/BatuhanAramaz">Batuhan Aramaz</a> 👨‍💻
</p>
