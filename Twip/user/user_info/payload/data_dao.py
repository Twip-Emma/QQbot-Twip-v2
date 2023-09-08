from .image_dao import get_card

async def get_user_data(user_id: str, user_name:str) -> str:
    await get_card(user_id)