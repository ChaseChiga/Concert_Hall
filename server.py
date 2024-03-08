from app import app

from app.controllers import users
from app.controllers import shows

if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True) 