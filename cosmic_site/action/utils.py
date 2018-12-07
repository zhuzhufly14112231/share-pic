#!/usr/bin/env python
# encoding: utf-8
'''
@file: utils.py
@time: 2018/11/19 16:47
'''
import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from action.models import Action


def create_action(user,verb,target=None):
    # 检查最后一分钟内的相同动作
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    # gte 大于等于     lte 小于等于
    similar_actions = Action.objects.filter(user_id=user.id,verb=verb,created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,target_id=target.id)
    if not similar_actions:
        action = Action(user=user,verb=verb,target=target)
        action.save()
        return True
    return False



 