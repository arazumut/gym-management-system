# Spor Salonu Yönetim Sistemi

Spor Salonu Yönetim Sistemi, bir fitness merkezi veya spor salonunun yönetimini kolaylaştırmak için tasarlanmış kapsamlı bir web uygulamasıdır. Bu sistem, modern teknolojiler kullanılarak geliştirilmiş olup, spor salonu operasyonlarının verimli bir şekilde yönetilmesini sağlar.

## İçindekiler
- [Özellikler](#özellikler)
- [Teknolojiler](#teknolojiler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

## Özellikler

### Kullanıcı Yönetimi
- **Kimlik Doğrulama ve Yetkilendirme**
  - Güvenli giriş sistemi
  - JWT tabanlı kimlik doğrulama
  - Rol bazlı yetkilendirme (Admin, Eğitmen, Üye)
  
- **Profil Yönetimi**
  - Kişisel bilgi düzenleme
  - Profil fotoğrafı yükleme (Cloudinary entegrasyonu)
  - Şifre değiştirme ve sıfırlama
  - Kullanıcı durumu takibi (online/offline)

### Eğitim ve Program Yönetimi
- **Egzersiz Programları**
  - Özelleştirilebilir egzersiz planları
  - Detaylı egzersiz açıklamaları ve görselleri
  - Set, tekrar ve ağırlık takibi
  
- **Diyet ve Beslenme**
  - Kişiselleştirilmiş beslenme programları
  - Öğün planlaması ve kalori takibi
  - Besin değeri hesaplamaları
  
- **İlerleme Takibi**
  - Vücut ölçüleri kaydı
  - Performans grafikleri
  - Hedef belirleme ve takip

### Üyelik ve Finans Yönetimi
- **Ödeme Sistemi**
  - Stripe entegrasyonu ile güvenli online ödemeler
  - Otomatik fatura oluşturma
  - Ödeme geçmişi takibi
  
- **Üyelik Planları**
  - Farklı üyelik paketleri
  - Özel indirimler ve kampanyalar
  - Üyelik yenileme hatırlatmaları

### İletişim ve Bildirim Sistemi
- **Gerçek Zamanlı İletişim**
  - Anlık mesajlaşma
  - Duyuru sistemi
  - Otomatik email bildirimleri
  
- **Yoklama Sistemi**
  - QR kod ile giriş-çıkış takibi
  - Devam durumu raporlama
  - Katılım istatistikleri

## Teknolojiler

### Frontend
- Next.js 13
- TypeScript
- Material-UI
- SWR
- Axios

### Backend
- Django REST Framework
- PostgreSQL
- Redis
- Celery

### Depolama ve Servisler
- Cloudinary (Medya depolama)
- Stripe (Ödeme sistemi)
- SendGrid (Email servisi)

## Kurulum

### Ön Gereksinimler
- Node.js (v16 veya üzeri)
- Python (v3.8 veya üzeri)
- Egzersiz Programları Oluşturma ve Düzenleme
- Diyet Planları ve Beslenme Takibi
- Özel Antrenman Programları
- İlerleme Takibi ve Raporlama
- Program Şablonları

### Üyelik ve Finans
- Üyelik Planları ve Paketler
- Online Ödeme Sistemi (Stripe Entegrasyonu)
- Ücret Takibi ve Hatırlatmalar
- Fatura Oluşturma
- Finansal Raporlar

### İletişim ve Takip
- Gerçek Zamanlı Bildirimler
- Yoklama Sistemi ve Raporlama
- Eğitmen-Öğrenci İletişimi
- Duyuru ve Mesajlaşma Sistemi
- Otomatik Email Bildirimleri

### Teknik Özellikler
- Responsive Tasarım (Mobil Uyumlu)
- Modern ve Kullanıcı Dostu Arayüz
- Yüksek Performans ve Hız
- Güvenli Veri Depolama
- API Entegrasyonları




