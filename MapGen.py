import pandas as pd 
import folium
import webbrowser
from geopy.distance import geodesic

df = pd.read_csv("apagao_log_test.csv")

if not df.empty:
    lat_media = df["latitude"].mean()
    lng_media = df["longitude"].mean()
    centro = (lat_media, lng_media)

    raio_max = max(
        geodesic(centro, (row["latitude"], row["longitude"])).meters
        for _, row in df.iterrows()
    )

    mapa = folium.Map(location=centro, zoom_start=14)

    # Adicionar círculo vermelho para a área de apagões
    folium.Circle(
        location=centro,
        radius=raio_max + 100,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.4,
        popup="Área de apagões"
    ).add_to(mapa)

    # Adicionar marcadores azuis nos pontos de apagão
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.8,
            popup=f"{row['cidade']} ({row['timestamp']})"
        ).add_to(mapa)

    mapa.save("mapa_apagao.html")
    print("🗺️ Mapa salvo como 'mapa_apagao.html'")
    webbrowser.open("mapa_apagao.html")
else:
    print("⚠️ Nenhum dado encontrado no CSV.")
