from datetime import datetime
import time
import requests
from scrapers.common.logger import get_logger

logger = get_logger(__name__)

def get_today() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")

def get_timestamp() -> str:
    return datetime.utcnow().isoformat()

def to_float(value: str) -> float:
    try:
        return float(str(value).replace(",", "").strip())
    except (ValueError, TypeError):
        return None

def to_int(value: str) -> int:
    try:
        return int(str(value).replace(",", "").strip())
    except (ValueError, TypeError):
        return None

def clean_text(value: str) -> str:
    if value is None:
        return None
    return str(value).strip()

def fetch_page(url: str, retries: int = 3, delay: int = 2) -> requests.Response:
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Fetching {url} (attempt {attempt})")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
    logger.error(f"All {retries} attempts failed for {url}")
    return None