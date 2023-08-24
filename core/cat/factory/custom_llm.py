from typing import Optional, List, Any, Mapping, Dict
import requests
from langchain.llms.base import LLM
from langchain.llms.openai import OpenAI


class LLMDefault(LLM):
    @property
    def _llm_type(self):
        return ""

    def _call(self, prompt, stop=None):
        return "AI: You did not configure a Language Model. " \
               "Do it in the settings!"


# elaborated from
# https://python.langchain.com/en/latest/modules/models/llms/examples/custom_llm.html
class LLMCustom(LLM):
    # endpoint where custom LLM service accepts requests
    url: str

    # optional key for authentication
    auth_key: str = ""

    # optional dictionary containing custom configuration
    options: Dict = {}

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            # run_manager: Optional[CallbackManagerForLLMRun] = None,
            run_manager: Optional[Any] = None,
    ) -> str:

        request_body = {
            "text": prompt,
            "auth_key": self.auth_key,
            "options": self.options
        }

        try:
            response_json = requests.post(self.url, json=request_body).json()
        except Exception as exc:
            raise ValueError("Custom LLM endpoint error "
                             "during http POST request") from exc

        generated_text = response_json["text"]

        return generated_text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Identifying parameters."""
        return {
            "url": self.url,
            "auth_key": self.auth_key,
            "options": self.options
        }


class CustomOpenAI(OpenAI):
    def __init__(self, url, temperature, max_tokens, stop, top_k, top_p, repeat_penalty):
        model_kwargs = {'repeat_penalty': repeat_penalty}
        if stop:
            model_kwargs['stop'] = stop.split(',')
            print(model_kwargs)

        super().__init__(openai_api_key=" ", 
                         model=url.split("/")[-1], 
                         temperature=temperature,
                         max_tokens=max_tokens,
                         top_k=top_k,
                         top_p=top_p,
                         model_kwargs=model_kwargs
                         )
        self.openai_api_base = url
