import os


working_dir = 'C:/Users/John/OneDrive/src/dustball/local'
cred_fpath = f'{working_dir}/valiant-broker-355912-67d74ed7957a.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_fpath
