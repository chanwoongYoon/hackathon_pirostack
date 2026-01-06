from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Question, Category, Answer
from .forms import QuestionForm, AnswerForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from users.decorators import staff_required


# Create your views here.


def question_list(request):
    """전체 질문 목록"""
    faq_questions = Question.objects.filter(is_faq=True).order_by("faq_order", "-created_at")[:5]
    #검색
    questions = Question.objects.all()
    q = request.GET.get("q", "").strip()
    if q:
        questions = questions.filter(Q(title__icontains=q) | Q(content__icontains=q))

    #정렬
    sort_param = request.GET.get("sort", "latest")
    if sort_param =="oldest":
        questions = questions.order_by("created_at", "id")
    else:
        questions = questions.order_by("-created_at", "-id")
    categories = Category.objects.all()
    context = {
        "questions": questions,
        "faq_questions":faq_questions,
        "categories": categories,
        "selected_sort": sort_param,
        "selected_category":None,
        "q":q,
    }
    

    return render(request, "questions/question_list.html", context)


def question_list_by_category(request, category_id):


    """
    [이서현] 카테고리별, 과제별, 시간순 정렬 및 필터링
    TODO: 커스텀 정렬 API 및 필터링 뷰 구현
    """
    faq_questions = Question.objects.filter(is_faq=True).order_by("faq_order", "-created_at")[:5]
    # 에러 방지를 위한 기본 구현
    category = get_object_or_404(Category, pk=category_id)  
    questions = Question.objects.filter(category=category)    

    #화면 렌더링에 필요한 카테고리 목록
    categories = Category.objects.all()
    sort_param = request.GET.get("sort", "latest") #기본값 lagtest로 설정
    session_categories = Category.objects.filter(category_type="session").order_by("name")
    assignment_categories = Category.objects.filter(category_type="assignment").order_by("name")

     #질문 검색
    q = request.GET.get("q", "").strip()

    if q:
        questions = questions.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        )

    #시간순 정렬 
    if sort_param == "oldest":
        questions = questions.order_by("created_at")
    else:
        questions = questions.order_by("-created_at")

    
    #템플릿에 전달할 데이터 꾸러미(context)
    context = {
        "questions": questions,
        "faq_questions":faq_questions,
        "categories": categories,
        "selected_category": category,

        "session_categories": session_categories,
        "assignment_categories": assignment_categories,
        "selected_sort": sort_param,
        "q":q,
    }

   
    #질문 리스트 페이지 렌더링
    return render(request, "questions/question_list.html", context)

@login_required
def my_questions(request):
    #내가 작성한 질문 리스트
    questions = Question.objects.filter(author=request.user)
    faq_questions = Question.objects.filter(is_faq=True).order_by("faq_order", "-created_at")[:5]

    #정렬
    sort_param=request.GET.get("sort","latest")
    if sort_param == "oldest":
        questions = questions.order_by("created_at", "id")
    else:
        questions = questions.order_by("-created_at", "-id")

    #카테고리 드롭다운
    categories = Category.objects.all().order_by("id")

    context = {
        "questions": questions,
        "faq_questions": faq_questions,
        "categories": categories,
        "selected_category": None,
        "selected_sort": sort_param,
        "page_title": "내가 작성한 질문",
    }
    return render(request, "questions/question_list.html", context)


@login_required
def my_scrapped_questions(request):
   
    #  내가 찜한 질문들 가져오기 
    questions = Question.objects.filter(scraps=request.user)
    faq_questions = Question.objects.filter(is_faq=True).order_by("faq_order", "-created_at")[:5]

    # 정렬 (기본 최신순)
    sort_param = request.GET.get("sort", "latest")
    if sort_param == "oldest":
        questions = questions.order_by("created_at", "id")
    else:
        questions = questions.order_by("-created_at", "-id")

    categories = Category.objects.all().order_by("id")

    context = {
        "questions": questions,
        "categories": categories,
        "selected_category": None,
        "selected_sort": sort_param,
        "page_title": "내가 찜한 질문",
        "faq_questions": faq_questions,
        
    }
    return render(request, "questions/question_list.html", context)

#찜기능 구현
@login_required
def toggle_scrap(request, pk):

    if request.method != "POST":
        return redirect("questions:detail", pk=pk)

    question = get_object_or_404(Question, pk=pk)

    # 이미 찜했으면 해제, 아니면 찜
    if request.user in question.scraps.all():
        question.scraps.remove(request.user)
    else:
        question.scraps.add(request.user)

    # 눌렀던 페이지로 다시 돌아가기 (없으면 상세로)
    return redirect(request.META.get("HTTP_REFERER", "questions:detail"))

def question_detail(request, pk):
    """질문 상세 페이지"""
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    context = {
        "question": question,
        "answers": answers,
    }
    return render(request, "questions/question_detail.html", context)


def question_create(request):
    """질문 작성"""
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = None
            question.is_anonymous = True
            question.save()
            return redirect("questions:detail", pk=question.pk)
    else:
        form = QuestionForm()

    return render(request, "questions/question_form.html", {"form": form})


def answer_create(request, pk):
    """답변 작성"""
    question = get_object_or_404(Question, pk=pk)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = None
            answer.is_anonymous = True
            answer.is_staff = False
            answer.save()

    return redirect("questions:detail", pk=pk)


def question_resolve(request, pk):
    """질문 해결 표시 토글"""
    question = get_object_or_404(Question, pk=pk)

    if request.method == "POST":
        question.is_resolved = not question.is_resolved
        question.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"is_resolved": question.is_resolved})

        return redirect("questions:detail", pk=pk)

    return redirect("questions:detail", pk=pk)


def question_update(request, pk):
    """질문 수정"""
    question = get_object_or_404(Question, pk=pk)

    # TODO: 작성자 본인 확인 로직 필요 (if request.user != question.author: ...)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect("questions:detail", pk=question.pk)
    else:
        form = QuestionForm(instance=question)

    return render(request, "questions/question_form.html", {"form": form})


def question_delete(request, pk):
    """질문 삭제"""
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        question.delete()
        return redirect("questions:list")
    return redirect("questions:detail", pk=pk)


def question_scrap(request, pk):
    """질문 찜하기 토글"""
    question = get_object_or_404(Question, pk=pk)

    if request.method == "POST":
        # 익명 사용자도 세션 기반으로 처리 가능하도록
        # TODO: 로그인 구현되면 request.user 사용
        # 현재는 간단히 전체 카운트만 증가/감소

        # 임시: 세션 기반 찜하기
        scrapped = request.session.get(f'scrapped_{pk}', False)
        request.session[f'scrapped_{pk}'] = not scrapped

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "scrapped": not scrapped,
                "scrap_count": question.scraps.count()
            })

        return redirect("questions:detail", pk=pk)

    return redirect("questions:detail", pk=pk)


def reply_create(request, pk, answer_pk):
    """꼬리질문(답변에 대한 대댓글) 작성"""
    question = get_object_or_404(Question, pk=pk)
    parent_answer = get_object_or_404(Answer, pk=answer_pk)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.question = question
            reply.parent = parent_answer
            reply.author = None
            reply.is_anonymous = True
            reply.is_staff = False
            reply.save()

    return redirect("questions:detail", pk=pk)






"""
[김서윤] 운영진 대시보드
"""

@staff_required
def staff_unanswered(request):
    questions = Question.objects.filter(is_resolved=False)
    categories = Category.objects.all().order_by("name")

    # 미답변 질문
    only_unanswered_param = request.GET.get("only_unanswered")
    if only_unanswered_param == "1":
        only_unanswered = "1"
    else:
        only_unanswered = "0"
    questions = Question.objects.all()
    if only_unanswered == "1":
        questions = questions.filter(is_resolved=False)


    # 필터링
    sort = request.GET.get("sort", "latest")
    if sort == "latest":
        questions = questions.order_by("-created_at")
    elif sort == "oldest":
        questions = questions.order_by("created_at")

    # 카테고리 필터
    category_id = request.GET.get("category")
    if category_id:
        questions = questions.filter(category_id=category_id)

    # 통계
    total_unanswered = Question.objects.filter(is_resolved=False).count() # 전체
    category_stats = ( # 카테고리별 미답변 개수
        Question.objects.filter(is_resolved=False)
        .values("category__name")
        .annotate(count=Count("id"))
    )

    session_categories = Category.objects.filter(category_type="session").order_by("name")
    assignment_categories = Category.objects.filter(category_type="assignment").order_by("name")

    return render(request, "questions/staff_unanswered.html", {
    "questions": questions,
    "sort": sort,
    "only_unanswered": only_unanswered,
    "total_unanswered": total_unanswered,
    "category_stats": category_stats,

    "session_categories": session_categories,
    "assignment_categories": assignment_categories,
    "categories": categories,
    
    })



@staff_required
def category_list(request):
    """카테고리 리스트"""
    sort = request.GET.get("sort", "latest")  # latest = 세션, oldest = 과제
    if sort == "latest":
        categories = Category.objects.filter(category_type="session").order_by("-created_at")
    else:
        categories = Category.objects.filter(category_type="assignment").order_by("-created_at")

    return render(request, "questions/category_list.html", {
        "categories": categories,
        "sort": sort,
    })


@staff_required
def category_create(request):
    """카테고리 생성"""
    if request.method == "POST":
        name = request.POST.get("name")
        category_type = request.POST.get("category_type", "session")
        if name:
            Category.objects.create(name=name, category_type=category_type)
            return redirect("questions:category_list")

    return render(request, "questions/category_form.html", {"action": "add"})


@staff_required
def category_update(request, pk):
    """카테고리 수정"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        category_type = request.POST.get("category_type")
        if name:
            category.name = name
            category.category_type = category_type
            category.save()
            return redirect("questions:category_list")

    return render(request, "questions/category_form.html", {"category": category, "action": "edit"})


@staff_required
def category_delete(request, pk):
    """카테고리 삭제"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("questions:category_list")

    return render(request, "questions/category_confirm_delete.html", {"category": category})