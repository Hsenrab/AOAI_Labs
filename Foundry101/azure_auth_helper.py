"""
Azure Authentication Helper

This module provides a comprehensive authentication solution for Azure
with multiple authentication options to work across different environments.

"""

import subprocess
import json
from azure.identity import InteractiveBrowserCredential, DeviceCodeCredential, DefaultAzureCredential


def authenticate_azure(auth_method=None, show_instructions=False):
    """
    Authenticate with Azure using multiple methods.
    
    Args:
        auth_method (str, optional): Specific authentication method to use.
                                   Options: 'cli', 'browser', 'device'
                                   If None, defaults to 'cli'
        show_instructions (bool): Whether to show authentication options instructions
        
    Returns:
        credential: Azure credential object ready for use with Azure AI Foundry
        
    Raises:
        Exception: If authentication fails
    """
    
    # First, try existing credentials
    try:
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")
        print("✅ Using existing Azure credentials")
        return credential
    except:
        # If no existing credentials, continue to specified method
        pass
    
    # Default to CLI if no method specified
    if auth_method is None:
        auth_method = 'cli'
    
    # Use the specified authentication method
    if auth_method.lower() == 'cli':
        return _authenticate_with_cli()
    elif auth_method.lower() == 'browser':
        return _authenticate_with_browser()
    elif auth_method.lower() == 'device':
        return _authenticate_with_device_code()
    else:
        raise ValueError(f"Invalid auth_method: {auth_method}. Use 'cli', 'browser', or 'device'")


def _authenticate_with_cli():
    """Authenticate using Azure CLI"""
    print("🔧 Using Azure CLI authentication...")
    try:
        # Run az login command
        result = subprocess.run(['az', 'login'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully logged into Azure CLI!")
            
            # Show current account
            account_result = subprocess.run(['az', 'account', 'show'], capture_output=True, text=True)
            if account_result.returncode == 0:
                account_info = json.loads(account_result.stdout)
                print(f"📧 Signed in as: {account_info.get('user', {}).get('name', 'Unknown')}")
                print(f"🏢 Subscription: {account_info.get('name', 'Unknown')}")
            
            # Use DefaultAzureCredential which will pick up CLI credentials
            credential = DefaultAzureCredential()
            return credential
        else:
            print("❌ Failed to log into Azure CLI")
            print(f"Error: {result.stderr}")
            raise Exception("Azure CLI login failed")
            
    except FileNotFoundError:
        print("❌ Azure CLI not found!")
        print("📦 Please install Azure CLI first:")
        print("   Windows: https://aka.ms/installazurecliwindows")
        print("   macOS: brew install azure-cli")
        print("   Linux: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli")
        raise


def _authenticate_with_browser():
    """Authenticate using interactive browser"""
    print("🌐 Starting interactive browser authentication...")
    credential = InteractiveBrowserCredential()
    
    # Test the credential
    try:
        credential.get_token("https://management.azure.com/.default")
        print("✅ Authentication successful!")
        return credential
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        raise


def _authenticate_with_device_code():
    """Authenticate using device code"""
    print("📱 Starting device code authentication...")
    print("📝 You'll receive a code to enter on another device")
    credential = DeviceCodeCredential()
    
    # Test the credential
    try:
        credential.get_token("https://management.azure.com/.default")
        print("✅ Authentication successful!")
        return credential
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        raise


def quick_authenticate():
    """
    Quick authentication that tries existing credentials first,
    then falls back to device code if needed.
    
    Returns:
        credential: Azure credential object
    """
    try:
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")
        print("✅ Using existing Azure credentials")
        return credential
    except:
        print("🔄 No existing credentials found. Using device code authentication...")
        return _authenticate_with_device_code()


def authenticate_with_cli():
    """
    Convenience function for Azure CLI authentication.
    
    Returns:
        credential: Azure credential object
    """
    return authenticate_azure('cli', show_instructions=False)


def authenticate_with_browser():
    """
    Convenience function for interactive browser authentication.
    
    Returns:
        credential: Azure credential object
    """
    return authenticate_azure('browser', show_instructions=False)


def authenticate_with_device_code():
    """
    Convenience function for device code authentication.
    
    Returns:
        credential: Azure credential object
    """
    return authenticate_azure('device', show_instructions=False)


if __name__ == "__main__":
    # Test the authentication
    try:
        cred = authenticate_azure()
        print("🎉 Authentication test successful!")
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
