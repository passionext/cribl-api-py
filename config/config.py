# Cribl API credentials
USER = "<PUT HERE YOUR ID>"
PASSWORD = "<PUR HERE YOUR PASSWORD>"

#Cribl API URL  
API_BASE_URL = "https://${workspaceName}-${organizationId}.cribl.cloud/api/v1"
# For requests that are specific to a certain Worker Group or Fleet, the base URL includes /m and the name of the Worker Group or Fleet:
# https://${workspaceName}-${organizationId}.cribl.cloud/api/v1/m/${groupName}
API_GROUP_URL = "https://${workspaceName}-${organizationId}.cribl.cloud/api/v1/m/${groupName}"
API_AUTH_URL = "https://login.cribl.cloud/oauth/token"