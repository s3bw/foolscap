from foolscap.meta_data.io import load_meta


def load_tags():
    stored_data = load_meta()

    tags = [meta['tags'] for _, meta in stored_data.items()]
    return set([tag for sublist in tags for tag in sublist])
