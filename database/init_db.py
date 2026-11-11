from database.connection import engine
from database.models import Base


print("Creando tablas...")

Base.metadata.create_all(engine)

print("Tablas creadas correctamente.")