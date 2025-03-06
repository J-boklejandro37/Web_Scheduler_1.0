from django.shortcuts import redirect

# Wrapper function for checking if there's a session
def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get("user_id"):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/accounts/entrance/')
    return wrapper