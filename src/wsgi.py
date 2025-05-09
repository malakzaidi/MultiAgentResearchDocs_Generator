import os
from app import app

# Set working directory to project root
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    app.run()