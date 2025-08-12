
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Esto agrega la carpeta raíz 'financeFast' al path

from core.config import settings

print("DATABASE_URL:", settings.DATABASE_URL)
print("SECRET_KEY:", settings.SECRET_KEY)
