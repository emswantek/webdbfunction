// Version 1.0.0 retrofit
param sites_eswebfunctions01_name string = 'eswebfunctions01'
param components_eswebfunctions01_name string = 'eswebfunctions01'
param serverfarms_ASP_escloudresfunctions_942c_name string = 'ASP-escloudresfunctions-942c'
param storageAccounts_escloudresfunctions84dc_name string = 'escloudresfunctions84dc'
param workspaces_EUS_externalid string = '/subscriptions/181a8156-13e8-499c-a532-7568c0ba7656/resourceGroups/DefaultResourceGroup-EUS/providers/Microsoft.OperationalInsights/workspaces/DefaultWorkspace-181a8156-13e8-499c-a532-7568c0ba7656-EUS'


resource components_eswebfunctions01_name_resource 'microsoft.insights/components@2020-02-02' = {
  name: components_eswebfunctions01_name
  location: 'eastus'
  kind: 'web'
  properties: {
    Application_Type: 'web'
    Flow_Type: 'Redfield'
    Request_Source: 'IbizaWebAppExtensionCreate'
    RetentionInDays: 90
    WorkspaceResourceId: workspaces_EUS_externalid
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

resource storageAccounts_escloudresfunctions84dc_name_resource 'Microsoft.Storage/storageAccounts@2025-01-01' = {
  name: storageAccounts_escloudresfunctions84dc_name
  location: 'eastus'
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'Storage'
  properties: {
    defaultToOAuthAuthentication: true
    allowCrossTenantReplication: false
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    networkAcls: {
      bypass: 'AzureServices'
      virtualNetworkRules: []
      ipRules: []
      defaultAction: 'Allow'
    }
    supportsHttpsTrafficOnly: true
    encryption: {
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
  }
}

resource serverfarms_ASP_escloudresfunctions_942c_name_resource 'Microsoft.Web/serverfarms@2024-11-01' = {
  name: serverfarms_ASP_escloudresfunctions_942c_name
  location: 'East US'
  tags: {
    Environment: 'Prod'
    project: 'CloudResumeChallenge'
  }
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
    size: 'Y1'
    family: 'Y'
    capacity: 0
  }
  kind: 'functionapp'
  properties: {
    perSiteScaling: false
    elasticScaleEnabled: false
    maximumElasticWorkerCount: 0
    isSpot: false
    reserved: true
    isXenon: false
    hyperV: false
    targetWorkerCount: 0
    targetWorkerSizeId: 0
    zoneRedundant: false
    asyncScalingEnabled: false
  }
}

resource sites_eswebfunctions01_name_resource 'Microsoft.Web/sites@2024-11-01' = {
  name: sites_eswebfunctions01_name
  location: 'East US'
  tags: {
    'hidden-link: /app-insights-resource-id': '/subscriptions/181a8156-13e8-499c-a532-7568c0ba7656/resourceGroups/es_cloud_res_functions/providers/microsoft.insights/components/eswebfunctions01'
    'hidden-link: /app-insights-instrumentation-key': 'a780d0ba-886a-4b7d-b180-00c2dbb418f5'
    'hidden-link: /app-insights-conn-string': 'InstrumentationKey=a780d0ba-886a-4b7d-b180-00c2dbb418f5;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/;ApplicationId=2bab7df6-9565-4a3e-ae17-cc1c9d9f571c'
    Environment: 'Prod'
    project: 'CloudResumeChallenge'
  }
  kind: 'functionapp,linux'
  properties: {
    enabled: true
    serverFarmId: serverfarms_ASP_escloudresfunctions_942c_name_resource.id
    reserved: true
    siteConfig: {
      numberOfWorkers: 1
      linuxFxVersion: 'PYTHON|3.11'
      acrUseManagedIdentityCreds: false
      alwaysOn: false
      http20Enabled: false
      functionAppScaleLimit: 200
      minimumElasticInstanceCount: 1
    }
    scmSiteAlsoStopped: false
    clientAffinityEnabled: false
    clientAffinityProxyEnabled: false
    clientCertEnabled: false
    clientCertMode: 'Required'
    hostNamesDisabled: false
    ipMode: 'IPv4'
    httpsOnly: true
    endToEndEncryptionEnabled: false
    redundancyMode: 'None'
    publicNetworkAccess: 'Enabled'
    storageAccountRequired: false
    keyVaultReferenceIdentity: 'SystemAssigned'
    sshEnabled: true
  }
}

resource sites_eswebfunctions01_name_ftp 'Microsoft.Web/sites/basicPublishingCredentialsPolicies@2024-11-01' = {
  parent: sites_eswebfunctions01_name_resource
  name: 'ftp'
  properties: {
    allow: false
  }
}

resource sites_eswebfunctions01_name_scm 'Microsoft.Web/sites/basicPublishingCredentialsPolicies@2024-11-01' = {
  parent: sites_eswebfunctions01_name_resource
  name: 'scm'
  properties: {
    allow: true
  }
}

resource sites_eswebfunctions01_name_web 'Microsoft.Web/sites/config@2024-11-01' = {
  parent: sites_eswebfunctions01_name_resource
  name: 'web'
  properties: {
    numberOfWorkers: 1
    defaultDocuments: [
      'Default.htm'
      'Default.html'
      'Default.asp'
      'index.htm'
      'index.html'
      'iisstart.htm'
      'default.aspx'
      'index.php'
    ]
    netFrameworkVersion: 'v4.0'
    linuxFxVersion: 'PYTHON|3.11'
    requestTracingEnabled: false
    remoteDebuggingEnabled: false
    httpLoggingEnabled: false
    acrUseManagedIdentityCreds: false
    logsDirectorySizeLimit: 35
    detailedErrorLoggingEnabled: false
    publishingUsername: '$eswebfunctions01'
    scmType: 'None'
    use32BitWorkerProcess: false
    webSocketsEnabled: false
    alwaysOn: false
    managedPipelineMode: 'Integrated'
    virtualApplications: [
      {
        virtualPath: '/'
        physicalPath: 'site\\wwwroot'
        preloadEnabled: false
      }
    ]
    loadBalancing: 'LeastRequests'
    experiments: {
      rampUpRules: []
    }
    autoHealEnabled: false
    vnetRouteAllEnabled: false
    vnetPrivatePortsCount: 0
    publicNetworkAccess: 'Enabled'
    cors: {
      allowedOrigins: [
        'https://portal.azure.com'
        'https://eric.swantek.me'
        'http://localhost:63342'
      ]
      supportCredentials: false
    }
    localMySqlEnabled: false
    ipSecurityRestrictions: [
      {
        ipAddress: 'Any'
        action: 'Allow'
        priority: 2147483647
        name: 'Allow all'
        description: 'Allow all access'
      }
    ]
    scmIpSecurityRestrictions: [
      {
        ipAddress: 'Any'
        action: 'Allow'
        priority: 2147483647
        name: 'Allow all'
        description: 'Allow all access'
      }
    ]
    scmIpSecurityRestrictionsUseMain: false
    http20Enabled: false
    minTlsVersion: '1.2'
    scmMinTlsVersion: '1.2'
    ftpsState: 'FtpsOnly'
    preWarmedInstanceCount: 0
    functionAppScaleLimit: 200
    functionsRuntimeScaleMonitoringEnabled: false
    minimumElasticInstanceCount: 1
    azureStorageAccounts: {}
    http20ProxyFlag: 0
  }
}

resource sites_eswebfunctions01_name_sites_eswebfunctions01_name_azurewebsites_net 'Microsoft.Web/sites/hostNameBindings@2024-11-01' = {
  parent: sites_eswebfunctions01_name_resource
  name: '${sites_eswebfunctions01_name}.azurewebsites.net'
  properties: {
    siteName: 'eswebfunctions01'
    hostNameType: 'Verified'
  }
}


