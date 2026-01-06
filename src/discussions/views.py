from django.shortcuts import render, redirect, get_object_or_404
from .models import DiscussionPost, DiscussionComment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q


# Create your views here.
def post_list(request):
    sort = request.GET.get("sort", "latest")
    if sort == "oldest":
        posts = DiscussionPost.objects.order_by("created_at")
    else:
        posts = DiscussionPost.objects.order_by("-created_at")

    q = request.GET.get("q", "").strip()
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))

    return render(
        request,
        "discussions/post_list.html",
        {
            "posts": posts,
            "sort": sort,
            "q": q,
            "show_search_bar": not request.is_staff,
        },
    )


def post_detail(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    comments = post.comments.order_by("created_at")
    return render(
        request, "discussions/post_detail.html", {"post": post, "comments": comments}
    )


@login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        link = request.POST.get("link")
        image = request.FILES.get("image")

        DiscussionPost.objects.create(
            author=request.user, title=title, content=content, link=link, image=image
        )
        return redirect("discussions:post_list")

    return render(request, "discussions/post_form.html")


@login_required
def comment_create(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")

        DiscussionComment.objects.create(
            post=post, author=request.user, content=content
        )
    return redirect("discussions:post_detail", post_id=post_id)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.link = request.POST.get("link")
        if request.FILES.get("image"):
            post.image = request.FILES.get("image")
        post.save()
        return redirect("discussions:post_detail", post_id=post.id)
    return render(request, "discussions/post_form.html", {"post": post})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(DiscussionPost, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == "POST":
        post.delete()
    return redirect("discussions:post_list")


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(DiscussionComment, id=comment_id)
    post_id = comment.post.id

    if comment.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == "POST":
        comment.delete()
    return redirect("discussions:post_detail", post_id=post_id)


@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(DiscussionComment, id=comment_id)
    post_id = comment.post.id

    if comment.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == "POST":
        comment.content = request.POST.get("content")
        comment.save()
        return redirect("discussions:post_detail", post_id=post_id)

    return render(
        request,
        "discussions/comment_form.html",
        {"comment": comment, "post_id": post_id},
    )
