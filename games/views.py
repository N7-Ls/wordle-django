import os, math, random
from django.conf import settings
from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Avg
from django.contrib import messages
from django.contrib.sessions.models import Session

from . import forms, models

# ---------------------------------------------------------------------------

# 載入所有五字單字
DICT_PATH = os.path.join(settings.BASE_DIR, 'valid_words.txt')
with open(DICT_PATH, encoding='utf-8') as f:
    valid_words = [w.strip().lower() for w in f if len(w.strip()) == 5]

# 根據日期決定答案
def get_answer_for_date(current_date=None):
    if current_date is None:
        current_date = date.today()
    base_date = date(2025, 6, 16)
    index = (current_date - base_date).days % len(valid_words)
    return valid_words[index]

def evaluate_guess(guess, answer):
    result = ['X'] * 5
    answer_chars = list(answer)

    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = 'G'
            answer_chars[i] = None

    for i in range(5):
        if result[i] == 'X' and guess[i] in answer_chars:
            result[i] = 'Y'
            answer_chars[answer_chars.index(guess[i])] = None

    return ''.join(result)

# ---------------------------------------------------------------------------

def index(request):
	if 'username' in request.session:
		username = request.session['username']

	today = date.today()
	leaderboard = models.History.objects.filter(date__date=today, is_solved=True)\
	.select_related('user').order_by('total_attempts', 'date')[:10]

	return render(request, 'index.html', locals())

# 登入
def login(request):
	if request.method == "POST":
		login_form = forms.LoginForm(request.POST)
		if login_form.is_valid():
			login_name = request.POST['username'].strip()
			password = request.POST['password']
			try:
				user = models.User.objects.get(username=login_name)
				if user.password == password:
					request.session['username'] = user.username
					messages.add_message(request, messages.SUCCESS, '登入成功')
					return redirect('/')
				else:
					messages.add_message(request, messages.WARNING, '密碼錯誤')
			except:
				messages.add_message(request, messages.WARNING, '找不到使用者')
		else:
			messages.add_message(request, messages.INFO, '請檢查輸入欄位')
	else:
		login_form = forms.LoginForm()

	return render(request, 'login.html', locals())

# 註冊
def register(request):
	if request.method == "POST":
		register_form = forms.RegisterForm(request.POST)
		if register_form.is_valid():
			username = request.POST['username'].strip()
			password = request.POST['password']
			confirm = request.POST['confirm_password']
			if password != confirm:
				messages.add_message(request, messages.WARNING, '密碼不一致')
			else:
				if models.User.objects.filter(username=username).exists():
					messages.add_message(request, messages.WARNING, '使用者名稱已存在')
				else:
					user = models.User.objects.create(username=username, password=password)
					request.session['username'] = user.username
					messages.add_message(request, messages.SUCCESS, '註冊成功')
					return redirect('/daily/')
		else:
			messages.add_message(request, messages.INFO, '請填寫所有欄位')
	else:
		register_form = forms.RegisterForm()

	return render(request, 'register.html', locals())

# 個人紀錄與統計資料
def info(request):
	if 'username' not in request.session:
		return redirect('/login/')

	username = request.session['username']
	user = models.User.objects.get(username=username)
	history = models.History.objects.filter(user=user).order_by('-date')

	# 統計
	total_games = history.count()
	solved_games = history.filter(is_solved=True).count()
	avg_attempts = history.filter(is_solved=True).aggregate(Avg('total_attempts'))['total_attempts__avg'] or 0
	# day streak 可之後補上

	return render(request, 'info.html', locals())

# 每日遊戲
def daily(request):
    if 'username' not in request.session:
        return redirect('/login/')

    # 每次進入 daily 時自動檢查並清除非今日的 Guess 資料
    models.Guess.objects.exclude(date=date.today()).delete()

    username = request.session['username']
    user = models.User.objects.get(username=username)
    today = date.today()

    today_answer = get_answer_for_date(today)

    # 取得今日歷史紀錄或建立新紀錄
    history, created = models.History.objects.get_or_create(
        user=user, date__date=today,
        defaults={'answer': today_answer, 'is_solved': False, 'total_attempts': 0}
    )

    guesses = models.Guess.objects.filter(user=user, date=today).order_by('attempt_times')

    if request.method == "POST":
        guess_form = forms.GuessForm(request.POST)
        if guess_form.is_valid():
            guess_word = request.POST['guess_word'].strip().lower()

            # 檢查是否為合法單字
            if guess_word not in valid_words:
                messages.add_message(request, messages.WARNING, '不是合法單字')
                return redirect('/daily/')
            # 若已猜中或次數已滿則不再處理
            elif history.is_solved:
                messages.add_message(request, messages.INFO, '你已完成今天的挑戰')
                return redirect('/daily/')
            elif history.total_attempts >= 6:
                messages.add_message(request, messages.INFO, '你已用完今天的 6 次機會')
                return redirect('/daily/')

            # 比對並紀錄結果
            result = evaluate_guess(guess_word, history.answer)
            history.total_attempts += 1
            models.Guess.objects.create(
                user=user, date=today, guess_word=guess_word, result=result, attempt_times=history.total_attempts
            )

            if result == 'GGGGG':
                history.is_solved = True
            else:
                messages.add_message(request, messages.INFO, f'結果：{result}')
            history.save()

            return redirect('/daily/')
        else:
            messages.add_message(request, messages.WARNING, '請輸入有效單字')
    else:
        guess_form = forms.GuessForm()

    return render(request, 'daily.html', locals())



def logout(request):
	if 'username' in request.session:
		Session.objects.all().delete()

	return redirect('/')