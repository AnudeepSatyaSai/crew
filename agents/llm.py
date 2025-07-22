# agents/llm.py
import json
import google.generativeai as genai

genai.configure(api_key="AIzaSyAbk0Z3zh2a1aXnQXlbzJ94SEpul7vD_Gg")
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

class LLMAgent:
    def __init__(self, context):
        self.context = context

    def summarize(self):
        # Compose a summary using all agent outputs, including macro and frequency agents
        summary = []
        if 'macro' in self.context:
            macro = self.context['macro']
            if 'macro_news_actionable' in macro:
                actionable = macro['macro_news_actionable']
                if actionable:
                    summary.append("Key macro news signals:")
                    for item in actionable[:5]:
                        summary.append(f"- {item['headline']} (Sentiment: {item['sentiment']}, Event: {item['event_type']}, Relevance: {item['relevance']})")
        if 'medium_frequency' in self.context:
            mf = self.context['medium_frequency']
            if 'scalping_signal' in mf:
                summary.append(f"Medium-frequency (scalping/intraday) signal: {mf['scalping_signal']} (ML pred: {mf.get('ml_predicted_return')})")
        if 'high_frequency' in self.context:
            hf = self.context['high_frequency']
            if 'hft_signal' in hf:
                summary.append(f"High-frequency (HFT) signal: {hf['hft_signal']} (ML pred: {hf.get('ml_predicted_return')})")
        # Add other agent summaries as before
        for k, v in self.context.items():
            if k in ['macro', 'medium_frequency', 'high_frequency', 'llm_summary', 'llm_factors', 'timestamp']:
                continue
            if isinstance(v, dict) and 'error' not in v:
                summary.append(f"{k.capitalize()} analysis: {str(v)[:200]}")
        return "\n".join(summary)

    def generate_factors(self):
        # Generate actionable factors from macro and frequency agent outputs
        factors = []
        macro = self.context.get('macro', {})
        if 'macro_news_actionable' in macro:
            for item in macro['macro_news_actionable'][:3]:
                if item['event_type']:
                    factors.append(f"Macro event: {item['event_type']} (Sentiment: {item['sentiment']})")
        mf = self.context.get('medium_frequency', {})
        if mf.get('scalping_signal'):
            factors.append(f"Scalping signal: {mf['scalping_signal']} (ML pred: {mf.get('ml_predicted_return')})")
        hf = self.context.get('high_frequency', {})
        if hf.get('hft_signal'):
            factors.append(f"HFT signal: {hf['hft_signal']} (ML pred: {hf.get('ml_predicted_return')})")
        return "\n".join(factors)
