
import requests


def generate_response(prompt):

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]

    except requests.exceptions.ConnectionError:
        raise Exception(
            "Unable to connect to Ollama. "
            "Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        raise Exception(
            "Ollama request timed out."
        )

    except requests.exceptions.RequestException as error:
        raise Exception(
            f"Ollama API error: {error}"
        )

    except (KeyError, ValueError) as error:
        raise Exception(
            f"Invalid Ollama response: {error}"
        )
