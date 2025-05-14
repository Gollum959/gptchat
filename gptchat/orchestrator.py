import json
import openai

from core.tool_router import ToolRouter


class GPTOrchestrator:
    def __init__(self, router: ToolRouter):
        self.router = router
        self.messages = [
            {
                "role": "system",
                "content": "You are an assistant that uses external tools to help users.",
            }
        ]

    def handle_user_request(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=self.messages,
            tools=self.router.get_tool_schemas(),
            tool_choice="auto",
        )

        tool_call = response.choices[0].message.tool_calls[0]

        print(f"{tool_call = }")

        if tool_call:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"GPT selected function: {name} with arguments: {arguments}")

            result = self.router.dispatch(name, arguments)

            print(f"Result selected function: {result}")

            self.messages.append(
                {"role": "function", "name": name, "content": str(result)}
            )

            response = openai.chat.completions.create(
                model="gpt-4", messages=self.messages
            )

        assistant_reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
