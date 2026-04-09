def chunk_pages(pages, size=500):
    chunks = []

    for page in pages:
        text = page["text"]
        title = page["title"]

        for i in range(0, len(text), size):
            chunk = text[i:i+size]

            chunks.append({
                "text": chunk,
                "title": title
            })

    return chunks