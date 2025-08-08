from pyairtable.orm import Model
from pyairtable.orm import fields

class Usuario(Model):
    clave = fields.TextField("clave")
    contra = fields.TextField("contra")
    nombre = fields.TextField("nombre")
    admin = fields.CheckboxField("admin")
    class Meta:
        api_key = "pat1qI8evTAXfxa3U.1c2fdf784789a7f37d15513ff0dcdc1b263c8455b9ce0a83e1c1ef5693574187"
        base_id = "appDnz0VMK3bUN7rW"
        table_name = "usuario"
