def echo_content(**params):
    content = params.get("content")
    name = params.get("name")

    return "{}, {}".format(content, name)
