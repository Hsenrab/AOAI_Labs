"""
Azure Authentication Helper

This module provides a comprehensive authentication solution for Azure
with multiple authentication options to work across different environments.

"""

import json
from azure.identity import InteractiveBrowserCredential, DeviceCodeCredential, DefaultAzureCredential


def authenticate_azure(auth_method=None, tenant_id=None, force=False):
    """
    Authenticate with Azure using multiple methods.
    
    Args:
        auth_method (str, optional): Specific authentication method to use.
                                   Options: 'browser', 'device'
                                   If None, defaults to 'browser'
        tenant_id (str, optional): Azure tenant ID to authenticate against.
                                 Required for both browser and device authentication.
        force (bool): Whether to force re-authentication
        
    Returns:
        credential: Azure credential object ready for use with Azure AI Foundry
        
    Raises:
        Exception: If authentication fails
    """
    
    # Set default auth method
    if auth_method is None:
        auth_method = 'browser'
    
    # Validate tenant_id is provided
    if tenant_id is None:
        raise ValueError("tenant_id is required. Please provide your Azure tenant ID.")
    
    # First, try existing credentials (skip if forcing re-authentication)
    if not force:
        try:
            credential = DefaultAzureCredential()
            credential.get_token("https://management.azure.com/.default")
            print("✅ Using existing Azure credentials")
            return credential
        except Exception as e:
            print(f"ℹ️ No existing credentials found, will authenticate...")
    
    # Use the specified authentication method
    if auth_method.lower() == 'browser':
        return _authenticate_with_browser(tenant_id)
    elif auth_method.lower() == 'device':
        return _authenticate_with_device_code(tenant_id)
    else:
        raise ValueError(f"Invalid auth_method: {auth_method}. Use 'browser' or 'device'")


def _authenticate_with_browser(tenant_id):
    """Authenticate using interactive browser"""
    print("🌐 Starting interactive browser authentication...")
    print(f"🏢 Authenticating with tenant: {tenant_id}")
    credential = InteractiveBrowserCredential(tenant_id=tenant_id)
    
    # Test the credential
    try:
        credential.get_token("https://management.azure.com/.default")
        print("✅ Authentication successful!")
        return credential
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        raise


def _authenticate_with_device_code(tenant_id):
    """Authenticate using device code"""
    print("📱 Starting device code authentication...")
    print(f"🏢 Authenticating with tenant: {tenant_id}")
    print("📝 You'll receive a code to enter on another device")
    credential = DeviceCodeCredential(tenant_id=tenant_id)
    
    # Test the credential
    try:
        credential.get_token("https://management.azure.com/.default")
        print("✅ Authentication successful!")
        return credential
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        raise