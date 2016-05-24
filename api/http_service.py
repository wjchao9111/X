from X.tools import lazy_loader_const
from X.tools.middleware import JsonResponse
from base.models import User
from sms.tasks import send_task_prepare_sync
from sms.views import get_task

http_user_list = ['hbzh_admin']


@lazy_loader_const
def api_login(code, pwd):
    try:
        assert code in http_user_list
        user = User.objects.get(code=code)
        assert user.pwd == pwd
        assert user.stat == 'normal'
        return user
    except:
        return None


def send_sms(request):
    j_user = request.json.get('user')
    user = api_login(j_user.get('code'), j_user.get('pass'))
    if user:
        j_task = request.json.get('task')
        task = get_task(j_task)
        task.user_id = user.id
        task.save()
        taskcount, id_list = send_task_prepare_sync(task)
        return JsonResponse({'success': True, 'result_list': id_list})
    else:
        return JsonResponse({'success': False, 'error_code': 'User not found or disabled'})
