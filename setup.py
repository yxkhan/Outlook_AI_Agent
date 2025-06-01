from setuptools import find_packages,setup

setup(name="outlook_ai_agent",
       version="0.0.1",
       author="Yaseen",
       author_email="yaseen.khan@infosys.com",
       packages=find_packages(),
       install_requires=['langchain_openai','langchain','langgraph','fastapi','uvicorn']
       )