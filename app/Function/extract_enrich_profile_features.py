def extract_profile_features(payload) -> dict:
    print(payload)
    if isinstance(payload, list):
        data = payload
    elif isinstance(payload, dict):
        data = payload.get("data", [])
    else:
        data = []

    if not isinstance(data, list):
        data = []

    user_block = {}
    captions = []

    # 🔍 Find user info and captions from mixed blocks
    for item in data:
        if not isinstance(item, dict):
            continue

        if item.get("user") and isinstance(item["user"], dict):
            user_block = item["user"]

        if isinstance(item.get("captions"), list):
            captions.extend(item["captions"])

    # 🧹 Normalize biography safely
    biography = (user_block.get("biography") or "").replace("\n", " ").strip()

    # 🧵 Combine captions into one string safely
    combined_captions = ", ".join(
        caption.replace("\n", " ").strip()
        for caption in captions
        if isinstance(caption, str) and caption.strip()
    )

    return {
        "username": user_block.get("username"),
        "full_name": user_block.get("full_name"),
        "biography": biography,
        "category": user_block.get("category"),
        "followers": user_block.get("follower_count"),
        "following": user_block.get("following_count"),
        "captions": combined_captions
    }
