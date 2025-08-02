def semantic_search(vectorstore, query, k=4):
    return [doc.page_content for doc in vectorstore.similarity_search(query, k=k)]

def build_explainable_prompt(question, clauses):
    context = "\n".join(f"- {clause}" for clause in clauses)
    prompt = (
        f"You are an insurance policy analysis expert. Given the following question:\n"
        f"'{question}'\n"
        f"and these relevant policy clauses:\n{context}\n"
        f"Answer precisely and explain your decision with references to the clauses if possible. "
        f"Output only the answer text, not anything else."
    )
    return prompt

def answer_question(llm, question, clauses):
    prompt = build_explainable_prompt(question, clauses)
    result = llm.invoke(prompt)
    return result.content.strip()
