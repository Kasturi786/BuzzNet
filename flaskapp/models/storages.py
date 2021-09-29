#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import gspread
import logging
from peewee import PostgresqlDatabase
from flaskapp.settings import (
    GOOGLE_SA_JSON_PATH,
    GOOGLE_USERS_SHEET_NAME_EXISTING,
    GOOGLE_USERS_SHEET_NAME_CALLS,
    GOOGLE_USERS_SPREADSHEET_ID,
    POSTGRESQL_DB_NAME,
    POSTGRESQL_HOST,
    POSTGRESQL_USER,
    POSTGRESQL_PORT,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_TEST_DB_NAME,
    TEST_ENVIRONMENT
)


__all__ = ('gs_users_existing', 'gs_users_calls', 'postgres_conn')


logger = logging.getLogger(__name__)


postgres_conn = PostgresqlDatabase(
    database=POSTGRESQL_TEST_DB_NAME if
    TEST_ENVIRONMENT else POSTGRESQL_DB_NAME,
    user=POSTGRESQL_USER,
    password=POSTGRESQL_PASSWORD,
    host=POSTGRESQL_HOST,
    port=POSTGRESQL_PORT
)


class GoogleSpreadSheet:
    gc = gspread.service_account(filename=GOOGLE_SA_JSON_PATH)

    def __init__(self, document_id='', sheet_name=''):
        self.document_id = document_id
        self.sheet_name = sheet_name
        self.spreadsheet = None
        self.worksheet = None

    def open_spreadsheet(self):
        self.spreadsheet = self.gc.open_by_key(self.document_id)
        self.worksheet = self.spreadsheet.worksheet(self.sheet_name)

    def append_row_to_sheet(self, row):
        if self.worksheet is None:
            self.open_spreadsheet()

        try:
            self.worksheet.append_row(row)
        except gspread.exceptions.APIError:
            try:
                self.gc.login()
                self.open_spreadsheet()
                self.worksheet.append_row(row)
            except gspread.exceptions.APIError:
                logger.error(f"Error raised while appending data to {self.sheet_name}.")  # noqa: 501
                return False
        return True


# interacts with users spreadsheet / Existing tab
gs_users_existing = GoogleSpreadSheet(
    GOOGLE_USERS_SPREADSHEET_ID,
    GOOGLE_USERS_SHEET_NAME_EXISTING
    )


# interacts with users spreadsheet / Calls tab
gs_users_calls = GoogleSpreadSheet(
    GOOGLE_USERS_SPREADSHEET_ID,
    GOOGLE_USERS_SHEET_NAME_CALLS
    )
