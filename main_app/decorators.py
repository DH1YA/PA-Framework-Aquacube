from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def group_required(*group_names):
    """
    Decorator to check if a user belongs to any of the specified groups.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user belongs to any of the specified groups
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                # Render custom 403 template
                return render(request, '403.html', status=403)
        
        return _wrapped_view
    return decorator
