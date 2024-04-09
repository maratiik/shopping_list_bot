from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReactionTypeEmoji
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
from sqlalchemy import Engine

from texts import texts
from text.text_makers import split_url
import keyboards.keyboards as keys
from util.states import BotState
from database.controller import ItemDAO, FavouriteDAO
from database.item_data import ItemData


delete_router = Router()
#TODO: ручки