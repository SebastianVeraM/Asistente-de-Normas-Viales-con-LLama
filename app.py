from pathlib import Path

from rag_pipeline import load_documents, create_vectorstore, build_rag
from plate_checker import can_circulate


def main():
    print("🚗 Asistente Normas Viales CDMX")
    docs = load_documents()
    vectorstore = create_vectorstore(docs)
    qa = build_rag(vectorstore)

    while True:
        query = input("Pregunta (o escribe 'placa:ABC1234'): ").strip()
        if query.lower() in ["salir", "exit"]:
            break
        if query.startswith("placa:"):
            plate = query.split(":")[1]
            if can_circulate(plate):
                print(f"✅ El vehículo con placa {plate} puede circular hoy.")
            else:
                print(
                    f"❌ El vehículo con placa {plate} NO puede circular hoy. Se recomienda usar transporte público o privado.")
        else:
            response = qa.invoke({"query": query})
            print("Respuesta:", response["result"])

            sources = set()
            for document in response.get("source_documents", []):
                source_name = Path(document.metadata.get("source", "Documento desconocido")).name
                page = document.metadata.get("page")
                page_label = f"p. {page + 1}" if isinstance(page, int) else "página no disponible"
                sources.add((source_name, page_label))

            if sources:
                print("Fuentes consultadas:")
                for source_name, page_label in sorted(sources):
                    print(f"- {source_name}, {page_label}")
            else:
                print("No se recuperaron fuentes para esta respuesta.")


if __name__ == "__main__":
    main()
