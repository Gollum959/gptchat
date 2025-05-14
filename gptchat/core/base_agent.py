from abc import ABC


class BaseToolAgent(ABC):
    def __init__(self):
        self._function_map = {
            fn._tool_meta["name"]: (fn, fn._tool_meta)
            for name in dir(self)
            if (fn := getattr(self, name)) and hasattr(fn, "_tool_meta")
        }

    def get_functions(self):
        return [meta for _, meta in self._function_map.values()]

    def call_function(self, name: str, arguments: dict):
        if name not in self._function_map:
            return {
                "error": f"Function '{name}' not found in {self.__class__.__name__}"
            }
        fn, _ = self._function_map[name]
        return fn(**arguments)
