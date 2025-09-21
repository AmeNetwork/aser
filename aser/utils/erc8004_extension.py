from a2a.types import (AgentExtension)
#connector 
def create_identity_extension(registrations,trustModels):
    identity_extension = AgentExtension(
        uri="https://eips.ethereum.org/EIPS/eip-8004",
        description="ERC-8004 Registrations",
        params={
            "registrations": registrations,
            "trustModels":trustModels
        }
    )
    return identity_extension


