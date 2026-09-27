import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Configuración de la página Web
st.set_page_config(
    page_title="Smart Web Scraper AI", page_icon="🕷️", layout="wide"
)

st.title("🕷️ Smart Web Scraper & Data Extractor")
st.write(
    "Introduce la URL de cualquier página web para extraer sus datos"
    " estructurados automáticamente."
)

# Entrada de la URL
url = st.text_input(
    "URL del sitio web:", placeholder="https://ejemplo.com/productos"
)

if st.button("Extraer Datos"):
  if not url:
    st.warning("Por favor, introduce una URL válida.")
  else:
    try:
      with st.spinner("Analizando y extrayendo contenido del sitio web..."):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
          soup = BeautifulSoup(response.text, "html.parser")

          # 1. Extraer Encabezados (H1, H2, H3)
          headings = []
          for tag in ["h1", "h2", "h3"]:
            for item in soup.find_all(tag):
              text = item.get_text(strip=True)
              if text:
                headings.append({"Etiqueta": tag.upper(), "Texto": text})

          df_headings = pd.DataFrame(headings)

          # 2. Extraer Enlaces
          links = []
          for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if href.startswith("http"):
              links.append({"Texto del Enlace": text or "Sin Texto", "URL": href})

          df_links = pd.DataFrame(links)

          # Mostrar resultados en la interfaz
          st.success("¡Extracción completada con éxito!")

          col1, col2 = st.columns(2)

          with col1:
            st.subheader("Encabezados encontrados")
            st.dataframe(df_headings, use_container_width=True)
            if not df_headings.empty:
              csv_h = df_headings.to_csv(index=False).encode("utf-8")
              st.download_button(
                  "Descargar Encabezados (CSV)",
                  csv_h,
                  "encabezados.csv",
                  "text/csv",
              )

          with col2:
            st.subheader("Enlaces encontrados")
            st.dataframe(df_links, use_container_width=True)
            if not df_links.empty:
              csv_l = df_links.to_csv(index=False).encode("utf-8")
              st.download_button(
                  "Descargar Enlaces (CSV)", csv_l, "enlaces.csv", "text/csv"
              )

        else:
          st.error(
              f"No se pudo acceder a la web. Código de respuesta:"
              f" {response.status_code}"
          )

    except Exception as e:
      st.error(f"Ocurrió un error al procesar la página: {e}")
