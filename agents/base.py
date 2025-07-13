import traceback

class BaseAgent:
    name = "base"

    def __init__(self, ticker):
        self.ticker = ticker

    async def safe_analyze(self, coro):
        try:
            return await coro()
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
            }
