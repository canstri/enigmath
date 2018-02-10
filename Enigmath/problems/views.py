from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from accounts.models import Profile
from .solve_problem_form import SolveProblemForm
from .models import Problem
from .models import CheckProblem

from olymps.models import Olymp
from lemmas.isequal import isequal


def problem_delete(request, id):
    try:
        obj = Problem.objects.get(id=id)
    except:
        raise Http404

    if obj.user != request.user:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()

        for checkprblm in CheckProblem.objects.filter(problem_id = obj.id):
            checkprblm.delete()

        obj.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    staff = "no"

    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

    context = {
        "staff":staff,
        "profile":profile,
        "object": obj,
    }
    return render(request, "confirm_delete.html", context)

def problem_thread(request, id):
    try:
        obj = Problem.objects.get(id=id)
    except:
        raise Http404

    content_object = obj.content_object # Post that the problem is on
    content_id = obj.content_object.id

    initial_data = {
            "content_type": obj.content_type,
            "object_id": obj.object_id
    }

    solve_problem_form = SolveProblemForm(request.POST or None)
    action_check = False
    if solve_problem_form.is_valid():
        expr1 = solve_problem_form.cleaned_data.get('expr1')
        expr2 = solve_problem_form.cleaned_data.get('expr2')
        action_check = isequal(expr1)

    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
    
    check_problem = CheckProblem.objects.filter(problem_id = obj.id, user = request.user.id)[0]

    context = {
        "staff":staff,
        "profile":profile,
        "problem": obj,
        "solve_problem_form": solve_problem_form,
        "check_problem": check_problem,
        "action_check":action_check,
    }
    return render(request, "problem.html", context)