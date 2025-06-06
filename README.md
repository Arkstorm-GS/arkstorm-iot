![Logo do Projeto](https://github.com/user-attachments/assets/169be40e-8e44-41ee-be43-e73022479cd7)

# Arkstorm - Detector de Apagões

Este projeto propõe um sistema de detecção de apagões com uso de visão computacional. Utilizando Python, MediaPipe e uma câmera comum, o sistema detecta gestos manuais em condições de baixa luminosidade para identificar eventos de apagão. Os dados são armazenados localmente com geolocalização e podem ser visualizados em um mapa interativo.

* Julia Marques (RM98680)
* Guilherme Morais (RM551981)
* Matheus Gusmão (RM550826)

Video da solução: https://youtu.be/-ryEcuMbZtg

## 📦 Funcionalidades

* Detecção de gestos de mão em tempo real
* Verificação de distância da mão para evitar ativações indevidas
* Validação do apagão por gestos repetidos
* Registro de localização e horário dos apagões detectados
* Geração de mapa com marcadores e área de abrangência

## 🚀 Tecnologias Utilizadas

* Python 3.10
* OpenCV
* MediaPipe
* Pandas
* Geocoder
* Geopy
* Folium

## 🔧 Dependências

Instale as bibliotecas com:

```bash
pip install opencv-python mediapipe pandas geocoder folium geopy
```

## ⚙️ Execução

1. Execute `main.py` para iniciar o sistema de detecção em tempo real.
2. Para gerar o mapa com os logs registrados, execute `mapa_apagao.py`.

> O log será salvo automaticamente no arquivo `apagao_log.csv`.

## 📋 Exemplo de Log Registrado

```csv
cidade,latitude,longitude,timestamp
São Paulo,-23.5475,-46.6361,2025-06-05 03:50:03
```

## 📈 Visualização do Mapa

* Um mapa interativo é gerado em `mapa_apagao.html`, mostrando:

  * Um **círculo vermelho** cobrindo a área total afetada
  * **Marcadores azuis** para cada ponto de apagão detectado


## 📅 Observações Finais

* O sistema é projetado para uso local e offline com abertura para expansão para bancos de dados e relatorios em tempo real
* Em ambientes escuros, um LED é utilizado para auxiliar a detecção da mão
* Não é necessário servidor ou banco de dados externo
* o arquivo `apagao_log_test.csv` pode ser usado para testar como seria o futuro uso com diversos pontos expalhados

---

> Este projeto integra conceitos de IoT, visão computacional e geolocalização para criar uma ferramenta funcional de monitoramento autônomo de apagões.
