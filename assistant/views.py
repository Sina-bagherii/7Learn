import os

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from openai import OpenAI, OpenAIError

from .forms import QuestionForm


DEFAULT_MODEL = getattr(settings, "CHATGPT_MODEL", "gpt-4o-mini")


def _call_chatgpt(question: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    """Send the question to OpenAI and return the response text."""

    client = OpenAI(api_key=api_key)
    response = client.responses.create(model=model, input=question)
    # `output_text` produces a string representation of the entire response.
    return response.output_text.strip()


@require_http_methods(["GET", "POST"])
def ask(request):
    form = QuestionForm(request.POST or None)
    answer = None
    error = None

    if request.method == "POST" and form.is_valid():
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            error = "OpenAI API key is not configured. Set the OPENAI_API_KEY environment variable."
        else:
            try:
                answer = _call_chatgpt(form.cleaned_data["question"], api_key)
            except OpenAIError as exc:
                error = f"ChatGPT request failed: {exc}"

        if error:
            messages.error(request, error)
        elif answer:
            messages.success(request, "ChatGPT responded successfully!")

    return render(request, "assistant/ask.html", {"form": form, "answer": answer, "error": error})
