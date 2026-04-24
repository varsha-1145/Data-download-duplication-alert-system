import hashlib

def compute_file_hash_from_filename(filename: str) -> str:
    """Simulate computing SHA256 hash based on filename (mock)."""
    return hashlib.sha256(filename.encode()).hexdigest()
