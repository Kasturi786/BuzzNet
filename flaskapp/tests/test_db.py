#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
This file is a part of heartvoices.org project.

The software embedded in or related to heartvoices.org
is provided under a some-rights-reserved license. This means
that Users are granted broad rights, including but not limited
to the rights to use, execute, copy or distribute the software,
to the extent determined by such license. The terms of such
license shall always prevail upon conflicting, divergent or
inconsistent provisions of these Terms. In particular, heartvoices.org
and/or the software thereto related are provided under a GNU GPLv3 license,
allowing Users to access and use the software’s source code.
Terms and conditions: https://www.goandtodo.org/terms-and-conditions

Created Date: Friday October 1st 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Friday, October 15th 2021, 11:44:29 am
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


import pytest
from flaskapp.models.ivr_models import (HealthMetric, User,
                                        Reminder,
                                        SmartReminder,
                                        Call,
                                        PhoneNumber)
from flaskapp.models.utils import create_tables, init_db, drop_all_tables
from flaskapp.models.storages import postgres_db


def test_create_and_drop_tables():
    drop_all_tables()
    tables = postgres_db.get_tables()
    assert len(tables) == 0
    init_db()
    tables_created = postgres_db.get_tables()
    assert len(tables_created) > 0
    assert 'users' in tables_created
    assert 'calls' in tables_created
    assert 'reminders' in tables_created
    assert 'phone_numbers' in tables_created
    assert 'health_metrics' in tables_created
    assert 'smart_reminders' in tables_created
