# Asistente de Normas Viales de la Ciudad de México

Prototipo educativo de un asistente basado en Llama que responde preguntas sobre normas viales y contingencias ambientales con recuperación aumentada por generación (RAG). La demostración funcional más reciente está en el notebook `Llama_IA.ipynb` y se ejecuta en Google Colaboratory.

> El proyecto es informativo y experimental. No sustituye las disposiciones oficiales ni asesoría legal. Los PDF incluidos son documentos estáticos; el asistente no consulta en tiempo real si Hoy No Circula o una contingencia están activos.

## Abrir la demostración en Colab

[![Abrir en Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SebastianVeraM/Asistente-de-Normas-Viales-con-LLama/blob/main/Llama_IA.ipynb)

1. Abre el notebook con el enlace anterior e inicia sesión en Colab.
2. En **Entorno de ejecución → Cambiar tipo de entorno de ejecución**, selecciona una GPU si está disponible.
3. En el panel **Secretos** (icono de llave), crea `HF_TOKEN` con un token de lectura de Hugging Face y habilita su uso en el notebook. La cuenta debe tener acceso aprobado a `meta-llama/Llama-3.2-3B-Instruct`.
4. Ejecuta las celdas en orden. El notebook clona este repositorio, lee los PDF, prepara embeddings, recupera fragmentos y carga el modelo.

El token se usa para descargar el modelo desde Hugging Face Hub; la generación de respuestas ocurre en la GPU de Colab. Nunca escribas el token en una celda ni lo guardes en Git. Si Colab reinicia el entorno, vuelve a ejecutar las celdas: el almacenamiento y las variables de la máquina virtual son temporales.

## Flujo RAG implementado

- Extrae texto y páginas de los PDF con `pypdf` y conserva archivo y número de página como metadatos.
- Divide el texto en fragmentos con traslape y calcula embeddings multilingües con `paraphrase-multilingual-MiniLM-L12-v2`.
- Combina similitud semántica con coincidencias léxicas; da prioridad a nombres propios consultados, como municipios, cuando aparecen textualmente en los documentos.
- Amplía cada fragmento recuperado con fragmentos vecinos de la misma página para reducir respuestas incompletas cuando una regla cruza un límite de fragmentación.
- Pasa el contexto y sus fuentes a `meta-llama/Llama-3.2-3B-Instruct`. El prompt pide responder en español, citar documento y página, no inventar y abstenerse cuando falte evidencia. También distingue las definiciones explícitas y exenciones de las inferencias no respaldadas.

El notebook incluye preguntas de prueba sobre límites de velocidad, Ecatepec, contingencias, fuentes de consulta y casos cuya respuesta no aparece en los documentos.

## Por qué se ejecuta en Google Colab

La primera versión intentaba cargar Llama 2 7B en el equipo local. El equipo no tenía memoria y capacidad de cómputo suficientes para ejecutar ese modelo de forma práctica. Por ello, el flujo de demostración se trasladó a Colab, que proporcionó una GPU Tesla T4 con 15 GB de memoria, y se cambió a Llama 3.2 3B Instruct, un modelo más pequeño que sí se pudo cargar en esa GPU.

Este cambio evita depender de la capacidad de cómputo del equipo personal durante la demostración. Colab requiere conexión a Internet para clonar el repositorio y descargar los modelos; la disponibilidad de GPU y la duración de la sesión dependen del servicio.

## Cambios entre la primera versión y la demostración actual

- Se pasó de cargar `meta-llama/Llama-2-7b-chat-hf` localmente a cargar `meta-llama/Llama-3.2-3B-Instruct` en Colab.
- El acceso a Hugging Face se configura mediante `HF_TOKEN` en Secretos de Colab, sin credenciales en el código.
- Se organizó el flujo del notebook desde la carga de documentos hasta la generación de respuestas.
- Se mejoró la recuperación híbrida para preguntas con nombres concretos y se añadió contexto vecino para conservar cláusulas completas.
- Se ajustaron las instrucciones del modelo para respuestas con fuentes, abstención concisa y una interpretación cuidadosa de excepciones explícitas.

No se aplicó fine-tuning con LoRA en esta etapa. La solución actual usa prompting y RAG para fundamentar las respuestas en los documentos.

## Documentos incluidos

- `REGLAMENTO_DE_TRNSITO_DE_LA_CIUDAD_DE_MEXICO_6.4.pdf` (el nombre del archivo del repositorio conserva `TRNSITO`)
- `Programa_Hoy_No_Circula.pdf`
- `Gaceta_Oficial_DF.pdf`

Los resultados dependen de la calidad, fecha y cobertura de estos archivos. Antes de tomar decisiones sobre circulación, contingencias, horarios o restricciones vigentes, consulta los avisos actuales de SEDEMA y de la Comisión Ambiental de la Megalópolis (CAMe).

## Scripts locales heredados

`app.py`, `rag_pipeline.py` y `plate_checker.py` corresponden a la primera aplicación de consola. `rag_pipeline.py` todavía carga Llama 2 7B desde la caché local (`local_files_only=True`), por lo que estos scripts no representan la migración a Colab ni son la ruta recomendada para la demostración actual. `plate_checker.py` contiene reglas simplificadas de ejemplo; no calcula el calendario oficial, hologramas, días festivos ni contingencias.

## Requisitos de Colab

- Cuenta de Google con acceso a Google Colab.
- Token de lectura de Hugging Face y acceso concedido al repositorio del modelo.
- GPU de Colab recomendada. La ejecución se comprobó en una Tesla T4 de 15 GB.
- Los tres PDF del repositorio.

El notebook instala `pypdf`; el entorno de Colab aporta PyTorch, Transformers y Sentence Transformers. Si Colab cambia su imagen base, puede ser necesario instalar o ajustar versiones de esas dependencias.

## Estructura del repositorio

```text
.
├── Llama_IA.ipynb                              # Flujo RAG actual para Google Colab
├── app.py                                       # Interfaz de consola de la versión inicial
├── rag_pipeline.py                              # Pipeline local inicial con Llama 2 7B
├── plate_checker.py                             # Verificador simplificado de demostración
├── Gaceta_Oficial_DF.pdf
├── Programa_Hoy_No_Circula.pdf
└── REGLAMENTO_DE_TRNSITO_DE_LA_CIUDAD_DE_MEXICO_6.4.pdf
```

## Seguridad y límites

- No subas tokens, archivos `.env`, entornos virtuales ni cachés de modelos.
- La lista de fragmentos recuperados ayuda a revisar el contexto, pero no garantiza por sí sola que la respuesta sea correcta.
- Los documentos normativos pueden quedar desactualizados; el notebook no verifica cambios ni avisos nuevos en Internet.
- Verifica las citas y el texto original, especialmente para preguntas legales o restricciones vigentes.
