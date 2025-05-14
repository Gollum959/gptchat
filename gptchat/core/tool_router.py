class ToolRouter:
    def __init__(self, agents=None):
        self.tools = {}
        if agents:
            for agent in agents:
                self.add_agent(agent)

    def add_agent(self, agent):
        for func in agent.get_functions():
            if func["name"] in self.tools:
                raise ValueError(f"Function {func['name']} is already registered.")
            self.tools[func["name"]] = (agent, func)

    def get_tool_schemas(self):
        schemas = []
        for _, func in self.tools.values():
            parameters = func.get("parameters", {})
            schema = {
                "type": "function",
                "function": {
                    "name": func["name"],
                    "description": func["description"],
                    "parameters": {
                        "type": "object",
                        "properties": parameters,
                        "required": list(parameters.keys()),
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            }
            schemas.append(schema)
        return schemas

    def dispatch(self, name, arguments):
        if name not in self.tools:
            raise ValueError(f"Function {name} not found")
        agent, _ = self.tools[name]
        return agent.call_function(name, arguments)
