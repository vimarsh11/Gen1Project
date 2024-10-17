from setuptools import find_packages, setup

setup(
    name='gen1project',
    version='0.0.1',
    author='vimarsh jaiswal',
    author_email='jaiswaldesh16@gmail.com',
    description='A generative AI project using OpenAI, LangChain, and Streamlit',
    install_requires=[
        "openai",
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages(),
    license='MIT'
)
