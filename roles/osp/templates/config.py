# Set Database Location and Type
# For MySQL Connections add ?charset=utf8mb4 for full Unicode Support
# dbLocation="sqlite:///db/database.db"
dbLocation="mysql+pymysql://osp:{{ database_password }}@localhost/osp?charset=utf8mb4"

# Redis Configuration
redisHost="localhost" # Default localhost
redisPort=6379 # Default 6379
redisPassword='' # Default ''

# Flask Secret Key
secretKey="{{ osp_secret_key }}"

# Password Salt Value
passwordSalt="{{ osp_password_salt }}"

# Allow Users to Register with the OSP Server
allowRegistration=True

# Require Users to Confirm their Email Addresses
requireEmailRegistration=True

# Enables Debug Mode
debugMode = False

# EJabberD Configuration
ejabberdAdmin = "admin"
ejabberdPass = "{{ ejabberd_pass }}"
ejabberdHost = "localhost"

