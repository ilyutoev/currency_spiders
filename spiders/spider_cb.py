# -*- coding: utf-8 -*-
from models import create_tables, Bank

create_tables()
Bank.create(bank_id=1, bank_name="Центробанк")
   