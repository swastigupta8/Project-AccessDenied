"""
SOC analyst report generation.

Previously this was an if/elif tree returning hardcoded string templates
labeled as a "Gemini AI SOC Analyst" in a code comment — no model was
ever called. This version calls the real Anthropic API when
ANTHROPIC_API_KEY is set. If it isn't set (e.g. someone clones the repo
without configuring a key), it falls back to a clearly-labeled
rule-based summary instead of silently pretending to be AI-generated.
"""
import os

_client = None
if os.environ.get("ANTHROPIC_API_KEY"):
    try:
        import anthropic
        _client = anthropic.Anthropic()
    except ImportError:
        _client = None


def _rule_based_fallback(process_status, network_status, hits) -> str:
    if hits > 0 and (process_status == "HIGH" or network_status == "HIGH"):
        return (f"[RULE-BASED FALLBACK — no ANTHROPIC_API_KEY configured] "
                f"Correlated signal: {hits} honeypot hit(s) alongside a {process_status}/"
                f"{network_status} process/network reading. Review immediately.")
    elif hits > 0:
        return (f"[RULE-BASED FALLBACK] Honeypot absorbed {hits} probe(s); "
                f"process/network telemetry currently nominal.")
    elif process_status == "HIGH" or network_status == "HIGH":
        return (f"[RULE-BASED FALLBACK] Elevated telemetry ({process_status}/{network_status}) "
                f"with no perimeter breach recorded.")
    return "[RULE-BASED FALLBACK] All monitored signals within baseline."


def generate_report(process_status: str, network_status: str, hits: int) -> dict:
    if _client is None:
        return {"report": _rule_based_fallback(process_status, network_status, hits), "source": "rule_based"}

    prompt = (
        "You are a SOC analyst summarizing live telemetry for a cyber-physical "
        "monitoring dashboard. Write a 2-3 sentence incident assessment.\n\n"
        f"Process anomaly status: {process_status}\n"
        f"Network anomaly status: {network_status}\n"
        f"Honeypot intrusion hits: {hits}\n\n"
        "Be concise and specific about recommended action."
    )
    try:
        message = _client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in message.content if block.type == "text")
        return {"report": text, "source": "claude-sonnet-4-6"}
    except Exception as e:
        return {"report": _rule_based_fallback(process_status, network_status, hits) +
                 f" (LLM call failed: {e})", "source": "rule_based_error_fallback"}
