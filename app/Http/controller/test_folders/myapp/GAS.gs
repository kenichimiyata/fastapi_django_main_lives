function doPost(e) {
  var image = e.postData.contents;
  var driveFolderId = 'folder_id';
  var s3BucketName = 'bucket_name';
  var serviceAccountKey = 'path/to/service_account_key.json';
  
  var drive = getDriveService();
  var driveFile = drive.createFile({
    'image.jpg',
    'mimeType': 'image/jpeg'
  });
  
  var fileContent = driveFile.getBlob().getBytes();
  var s3 = getS3Service();
  s3.putObject({
    'Bucket': s3BucketName,
    'Key': 'image.jpg',
    'Body': fileContent
  });
  
  var fastApiUrl = 'http://localhost:8000/judge';
  var options = {
    'method': 'POST',
    'headers': {
      'Content-Type': 'application/json'
    },
    'payload': JSON.stringify({
      'image_base64': Utilities.base64Encode(fileContent)
  };
  
  UrlFetchApp.fetch(fastApiUrl, options);
}

function getDriveService() {
  var serviceAccountKey = 'path/to/service_account_key.json';
  var serviceAccountAuth = getServiceAccountAuth_(serviceAccountKey);
  var driveService = OAuth2.createService('drive')
    .setAuthorizationBaseUrl('https://accounts.google.com')
    .setTokenUrl('https://accounts.google.com/o/oauth2/token')
    .setClientId(serviceAccountAuth.client_id)
    .setClientSecret(serviceAccountAuth.client_secret)
    .setCallbackFunction('authCallback')
    .setPropertyStore(PropertiesService.getUserProperties());
  
  driveService.setScope('https://www.googleapis.com/auth/drive');
  return driveService;
}

function getS3Service() {
  var serviceAccountKey = 'path/to/service_account_key.json';
  var serviceAccountAuth = getServiceAccountAuth_(serviceAccountKey);
  var s3Service = OAuth2.createService('s3')
    .setAuthorizationBaseUrl('https://s3.amazonaws.com')
    .setTokenUrl('https://s3.amazonaws.com/o/oauth2/token')
    .setClientId(serviceAccountAuth.client_id)
    .setClientSecret(serviceAccountAuth.client_secret)
    .setCallbackFunction('authCallback')
    .setPropertyStore(PropertiesService.getUserProperties());
  
  s3Service.setScope('https://s3.amazonaws.com/auth/s3');
  return s3Service;
}

function getServiceAccountAuth_(serviceAccountKey) {
  var serviceAccountAuth = {};
  serviceAccountAuth.client_id = serviceAccountKey.client_id;
  serviceAccountAuth.client_secret = serviceAccountKey.client_secret;
  return serviceAccountAuth;
}