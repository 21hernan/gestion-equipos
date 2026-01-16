import os
from supabase import create_client

# Reemplaza con tus valores reales
SUPABASE_URL = "https://dejsrxnqpgespknupkid.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlanNyeG5xcGdlc3BrbnVwa2lkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQ0NjQsImV4cCI6MjA4MTA4MDQ2NH0.miCWSNoVy17oyYm6VjFbIPVCCgqunGxw6ne4f5m5_Uc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    response = supabase.table('equipos').select('*').execute()
    print("✅ Conexión exitosa!")
    print("Datos:", response.data)
except Exception as e:
    print("❌ Error al conectar:", e)
