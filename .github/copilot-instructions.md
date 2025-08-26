# Copilot Agent Instructions for AOAI_Labs Repository

## Repository Overview

**AOAI_Labs** is an educational repository containing hands-on labs and tutorials for Azure OpenAI (AOAI) and related Azure AI services. This repository is designed as a comprehensive learning resource for understanding Azure AI services integration, RAG (Retrieval-Augmented Generation) patterns, and AI search capabilities.

**Repository Size**: ~46 Jupyter notebooks across 6 main lab directories
**Project Type**: Educational/Tutorial repository  
**Languages**: Python, Jupyter Notebooks
**Target Runtime**: Python 3.8+, Azure Machine Learning, VS Code
**Key Dependencies**: Azure SDK for Python, OpenAI Python SDK, azure-search-documents==11.5.1

### Educational Focus
This is a **learning-focused educational project**. Prioritize simplicity and clarity over production-ready code. No complex error handling, backwards compatibility, or production optimizations are needed. Notebooks are designed to be executed sequentially (top-to-bottom) as learning exercises.

### Authentication Evolution
The repository is transitioning from API key-based authentication to modern login-based credentials as demonstrated in the Foundry101 notebooks. Newer labs use Azure authentication with `azure_auth_helper.py` while legacy labs still use API keys in `.env` files.

## Architecture & Project Layout

### Main Lab Directories

1. **`AzureAIRAGLab/`** - Azure OpenAI RAG fundamentals
   - `00_Setup.ipynb` - Environment setup and resource configuration
   - `01_AOAI_handson.ipynb` - Basic Azure OpenAI API usage
   - `02_ChatCompletion_api.ipynb` - Chat completion patterns
   - `03_Tokens_and_usage.ipynb` - Token management and usage optimization
   - `04_Chunking.ipynb` - Document chunking strategies
   - `05_AI_doc_intelligence_doc_processing - Layout.ipynb` - Document Intelligence integration
   - `08_AzureSearchSimple.ipynb` - Basic Azure AI Search
   - `09_AzureSearch.ipynb` - Advanced RAG with Azure AI Search

2. **`AzureAISearchLab/`** - Advanced Azure AI Search scenarios
   - `00_Setup.ipynb` - Setup and prerequisites
   - `01_AI_doc_intelligence_doc_processing - Layout.ipynb` - Document processing
   - `02_Chunking.ipynb` - Content chunking
   - `03_AzureSearchSimple.ipynb` - Basic search implementation
   - `04_AzureSearchDataSource.ipynb` - Data source configuration
   - `05_AzureSearchSkillSet.ipynb` - Cognitive skills integration
   - `06_AzureSearchCustomSkill.ipynb` - Custom skills with Azure Functions
   - `07_AzureSearchEmbeddings.ipynb` - Vector search and embeddings

3. **`Foundry101/`** - Azure AI Foundry labs
   - `azure_auth_helper.py` - Authentication utilities for Foundry
   - Foundry-specific notebooks for modern Azure AI platform

4. **`ContentSafety/`** - Azure AI Content Safety integration

5. **`Other/`** - Shared utilities and templates
   - `requirements.txt` - Legacy file (outdated, not used)
   - `credentials_template.env` - Environment variable template

### Configuration Files

**Environment Configuration** - Each major lab directory has its own `.env` file:
- `AzureAIRAGLab/.env` - RAG lab specific configuration
- `AzureAISearchLab/.env` - Search lab specific configuration  
- `Foundry101/.env` - Azure AI Foundry specific configuration
- Root `.env` - Global configuration (also exists)

**Typical .env structure** (Legacy labs):
```
OPENAI_API_KEY="..." 
OPENAI_API_ENDPOINT="https://openai-universal.openai.azure.com/"
AZURE_AI_KEY="..."
AI_SEARCH_KEY="..."
AI_SEARCH_ENDPOINT="https://small-search-3.search.windows.net"
BLOB_STORAGE_ACCOUNT_CONNECTION_STRING="..."
```

**Modern Authentication** (Foundry labs):
- Uses `azure_auth_helper.py` for interactive login-based authentication
- Supports multiple auth methods: device code, browser, CLI
- Still uses .env files for endpoints and configuration, but no API keys stored

**Dependency Management**:
- Notebooks install their own dependencies using `%pip install` cells
- No centralized requirements.txt file is used
- Each notebook specifies only the packages it needs

### Azure Functions Projects
- `AzureAISearchLab/genai-extract-from-pdf/` - Custom skill for PDF extraction
- `AzureAISearchLab/mapping-example/` - Custom mapping example

## Development Guidelines

### Notebook Execution Pattern
1. **Always start with `00_Setup.ipynb`** in each lab directory
2. **Execute notebooks sequentially** (00 → 01 → 02...)
3. **Run cells top-to-bottom** within each notebook
4. **Environment variables must be configured** before running any notebooks

### Common Setup Steps
```python
# Standard imports in most notebooks
%pip install python-dotenv
%pip install azure-search-documents==11.5.1
%pip install azure-identity

from dotenv import load_dotenv
import os
load_dotenv()

# Environment variable loading pattern
AI_SEARCH_ENDPOINT = os.getenv('AI_SEARCH_ENDPOINT')
AI_SEARCH_KEY = os.getenv('AI_SEARCH_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_ENDPOINT = os.getenv('OPENAI_API_ENDPOINT')
```

### Dependency Installation Pattern
Each notebook includes `%pip install` cells for its specific requirements:
- Always install packages at the beginning of notebooks
- Use specific versions where compatibility is important (e.g., `azure-search-documents==11.5.1`)
- Common packages: `python-dotenv`, `azure-identity`, `openai`, `azure-search-documents`

### Azure Resource Requirements
Most labs require these Azure resources:
- **Azure OpenAI Service** (GPT-4, GPT-3.5-turbo, text-embedding-ada-002)
- **Azure AI Search** (Basic tier or higher, semantic ranking enabled)
- **Azure Storage Account** (for blob storage and data sources)
- **Azure AI Services** (multiservice account for cognitive skills)
- **Azure AI Document Intelligence** (for document processing)

### Common Code Patterns

**Azure Search Client Setup**:
```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

AZURE_SEARCH_CREDENTIAL = AzureKeyCredential(AI_SEARCH_KEY)
index_client = SearchIndexClient(endpoint=AI_SEARCH_ENDPOINT, credential=AZURE_SEARCH_CREDENTIAL)
```

**OpenAI Client Setup** (Legacy with API keys):
```python
from openai import AzureOpenAI

openai_client = AzureOpenAI(
    api_version="2024-06-01",
    azure_endpoint=OPENAI_API_ENDPOINT,
    api_key=OPENAI_API_KEY
)
```

**Modern Authentication Setup** (Foundry approach):
```python
from azure_auth_helper import authenticate_azure

# Interactive authentication
credential = authenticate_azure()

# Use with Azure AI services
from azure.ai.projects import AIProjectClient
project_client = AIProjectClient.from_connection_string(
    conn_str=project_connection_string,
    credential=credential
)
```

## Validation Steps

### Environment Validation
1. **Check .env file exists** with all required variables
2. **Check packages used** by checking all libraries used are installed within the notebook (with versions)

### Notebook Validation
1. **Run setup cells first** (pip installs, imports, environment loading)
2. **Run rest of the cells** when connecting to Azure services


## Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `fatal: detected dubious ownership in repository` | Use `git config --global --add safe.directory <path>` |
| `Kernel reset` or invalid kernel | Close/reopen file, refresh and choose kernel again |
| Authentication failures | Verify all environment variables in `.env` file |
| Search index errors | Ensure Azure AI Search service has proper tier and settings |
| Missing modules | Run `%pip install` commands in notebook cells |

### File Dependencies
- **Notebooks depend on lab-specific `.env`** configuration in their respective directories
- **Azure Functions** in `AzureAISearchLab/` use separate `local.settings.json`
- **SourceDocument.py** utility class used across multiple labs
- **Foundry auth helper** in `Foundry101/azure_auth_helper.py` for authentication

## Agent Instructions

1. **Trust these instructions** - only search for additional context if information is incomplete or incorrect
2. **Follow sequential execution** - respect the numbered notebook order
3. **Prioritize simplicity** - this is educational code, avoid overengineering
4. **Keep changes minimal and focused** - limit changes to the minimum lines of code and files needed for the requested task. If you see potential improvements, suggest them to the user rather than implementing them automatically
5. **Use provided patterns** - follow established code patterns for consistency
6. **Test incrementally** - validate each notebook cell before proceeding
7. **Focus on learning outcomes** - explanations should be clear and educational

When working with this repository, start with understanding the specific lab context, ensure proper environment setup, and follow the established patterns for Azure service integration.