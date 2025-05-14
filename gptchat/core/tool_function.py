def tool_function(name, description, parameters=None):
    def wrapper(func):
        func._tool_meta = {
            "name": name,
            "description": description,
            "parameters": parameters or {},
        }
        return func

    return wrapper
