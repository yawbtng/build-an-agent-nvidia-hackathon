from langchain_core.runnables.config import RunnableConfig
from scrapybara.client import BrowserInstance, UbuntuInstance, WindowsInstance

from ..types import CUAState
from ..utils import get_configuration_with_defaults, get_scrapybara_client

# Copied from the OpenAI example repository
# https://github.com/openai/openai-cua-sample-app/blob/eb2d58ba77ffd3206d3346d6357093647d29d99c/utils.py#L13
BLOCKED_DOMAINS = [
    "maliciousbook.com",
    "evilvideos.com",
    "darkwebforum.com",
    "shadytok.com",
    "suspiciouspins.com",
    "ilanbigio.com",
]


def create_vm_instance(state: CUAState, config: RunnableConfig):
    instance_id = state.get("instance_id")
    configuration = get_configuration_with_defaults(config)
    scrapybara_api_key = configuration.get("scrapybara_api_key")
    timeout_hours = configuration.get("timeout_hours")
    environment = configuration.get("environment")

    if instance_id is not None:
        # If the instance_id already exists in state, do nothing.
        return {}

    if not scrapybara_api_key:
        raise ValueError(
            "Scrapybara API key not provided. Please provide one in the configurable fields, "
            "or set it as an environment variable (SCRAPYBARA_API_KEY)"
        )

    client = get_scrapybara_client(scrapybara_api_key)

    instance: UbuntuInstance | BrowserInstance | WindowsInstance

    if environment == "ubuntu":
        instance = client.start_ubuntu(timeout_hours=timeout_hours)
    elif environment == "windows":
        instance = client.start_windows(timeout_hours=timeout_hours)
    elif environment == "web":
        blocked_domains = [
            domain.replace("https://", "").replace("www.", "") for domain in BLOCKED_DOMAINS
        ]
        instance = client.start_browser(
            timeout_hours=timeout_hours, blocked_domains=blocked_domains
        )
    else:
        raise ValueError(
            f"Invalid environment. Must be one of 'web', 'ubuntu', or 'windows'. Received: {environment}"
        )

    stream_url = instance.get_stream_url().stream_url

    return {
        "instance_id": instance.id,
        "stream_url": stream_url,
    }
