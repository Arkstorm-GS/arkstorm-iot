import cv2
import mediapipe as mp
import numpy as np
import time
import geocoder
import pandas as pd
from datetime import datetime

# Inicialização MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Parâmetros
apagao_detectado_count = 0
apagao_registrado = False
tempo_reset = 30  # segundos para resetar o ciclo após apagão detectado
tempo_apagao = None
limite_distancia_min = 0.2
limite_distancia_max = 0.6

estado_mao = "aberta"
sinal_detectado = False
status = "NORMAL"
distancia_mao = 0

font = cv2.FONT_HERSHEY_SIMPLEX

# Alterar para capturar vídeo ou webcam
# Use 'video.mp4' para vídeo ou 0 para webcam. Aqui usamos 0 + backend DirectShow.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: não foi possível acessar a câmera.")
    cap.release()
    hands.close()
    exit()
else:
    print("✅ Câmera aberta com sucesso.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ cap.read() retornou False. Encerrando.")
        break

    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    brilho = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    landmarks_detectados = 0
    mao_fechada = False
    distancia_mao = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks_detectados = len(hand_landmarks.landmark)

            pulso = hand_landmarks.landmark[0]
            centro_palma = hand_landmarks.landmark[9]
            distancia_mao = np.linalg.norm([
                pulso.x - centro_palma.x,
                pulso.y - centro_palma.y
            ])

            dedos_fechados = 0
            ids_dedos = [8, 12, 16, 20]
            for i in ids_dedos:
                # Se a ponta do dedo está abaixo (em y) do ponto intermediário, considera dedo fechado
                if hand_landmarks.landmark[i].y > hand_landmarks.landmark[i - 2].y:
                    dedos_fechados += 1

            if dedos_fechados == 4 and limite_distancia_min <= distancia_mao <= limite_distancia_max:
                mao_fechada = True

    # Detecta transição de mão aberta para fechada
    if mao_fechada and estado_mao == "aberta":
        estado_mao = "fechada"
        sinal_detectado = True
        print("✋ Sinal de mão fechada detectado!")
    elif not mao_fechada and estado_mao == "fechada":
        estado_mao = "aberta"

    if sinal_detectado:
        apagao_detectado_count += 1
        sinal_detectado = False

    # Detectar 3 sinais consecutivos, registra apagão
    if apagao_detectado_count >= 3 and not apagao_registrado:
        status = "APAGAO DETECTADO"
        apagao_registrado = True
        tempo_apagao = time.time()

        # Tenta obter geolocalização por IP
        g = geocoder.ip('me')
        if g.ok:
            dados = {
                "cidade": g.city,
                "latitude": g.latlng[0],
                "longitude": g.latlng[1],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            df = pd.DataFrame([dados])
            df.to_csv("apagao_log.csv", index=False)
            print("📄 Log de apagão salvo em apagao_log.csv")
        else:
            print("⚠️ Não foi possível obter geolocalização.")

    # Reinicia contagem para detectar novo apagão
    if apagao_registrado and (time.time() - tempo_apagao) >= tempo_reset:
        print("⏳ Resetando sistema para novo ciclo...")
        apagao_detectado_count = 0
        apagao_registrado = False
        tempo_apagao = None
        status = "NORMAL"

    # Exibe informações na tela
    cv2.putText(frame, f"Brilho: {brilho:.2f}", (10, 30), font, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Landmarks: {landmarks_detectados}", (10, 60), font, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Distancia: {distancia_mao:.3f}", (10, 90), font, 0.7, (255, 255, 0), 2)
    cv2.putText(frame, f"Sinais: {apagao_detectado_count}", (10, 120), font, 0.7, (255, 255, 255), 2)
    cv2.putText(
        frame,
        f"Status: {status}",
        (10, 150),
        font,
        0.7,
        (0, 0, 255) if "APAGAO" in status else (0, 255, 0),
        2
    )

    cv2.imshow("Apagao Detector", frame)

    # Sai ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()