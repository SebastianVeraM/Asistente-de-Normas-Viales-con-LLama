# Asistente de Normas Viales CDMX con Llama

Asistente de línea de comandos que responde preguntas sobre normas viales de la Ciudad de México usando recuperación aumentada por generación (RAG). Busca fragmentos relevantes en los documentos PDF del proyecto, los entrega a Llama 2 y muestra las fuentes consultadas.

También incluye una comprobación de circulación por terminación de placa. Esa función es actualmente una **regla de demostración simplificada**; no refleja el calendario oficial completo ni contingencias ambientales. No debe usarse para decidir si un vehículo puede circular.

## Funciones actuales

- Carga tres documentos PDF locales y extrae su texto.
- Divide el texto en fragmentos de 1,000 caracteres con 150 de traslape.
- Busca los tres fragmentos más relevantes con FAISS y embeddings multilingües.
- Genera respuestas en español con `meta-llama/Llama-2-7b-chat-hf`.
- Imprime los nombres de archivo y páginas recuperados como fuentes.
- Acepta consultas de placa con el formato `placa:ABC1234`.

## Requisitos

- Python 3.12 (el entorno de desarrollo del proyecto usa esta versión).
- Espacio en disco y memoria suficientes para Llama 2 7B. Los pesos descargados ocupan aproximadamente 13.5 GB; cargar y generar respuestas en CPU puede tardar varios minutos.
- Cuenta de Hugging Face con acceso aprobado a `meta-llama/Llama-2-7b-chat-hf`.
- Los dos modelos deben estar descargados en la caché local de Hugging Face antes de ejecutar la aplicación. El código usa `local_files_only=True`, por lo que no intenta descargarlos al iniciar.

## Documentos

Coloca estos archivos PDF en la carpeta raíz del proyecto:

- `REGLAMENTO_DE_TRNSITO_DE_LA_CIUDAD_DE_MXICO_6.4.pdf`
- `Programa_Hoy_No_Circula.pdf`
- `Gaceta_Oficial_DF.pdf`

Los nombres deben coincidir exactamente. El programa termina con un error claro si falta un archivo o si no se puede extraer texto. Los PDF escaneados requieren OCR antes de usarse.

## Instalación en Windows

Abre PowerShell en la carpeta del proyecto y crea el entorno virtual:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Instala las dependencias:

```powershell
pip install langchain langchain-classic langchain-community langchain-core langchain-huggingface langchain-text-splitters sentence-transformers transformers torch pypdf faiss-cpu
```

Si PowerShell bloquea la activación, puedes invocar el Python del entorno directamente con `\.venv\Scripts\python.exe`.

## Preparar los modelos

Primero acepta los términos y solicita acceso a Llama 2 en Hugging Face. Después inicia sesión desde el entorno virtual y descarga los dos modelos una sola vez:

```powershell
hf auth login
hf download meta-llama/Llama-2-7b-chat-hf
hf download sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

El token es personal: no lo pegues en el código ni lo subas al repositorio. Cuando los modelos estén en la caché, la aplicación los carga desde allí.

## Ejecutar

```powershell
python app.py
```

La primera inicialización lee los PDFs, calcula los embeddings de todos sus fragmentos y carga Llama. El índice FAISS se reconstruye en cada inicio, así que esa etapa también puede tardar.

Escribe una pregunta, por ejemplo:

```text
¿Cuál es el límite de velocidad indicado para estacionamientos?
```

Para probar el verificador simplificado de placas:

```text
placa:ABC1234
```

Escribe `salir` para cerrar la aplicación. La respuesta de Llama no se transmite gradualmente: aparece completa al terminar la generación. El máximo actual es de 128 tokens; el tiempo depende del hardware y puede ser largo en CPU.

## Estructura

```text
.
├── app.py                  # Interfaz de consola y bucle de preguntas
├── plate_checker.py        # Verificación de placa de demostración
├── rag_pipeline.py         # Carga de PDFs, FAISS, embeddings y Llama
├── Gaceta_Oficial_DF.pdf
├── Programa_Hoy_No_Circula.pdf
└── REGLAMENTO_DE_TRNSITO_DE_LA_CIUDAD_DE_MXICO_6.4.pdf
```

## Alcance y limitaciones

- Es un prototipo educativo e informativo, no una fuente oficial ni asesoría legal.
- Las respuestas dependen del contenido y vigencia de los PDFs disponibles. Revisa siempre el documento oficial vigente.
- La comprobación `placa:` es ilustrativa y no consulta holograma, tipo de combustible, día festivo ni contingencias.
- El sistema actual no conserva el índice FAISS entre ejecuciones y no transmite tokens en streaming.

## Archivos locales y credenciales

No agregues al control de versiones el entorno `.venv`, tokens, archivos `.env` ni cachés de modelos. Guarda los tokens mediante `hf auth login` o variables de entorno seguras, nunca dentro del código fuente.
