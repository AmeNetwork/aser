
from typing import Any
from uuid import uuid4
import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    MessageSendParams,
    SendMessageRequest
)


base_url = 'http://localhost:9999'


async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,

        )
        agent_card = await resolver.get_agent_card()

        client = A2AClient(
            httpx_client=httpx_client, agent_card=agent_card
        )
        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': 'get bitcoin price'}
                ],
                'messageId': uuid4().hex,
            },
        }
        request = SendMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )
        response = await client.send_message(request)
        print(response.model_dump(mode='json', exclude_none=True))

if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
