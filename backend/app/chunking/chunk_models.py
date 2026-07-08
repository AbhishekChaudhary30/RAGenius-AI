from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TextChunk:
    chunk_id: int
    text: str
    start_index: int
    end_index: int
    character_count: int
    word_count: int
    metadata: Dict[str, Any]