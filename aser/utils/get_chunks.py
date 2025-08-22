import semchunk
def get_chunks(text,chunk_size):
    chunker= semchunk.chunkerify('gpt-4', chunk_size)
    chunks = chunker(text)
    return chunks