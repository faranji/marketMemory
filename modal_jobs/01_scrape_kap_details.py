# Controlled Modal detail scraper: start with five URLs and three workers.
import modal
from config.settings import SCRAPING
app=modal.App('market-memory-kap-details')
image=(modal.Image.debian_slim(python_version='3.12').pip_install('playwright','beautifulsoup4','lxml').run_commands('playwright install --with-deps chromium').workdir('/root/app').env({'PYTHONPATH':'/root/app'}).add_local_dir('src',remote_path='/root/app/src').add_local_dir('config',remote_path='/root/app/config'))
@app.function(image=image,max_containers=SCRAPING.max_workers,timeout=180,retries=2)
def scrape_one_detail(url:str)->dict:
    # TODO: random delay; headless Chromium; HTML/body text; parse source metadata; return dict; no Supabase here.
    raise NotImplementedError
@app.local_entrypoint()
def main(input_csv:str='data/raw/kap/TUPRS/probe_links.csv',limit:int=5,run_name:str='pilot'):
    # TODO: read/dedupe/head(limit); map workers; save HTML and JSONL locally; distinguish TUPRS publisher.
    raise NotImplementedError
