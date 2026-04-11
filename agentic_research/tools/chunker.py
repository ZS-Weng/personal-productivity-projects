def chunk_text(text, chunk_size, overlap):
    """
    Splits the input text into chunks of specified size with overlap.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk.
        overlap (int): The number of characters to overlap between chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    
    min_chunk = int(chunk_size - overlap)
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        temp_chunk = text[start:end]
        if temp_chunk.rfind("\n\n") != -1 and temp_chunk.rfind("\n\n") >= min_chunk:
            end_adj = temp_chunk.rfind("\n\n")
        elif temp_chunk.rfind("\n") != -1 and temp_chunk.rfind("\n") >= min_chunk:
            end_adj = temp_chunk.rfind("\n")
        elif temp_chunk.rfind(".") != -1 and temp_chunk.rfind(".") >= min_chunk:
            end_adj = temp_chunk.rfind(".")
        else:
            end_adj = len(temp_chunk)

        chunks.append(text[start:start + end_adj])
        start += end_adj - overlap
    
    return chunks

## Code used for testing of chunking behaviour
# text =     """
#     Splits the input text into chunks of specified size with overlap.

#     Args:
#         text (str): The input text to be chunked.
#         chunk_size (int): The maximum size of each chunk.
#         overlap (int): The number of characters to overlap between chunks.

#     Returns:
#         List[str]: A list of text chunks.
#     """

# print(chunk_text(text, 100, 30))