from pydantic import BaseModel, Field, ConfigDict


class TransferRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_user: str = Field(alias="from")
    to_user: str = Field(alias="to")
    amount: float = Field(gt=0)