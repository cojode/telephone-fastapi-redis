from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class PhoneModel(BaseModel):
    phone: PhoneNumber = Field(
        ...,
        description="Phone number",
        examples=["+79161234567", "+74951234567", "+442071234567"],
    )


class Address(BaseModel):
    region: str = Field(
        ...,
        description="Region / province / state-level unit",
        examples=["Московская область", "Калифорния", "Île-de-France"],
    )
    district: str | None = Field(
        None,
        description="District within the region (optional)",
        examples=["Пушкинский район", "Santa Clara County", "Paris"],
        json_schema_extra={"optional": True},
    )
    city: str = Field(
        ...,
        description="City / populated locality",
        examples=["Москва", "Сан-Франциско", "Париж"],
    )
    settlement: str | None = Field(
        None,
        description="Village, settlement, or microdistrict (optional)",
        examples=["село Иваново", "Sunnyvale", "La Défense"],
        json_schema_extra={"optional": True},
    )
    street: str = Field(
        ...,
        description="Street",
        examples=["ул. Пушкина", "Main Street", "Avenue des Champs-Élysées"],
    )
    house: str = Field(
        ..., description="House number", examples=["д. 10", "123", "№ 25"]
    )
    building: str | None = Field(
        None,
        description="Building (optional)",
        examples=["корп. 2", "Building B", "Bâtiment C"],
        json_schema_extra={"optional": True},
    )
    structure: str | None = Field(
        None,
        description="Structure (optional)",
        examples=["стр. 1", "Tower 1", "Tour Montparnasse"],
        json_schema_extra={"optional": True},
    )
    flat: str | None = Field(
        None,
        description="Apartment or office (optional)",
        examples=["кв. 42", "Apt 5B", "Bureau 301"],
        json_schema_extra={"optional": True},
    )
    postal_code: str | None = Field(
        None,
        description="Postal code",
        examples=["101000", "95035", "75008"],
        json_schema_extra={"optional": True},
    )


class AddressModel(BaseModel):
    address: Address = Field(
        ...,
        description="Address",
        examples=[
            {
                "region": "Московская область",
                "city": "Москва",
                "street": "ул. Тверская",
                "house": "д. 7",
                "flat": "кв. 15",
            },
            {
                "region": "Калифорния",
                "city": "Сан-Франциско",
                "street": "Market Street",
                "house": "1",
                "postal_code": "94105",
            },
        ],
    )


class PhoneAddressModel(AddressModel, PhoneModel): ...


class PhoneRequest(PhoneModel): ...


class UpdateAddressRequest(AddressModel): ...


class PhoneAddressRequest(PhoneAddressModel): ...


class AddressResponse(AddressModel): ...
