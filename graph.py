import pandas as pd
import matplotlib.pyplot as plt

# 1) Ölçüm sonuçlarını bir sözlükte tanımlayıp DataFrame'e dönüştürüyoruz
data = {
    'Senaryo': ['Ethernet', 'Loss5_Delay50', 'WiFi_5G'],
    'Gönderme_Mbps': [6452.42, 4540.7, 1373.23],
    'Alma_Mbps':    [6452.10, 4540.55, 1373.13]
}
df = pd.DataFrame(data)

# 2) Grafik boyutunu belirliyoruz
plt.figure(figsize=(8, 4))

# 3) "Gönderme" ve "Alma" serilerini çiziyoruz
plt.plot(df['Senaryo'], df['Gönderme_Mbps'],
         marker='o', linewidth=2, label='Gönderme')
plt.plot(df['Senaryo'], df['Alma_Mbps'],
         marker='o', linewidth=2, label='Alma')

# 4) Eksen etiketleri ve başlık ekliyoruz
plt.xlabel('Senaryo')
plt.ylabel('Throughput (Mbps)')
plt.title('Ağ Performans Ölçümleri')

# 5) Legend ve ızgara görünürlüğü
plt.legend()
plt.grid(True)

# 6) Grafik düzenini sıkıştırıp kaydediyoruz
plt.tight_layout()
plt.savefig('network_performance.png', dpi=300)

# 7) Grafiği ekranda gösteriyoruz
plt.show()
