from rag_pipeline import load_documents, create_vectorstore, build_rag
from plate_checker import can_circulate


def main():
    print("🚗 Asistente Normas Viales CDMX")
    docs = load_documents()
    vectorstore = create_vectorstore(docs)
    qa = build_rag(vectorstore)

    while True:
        query = input("Pregunta (o escribe 'placa:ABC1234'): ")
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
            answer = qa.run(query)
            print("Respuesta:", answer)


if __name__ == "__main__":
    main()
