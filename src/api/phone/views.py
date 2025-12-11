from fastapi import APIRouter, Depends, status, HTTPException
from redis.asyncio import Redis
from src.dependency import get_redis_client
from src.api.phone.schema import (
    AddressResponse,
    PhoneAddressRequest,
    UpdateAddressRequest,
    PhoneNumber,
    Address,
)

router = APIRouter()


def _phone_as_redis_key(phone: PhoneNumber):
    """Generate Redis key for storing phone → address mapping."""
    return f"phone:{phone}"


@router.get(
    "/{phone}",
    status_code=status.HTTP_200_OK,
    response_model=AddressResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"detail": "Not Found"},
    },
    description="""
Retrieve the address associated with a given phone number.

**Behavior:**
- Looks up the phone number in Redis using the key `phone:{phone}`.
- If a record is found, returns HTTP 200 with the address in JSON format.
- If no record exists for the given phone number, returns HTTP 404.

**Use case:**
- Quickly verify or fetch the current address of a client by phone number.
""",
)
async def get_address_by_phone(
    phone: PhoneNumber, redis_client: Redis = Depends(get_redis_client)
):
    if address := await redis_client.get(_phone_as_redis_key(phone)):
        return AddressResponse(address=Address.model_validate_json(address))
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"detail": "Conflict"},
        status.HTTP_201_CREATED: {"detail": "Created"},
    },
    description="""
Create a new phone+address mapping in Redis.

**Behavior:**
- Accepts a JSON payload containing `phone` and `address`.
- Attempts to create a new record in Redis with `NX` flag (only if key does not exist).
- Returns HTTP 201 if successfully created.
- Returns HTTP 409 if the phone number already exists in Redis (no overwrite).

**Use case:**
- Register a new client or record their address for the first time.

Please lookup for the `PhoneAddressRequest` schema for all available model fields.
""",
)
async def create_phone_address(
    body: PhoneAddressRequest, redis_client: Redis = Depends(get_redis_client)
):
    if not await redis_client.set(
        _phone_as_redis_key(body.phone),
        body.address.model_dump_json(),
        nx=True,
    ):
        raise HTTPException(status.HTTP_409_CONFLICT)
    return {"detail": "Created"}


@router.put(
    "/{phone}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"detail": "Not Found"},
        status.HTTP_200_OK: {"detail": "Ok"},
    },
    description="""
Update the address for an existing phone number.

**Behavior:**
- Accepts a JSON payload containing `address`.
- Uses the `XX` flag in Redis to update the record only if it already exists.
- Returns HTTP 200 with `{ "detail": "Ok" }` if the update succeeds.
- Returns HTTP 404 if the phone number does not exist in Redis.

**Use case:**
- Update a client's address after relocation or correction.

Please lookup for the `UpdateAddressRequest` schema for all available model fields.
""",
)
async def update_address(
    phone: PhoneNumber,
    body: UpdateAddressRequest,
    redis_client: Redis = Depends(get_redis_client),
):
    if not await redis_client.set(
        _phone_as_redis_key(phone),
        body.address.model_dump_json(),
        xx=True,
    ):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return {"detail": "Ok"}


@router.delete(
    "/{phone}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}},
    description="""
Delete a phone+address mapping from Redis.

**Behavior:**
- Attempts to delete the record associated with the given phone number.
- Returns HTTP 204 if the record existed and was deleted.
- Returns HTTP 404 if the record was not found.

**Use case:**
- Remove outdated, erroneous, or unnecessary client address records.
""",
)
async def remove_phone_address(
    phone: PhoneNumber,
    redis_client: Redis = Depends(get_redis_client),
):
    if await redis_client.delete(_phone_as_redis_key(phone)) < 1:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
