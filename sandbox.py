def search_to_url(search):
    search_spliced = search.split()
    length_search_splice = len(search_spliced)
    raw_url_bridge_beg = ""

    for i, word in enumerate(search_spliced):
        print(i, word)
        if i != (length_search_splice - 1):
            raw_url_bridge_beg += word.lower() + "+"
        else:
            raw_url_bridge_beg += word.lower()

    print(raw_url_bridge_beg)

    raw_url_start = f"https://whiskyauctioneer.com/auction-search?text="
    raw_url_bridge_final = raw_url_bridge_beg
    raw_url_end = "&sort=field_reference_field_end_date+DESC&items_per_page=500"

    final_url = raw_url_start + raw_url_bridge_final + raw_url_end
    return final_url
