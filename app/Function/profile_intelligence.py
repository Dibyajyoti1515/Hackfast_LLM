def extract_profile_features(payload: dict) -> dict:
    data = payload.get("data", [])

    user_block = None
    captions = []

    # Find user info and captions from mixed blocks
    for item in data:
        if item.get("user"):
            user_block = item["user"]

        if item.get("captions"):
            captions.extend(item["captions"])

    if not user_block:
        raise ValueError("User data not found in payload")

    # Normalize biography
    biography = user_block.get("biography", "")
    biography = biography.replace("\n", " ").strip()

    # Combine captions into one string
    combined_captions = ", ".join(
        caption.replace("\n", " ").strip()
        for caption in captions
        if caption.strip()
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
