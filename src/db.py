"""One validated Supabase backend client for trusted scripts."""
import os
from dotenv import load_dotenv
from supabase import Client,create_client

def get_supabase_client()->Client:
    # WHY: repeated connection code causes inconsistent environment names.
    load_dotenv()
    url=os.getenv('SUPABASE_URL'); key=os.getenv('SUPABASE_SECRET_KEY')
    if not url or not key:
        raise RuntimeError('SUPABASE_URL and SUPABASE_SECRET_KEY are required.')
    # Never print the secret key and never expose this client in browser code.
    return create_client(url,key)
