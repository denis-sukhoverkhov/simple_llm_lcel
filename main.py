import os
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
import logging
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn


if __name__ == "__main__":
    if os.environ["DEBUG"] == "true":
        logging.basicConfig(level=logging.DEBUG)

    model = ChatOpenAI(model="gpt-3.5-turbo")

    system_template = "Translate the following into {language}:"
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )

    parser = StrOutputParser()

    chain = prompt_template | model | parser

    # 4. App definition
    app = FastAPI(
        title="LangChain Server",
        version="1.0",
        description="A simple API server using LangChain's Runnable interfaces",
    )

    # 5. Adding chain route

    add_routes(
        app,
        chain,
        path="/chain",
    )

    uvicorn.run(app, host="localhost", port=8000)
