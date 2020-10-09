from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AboutSection
from .forms import AboutSectionForm
# Create your views here.


def about(request):
    """ view returns about page with about sections """
    about_sections = None
    about_sections = AboutSection.objects.all()
    context = {
        'about_sections': about_sections
    }
    return render(request, 'about/about.html', context)


@login_required
def add_section(request):
    """ view for admin to create about section """
    # only allow superuser access
    if not request.user.is_superuser:
        messages.error(
            request,
            "You must be logged in as KOR admin to do this"
        )
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = AboutSectionForm(request.POST)
        if form.is_valid():
            about_section = form.save()
            messages.success(
                request,
                f"New Section, \
                    {about_section.section_title} has been added to the store"
            )
            return redirect(reverse('about'))
        else:
            messages.error(
                request,
                'Failed to add new section. Double check the form is valid.'
            )
    else:
        form = AboutSectionForm()
    context = {
        'form': form,
    }

    return render(request, 'about/add_section.html', context)


@login_required
def edit_section(request, section_id):
    """ view for admin to update about section """
    # only allow superuser access
    if not request.user.is_superuser:
        messages.error(
            request,
            "You must be logged in as KOR admin to do this"
        )
        return redirect(reverse('home'))
    about_section = get_object_or_404(AboutSection, pk=section_id)
    if request.method == 'POST':
        form = AboutSectionForm(request.POST, instance=about_section)
        if form.is_valid():
            about_section = form.save()
            messages.success(
                request,
                f"New Section, \
                    {about_section.section_title} has been added to the store"
            )
            return redirect(reverse('about'))
        else:
            messages.error(
                request,
                'Failed to edit section. Double check the form is valid.'
            )
    else:
        form = AboutSectionForm(instance=about_section)

    context = {
        'form': form,
    }

    return render(request, 'about/edit_section.html', context)


@login_required
def delete_section(request, section_id):
    """ view for admin to delete about section """
    # only allow superuser access
    if not request.user.is_superuser:
        messages.error(
            request,
            "You must be logged in as KOR admin to do this"
        )
        return redirect(reverse('home'))

    about_section = get_object_or_404(AboutSection, pk=section_id)
    about_section.delete()
    messages.success(
        request,
        f"Successfully deleted \"{about_section.section_title}\""
    )
    return redirect(reverse('about'))
