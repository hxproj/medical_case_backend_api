#mysql connection string
SQLALCHEMY_DATABASE_URI='mysql+mysqldb://root:123456@127.0.0.1:3307/medical_case_of_illness?charset=utf8'

HTTP_HOST = ''
HTTP_PORT = 9000
LOG = 'var/medical_case_of_illness/logs'

QUERY_LIMIT = 10
PER_PAGE = 10
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif','JPG','PNG'])
TEMPLETE_LOCATION ='C:\Users\solitaire\Desktop\illness.docx'

STATIC_FILES_PATH='C:\Medical_Case\\'