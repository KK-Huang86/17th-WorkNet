import json
from urllib.parse import urlparse

import rules
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from lib.models.paginate import paginate_queryset
from lib.models.rule_required import rule_required

from .forms.jobs_form import JobForm
from .models import Job


def index(request):
    jobs = Job.objects.order_by("-id")
    jobs_with_permissions = [
        {"job": job, "can_edit": rules.test_rule("can_edit_job", request.user, job.id)}
        for job in jobs
    ]
    page_obj = paginate_queryset(request, jobs_with_permissions, 10)
    return render(request, "jobs/index.html", {"page_obj": page_obj})


def show(request, id):
    job = get_object_or_404(Job, pk=id)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)

            tags = request.POST.get("tags")
            if tags:
                tags = [tag["value"] for tag in json.loads(tags)]
                job.tags.set(tags, clear=False)

            job.save()
            messages.success(request, "更新成功")
            return redirect("jobs:show", job.id)
        else:
            return render(request, "jobs/edit.html", {"form": form, "job": job})

    previous_url = request.META.get("HTTP_REFERER", "/")
    referer_path = urlparse(previous_url).path
    backJobs = "resumes" not in referer_path
    return render(
        request,
        "jobs/show.html",
        {"job": job, "backJobs": backJobs, "tags": job.tags.all()},
    )


@rule_required("can_edit_job")
def edit(request, id):
    job = get_object_or_404(Job, pk=id)
    form = JobForm(instance=job)
    tags = list(job.tags.values_list("name", flat=True))

    return render(request, "jobs/edit.html", {"form": form, "job": job, "tags": tags})


def delete(request, id):
    job = get_object_or_404(Job, pk=id)
    job.mark_delete()
    messages.success(request, "刪除成功")
    return redirect("jobs:index")


LOCATION_MAP = {
    "基隆": "Keelung",
    "台北": "Taipei",
    "新北": "New Taipei",
    "桃園": "Taoyuan",
    "新竹": "Hsinchu",
    "苗栗": "Miaoli",
    "台中": "Taichung",
    "彰化": "Changhua",
    "南投": "Nantou",
    "雲林": "Yunlin",
    "嘉義": "Chiayi",
    "台南": "Tainan",
    "高雄": "Kaohsiung",
    "屏東": "Pingtung",
    "台東": "Taitung",
    "花蓮": "Hualien",
    "宜蘭": "Yilan",
    "澎湖": "Penghu",
    "金門": "Kinmen",
    "連江": "Lienchiang",
}


def get_location_code(location_input):
    return LOCATION_MAP.get(location_input, location_input)


def search_results(request):
    search_term = request.GET.get("q")
    location = request.GET.get("location")
    tags = request.GET.getlist("tags")

    search_filter = Q()
    search_term_list = []

    if search_term:
        search_term_list = [search_term.lower()]

        search_filter &= Q(title__icontains=search_term) | Q(
            company__name__icontains=search_term
        )

    if location:
        location_code = get_location_code(location)
        search_filter &= Q(location__icontains=location_code)

    jobs = (
        Job.objects.filter(search_filter)
        .select_related("company")
        .filter(tags__name__in=search_term_list)
        .distinct()
    )

    page_obj = paginate_queryset(request, jobs, 10)

    return render(
        request,
        "jobs/search_results.html",
        {
            "page_obj": page_obj,
            "tags": tags,
            "search_term": search_term,
            "location": location,
        },
    )
