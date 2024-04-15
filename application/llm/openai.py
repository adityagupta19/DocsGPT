from application.llm.base import BaseLLM
from application.core.settings import settings


class OpenAILLM(BaseLLM):

    def __init__(self, api_key=None, *args, **kwargs):
        global openai
        from openai import OpenAI

        super().__init__(*args, **kwargs)
        self.client = OpenAI(
            api_key=api_key,
        )
        self.api_key = api_key

    def _get_openai(self):
        # Import openai when needed
        import openai

        return openai

    def _raw_gen(
        self,
        baseself,
        model,
        messages,
        stream=False,
        engine=settings.AZURE_DEPLOYMENT_NAME,
        **kwargs
    ):
        response = self.client.chat.completions.create(
            model=model, messages=messages, stream=stream, **kwargs
        )

        return response.choices[0].message.content

    def _raw_gen_stream(
        self,
        baseself,
        model,
        messages,
        stream=True,
        engine=settings.AZURE_DEPLOYMENT_NAME,
        **kwargs
    ):
        response = self.client.chat.completions.create(
            model=model, messages=messages, stream=stream, **kwargs
        )

        for line in response:
            # import sys
            # print(line.choices[0].delta.content, file=sys.stderr)
            if line.choices[0].delta.content is not None:
                yield line.choices[0].delta.content


class AzureOpenAILLM(OpenAILLM):

    def __init__(
        self, openai_api_key, openai_api_base, openai_api_version, deployment_name
    ):
        super().__init__(openai_api_key)
        self.api_base = (settings.OPENAI_API_BASE,)
        self.api_version = (settings.OPENAI_API_VERSION,)
        self.deployment_name = (settings.AZURE_DEPLOYMENT_NAME,)
        from openai import AzureOpenAI

        self.client = AzureOpenAI(
            api_key=openai_api_key,
            api_version=settings.OPENAI_API_VERSION,
            api_base=settings.OPENAI_API_BASE,
            deployment_name=settings.AZURE_DEPLOYMENT_NAME,
        )

    def _get_openai(self):
        openai = super()._get_openai()

        return openai
