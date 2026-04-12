from logger import logger

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        
        # Modern LangChain uses .invoke() with "input" key
        result = chain.invoke({"input": user_input})
        
        # Extract response based on your chain's output structure
        response = {
            "response": result.get("answer", result.get("result", "No answer generated")),
            "sources": []
        }
        
        # Handle source documents (they might be in "context" or "source_documents")
        if "context" in result:
            for doc in result["context"]:
                source = doc.metadata.get("source", doc.metadata.get("sources", "Unknown"))
                response["sources"].append(source)
        elif "source_documents" in result:
            for doc in result["source_documents"]:
                source = doc.metadata.get("source", doc.metadata.get("sources", "Unknown"))
                response["sources"].append(source)
        
        logger.debug(f"Chain response: {response}")
        return response
        
    except Exception as e:
        logger.exception("Error on query chain")
        raise