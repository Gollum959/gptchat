from orchestrator import GPTOrchestrator
from core.tool_router import ToolRouter
from agents.database_service import DatabaseService
from agents.currency_service import CurrencyService

if __name__ == "__main__":
    router = ToolRouter()
    router.add_agent(DatabaseService())
    router.add_agent(CurrencyService())

    orchestrator = GPTOrchestrator(router)

    while True:
        user_input = input("Ваш запрос: ")
        if user_input.lower() in {"exit", "выход"}:
            break
        response = orchestrator.handle_user_request(user_input)
        print("Ответ:", response)
