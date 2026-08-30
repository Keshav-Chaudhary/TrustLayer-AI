import chromadb
import re

client = chromadb.PersistentClient(path='data/vector_store')
collection = client.get_collection('hotel_knowledge')

results = collection.get()

ids_to_update = []
metadatas_to_update = []

for idx, doc_id in enumerate(results['ids']):
    meta = results['metadatas'][idx]
    doc = results['documents'][idx]
    
    # Try to extract hotel name from doc
    match = re.search(r"Hotel Profile:\s*(.*?)\s*(?:located in|.)", doc)
    if match:
        name = match.group(1).strip()
        if "located in" in name:
            name = name.split("located in")[0].strip()
        if "." in name:
            name = name.split(".")[0].strip()
            
        meta['hotel_name'] = name
        ids_to_update.append(doc_id)
        metadatas_to_update.append(meta)
    else:
        # Some chunks might not have Hotel Profile. If so, just skip or use ID
        pass

if ids_to_update:
    # Batch update
    batch_size = 500
    for i in range(0, len(ids_to_update), batch_size):
        batch_ids = ids_to_update[i:i+batch_size]
        batch_metas = metadatas_to_update[i:i+batch_size]
        collection.update(ids=batch_ids, metadatas=batch_metas)
        print(f"Updated {len(batch_ids)} records.")
else:
    print("No records matched.")

print("Done.")
