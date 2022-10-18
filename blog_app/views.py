from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from .forms import ContactForm, SignUpForm, UserUpdateForm, CommentForm, LoginForm
from django.core.mail import send_mail
from .models import Comment, Post, Category, EmailVerification
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
import uuid


# print category
def print_category():
    return Category.objects.all()


# Login
class UserLoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            form.order_fields(field_order=["username","email","password"])
            context = {
                'ctgry':print_category(),
                'form':form
            }
            return render(request, 'blog_app/login.html', context)
        messages.info(request, 'You have already logedin.')
        return redirect('/profile/')

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        form.order_fields(field_order=["username","email","password"])
        
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = authenticate(username=uname, password=upass)

            if user is not None:
                email_verify_obj = EmailVerification.objects.get(user=user)
                if email_verify_obj.verify:
                    login(request, user)
                    messages.success(request, 'Login Successfully.')
                    return redirect('/profile/')
                else:
                    messages.info(request, 'Your Account is not verified, please check your email to verify!')
                    return redirect('/accounts/login/')
        context = {
                'ctgry':print_category(),
                'form':form
            }
        return render(request, 'blog_app/login.html', context)


# home view
class HomeView(View):
        def get(self, request, cat='All'):
            try:
                # filtering post acording to category
                all_post = ''
                if cat == 'All':
                    all_post = Post.objects.order_by('?')[:20]
                else:
                    category_id = Category.objects.get(title=cat).id
                    all_post = Post.objects.filter(category=category_id)

                context = {
                    'all_post':all_post,
                    'latest_post':Post.objects.order_by('date').reverse()[:5],
                    'ctgry':print_category(),
                }
                return render(request, 'blog_app/home.html', context)
            except Exception as e:
                return redirect('/')
    


# Contact View
class ContactView(View):
    def get(self, request):
        context = {
            'form':ContactForm(),
            'ctgry':print_category()
            }
        return render(request, 'blog_app/contact.html', context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            con_message = form.cleaned_data['desc']
            # sending mail
            subject = "Contact Form Mail."
            message = f"Name : {name}\nPhone : {phone}\nEmail : {email}\n{con_message}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['subodhm457@gmail.com', 'subodh.minz.code@gmail.com']
            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
            messages.success(request, 'Your message has been sent!')
        return redirect('/contact/')


# detail post view
def postDetail(request, id, cat='All'):
    try:
        comment_form = CommentForm()
        # filtering best product
        category_id = Category.objects.get(title='Best Product').id
        best_products = Post.objects.filter(category=category_id).order_by('?')[:5]
        # getting category
        post = Post.objects.filter(pk=id).first()
        comments = Comment.objects.filter(post=post)[:5]
        if request.method == 'POST':
            if request.user.is_authenticated:
                # comment section
                post_instence = Post.objects.get(pk=id)
                comments_data = CommentForm(request.POST)
                if comments_data.is_valid():
                    message = comments_data.cleaned_data['message']
                    comment_obj = Comment(post=post_instence, user=request.user, message=message)
                    comment_obj.save()
                else:
                    return redirect(f'/postdetail/{id}/')

            else:
                return redirect('/accounts/login/')
        else:
            comment_form = CommentForm()
        
        context = {
            'comments':comments,
            'po_dtl':Post.objects.get(pk=id),
            'comment_form':comment_form,
            'latest_post':Post.objects.order_by('date').reverse()[:5],
            'ctgry':print_category(),
            'best_products':best_products
        }
        return render(request, 'blog_app/post_detail.html', context)
    except Exception as e:
        return redirect('/')


# search view
def search(request):
    search_form_data = request.GET
    search_form_data = search_form_data['search'].title()
    all_post = Post.objects.filter(title__icontains=search_form_data)
    context = {
        'all_post':all_post,
        'latest_post':Post.objects.order_by('date').reverse()[:5],
        'ctgry':print_category(),
    }
    return render(request, 'blog_app/home.html', context)

# About View
class AboutView(View):
    def get(self, request):
        return render(request, 'blog_app/about.html', {'ctgry':print_category()})


# send mail to verify account  
def send_mail_to_verify(email, token):
    subject = "Verify Email"
    message = f"Hi Click on the link to verify your account http://127.0.0.1:8000/account_verify/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)


# sign up view
class UserSignUpView(TemplateView):
    def get(self, request):
        if not request.user.is_authenticated:
            context = {
                'form':SignUpForm(),
                'auth':'Sign Up',
                'ctgry':print_category(),
            }
            return render(request, 'blog_app/signup.html', context)
        else:
            messages.info(request, 'You have logedin. Please logout first!')
            return redirect('/profile/')

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            uid = uuid.uuid4()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if User.objects.filter(email=email).exists():
                messages.info(request, 'This email has already taken!')
            else:
                user_obj = form.save()
                EmailVerification_obj = EmailVerification(user=user_obj, token=uid)
                EmailVerification_obj.save()
                send_mail_to_verify(user_obj.email, uid)
                messages.success(request, "Your account created successfully, to verify your Account Check your Email")
                return redirect('/accounts/login/')

        context = {
                'form':form,
                'auth':'Sign Up',
                'ctgry':print_category(),
            }
        return render(request, 'blog_app/signup.html', context)
            

# account verify
def account_verify(request, token):
    email_verify = EmailVerification.objects.get(token=token)
    email_verify.verify = True
    email_verify.save()
    return redirect('/accounts/login/')

# User Profile View
def user_profile(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You are not login, without login you can not access Progile!')
        return redirect('/')

    else:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
            context = {
            'u_form':u_form,
            }
            return render(request, 'blog_app/user_profile.html', context)
        else:
            u_form = UserUpdateForm(instance=request.user)
            context = {
            'ctgry':print_category(),
            'u_form':u_form,
            }
            return render(request, 'blog_app/user_profile.html', context)