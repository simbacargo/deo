import os
import json
from PIL import Image
from django.conf import settings as django_settings
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
import datetime
from authentication.models import User
from typing import Any


def terms_and_condition(request: Any) -> HttpResponse:
    return render(request, 'terms.html', {})


@login_required
def network(request: Any) -> HttpResponse:
    users_list = User.objects.filter(is_active=True).order_by('username')
    paginator = Paginator(users_list, 100)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)

    except PageNotAnInteger:
        users = paginator.page(1)

    except EmptyPage:  # pragma: no cover
        users = paginator.page(paginator.num_pages)

    return render(request, 'core/network.html', {'users': users})

    
from typing import Any, Callable, Optional, TypeVar
from django.views.decorators.cache import cache_page
@login_required
# @cache_page(60)
def profile(request, username) -> Callable:
    page_user = get_object_or_404(User, username=username)
    # all_feeds = Feed.get_feeds().filter(user=page_user)
    # paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    # feeds = paginator.page(1)
    feeds = 0
    from_feed = -1
    if feeds:  # pragma: no cover
        # from_feed = feeds[0].id
        from_feed = 1

    feeds_count = 0#Feed.objects.filter(user=page_user).count()
    article_count = 0#Article.objects.filter(create_user=page_user).count()
    article_comment_count = 0#ArticleComment.objects.filter(user=page_user).count()
    question_count = 0#Question.objects.filter(user=page_user).count()
    answer_count = 0#Answer.objects.filter(user=page_user).count()
    activity_count = 0#Activity.objects.filter(user=page_user).count()
    messages_count = 0#Message.objects.filter(Q(from_user=page_user) | Q(user=page_user)).count()
    data, datepoints = 0,0#Activity.daily_activity(page_user)

    ac = User.objects.get(username=request.user)
    account = ac
    data = {
        'page_user': page_user,
        'feeds_count': feeds_count,
        'article_count': article_count,
        'article_comment_count': article_comment_count,
        'question_count': question_count,
        'global_interactions': activity_count + messages_count,  # noqa: E501
        'answer_count': answer_count,
        'bar_data': [
            feeds_count,
            article_count, article_comment_count, question_count,
            answer_count,
             activity_count],
        'bar_labels': json.dumps('["Feeds", "Articles", "Comments", "Questions", "Answers", "Activities"]'),  # noqa: E501
        'line_labels': datepoints,
        'line_data': data,
        'feeds': feeds,
        'account':account,
        'from_feed': from_feed,
        'page': 1
        }


    # is_friend
    # try:
    #     import Friend
    #     friend_list = Friends.objects.get(user=account)
    # except #Friends.DoesNotExist:
    #     friend_list = Friends(user=account)
    #     friend_list.save()
    # friends = friend_list.friends.all()
    # data['friends'] = friends
    
    # # Define template variables
    # is_self = True
    # is_friend = False
    # request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
    # friend_requests = None
    # user = request.user
    # if user.is_authenticated and user != account:
    #     is_self = False
    #     if friends.filter(pk=user.id):
    #         is_friend = True
    #     else:
    #         is_friend = False
    #         # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
    #         if get_friend_request_or_false(sender=account, receiver=user) != False:
    #             request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
    #             context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
    #         # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
    #         elif get_friend_request_or_false(sender=user, receiver=account) != False:
    #             request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
    #         # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
    #         else:
    #             request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    
    # elif not user.is_authenticated:
    #     is_self = False
    # else:
    #     try:
    #         friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
    #     except:
    #         pass
        
    # Set the template variables to the values
    # data['is_friend'] = is_friend
    # data['request_sent'] = request_sent
    # data['friend_requests'] = friend_requests
    # from config.settings import BASE_URL
    # data['BASE_URL'] =      BASE_URL
    # # return render(request, "account/account.html", context)

    # data['friends']=friends
    # data['friend_requests']=friend_requests
    # data['request_sent']=request_sent
    # data['hide_email']=True #Atleas for now, later change tis to a user defined fild
    # data['is_friend']=  False #Atleas for now, later change tis to a user defined fild
    # data['is_self']=is_self
    
    return render(request, 'users-profile.html', data)
