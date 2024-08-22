import csv
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ReviewerReporterForm
from review import models as review_models

def reviewer_reporter(request):
    if request.method == 'POST':
        form = ReviewerReporterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Fetch peer review data
            review_requests = get_peer_review_data(start_date, end_date) 

            # Generate CSV response
            response = generate_csv_response(review_requests)
            return response

    else:  # GET request
        form = ReviewerReporterForm()

    context = {
        'form': form,
    }
    return render(request, 'reviewer_reporter/report.html', context)

def get_peer_review_data(start_date, end_date):
    review_requests = review_models.ReviewAssignment.objects.filter(
        date_requested__gte=start_date,
        date_requested__lte=end_date
    ).select_related(
        'reviewer', 'article'
    )

    # Prepare data for CSV export
    data = []
    for request in review_requests:
        reviewer_name = request.reviewer.full_name() if request.reviewer else "N/A"
        manuscript_number = request.article.pk 
        request_date = request.date_requested.strftime('%Y-%m-%d')

        # Determine review request status and dates
        if request.date_complete and request.decision != 'withdrawn':
            status = "Completed"
            status_date = request.date_complete.strftime('%Y-%m-%d')
            withdraw_date = "" 
        elif request.date_declined:
            status = "Declined"
            status_date = request.date_declined.strftime('%Y-%m-%d')
            withdraw_date = ""
        elif request.decision == 'withdrawn':
            status = "Withdrawn"
            status_date = ""
            withdraw_date = request.date_complete.strftime('%Y-%m-%d') if request.date_complete else "" 
        else:
            status = "Pending"
            status_date = ""
            withdraw_date = "" 

        accept_date = request.date_accepted.strftime('%Y-%m-%d') if request.date_accepted else ""
        complete_date = request.date_complete.strftime('%Y-%m-%d') if request.date_complete and request.decision != 'withdrawn' else "" 

        data.append([
            reviewer_name, 
            manuscript_number, 
            request_date, 
            status, 
            status_date,
            accept_date,
            complete_date,
            withdraw_date, 
        ])

    return data

    # Prepare data for CSV export
    data = []
    for request in review_requests:
        reviewer_name = request.reviewer.full_name() if request.reviewer else "N/A"
        manuscript_number = request.article.pk 
        request_date = request.date_requested.strftime('%Y-%m-%d')

        # Determine review request status and date
        if request.date_complete:
            status = "Completed"
            status_date = request.date_complete.strftime('%Y-%m-%d')
        elif request.date_declined:
            status = "Declined"
            status_date = request.date_declined.strftime('%Y-%m-%d')
        elif request.decision == 'withdrawn':
            status = "Withdrawn"
            status_date = request.date_complete.strftime('%Y-%m-%d') 
        else:
            status = "Pending"
            status_date = ""

        # Dates for accepted and completed reviews
        accept_date = request.date_accepted.strftime('%Y-%m-%d') if request.date_accepted else ""
        complete_date = request.date_complete.strftime('%Y-%m-%d') if request.date_complete else ""

        data.append([
            reviewer_name, 
            manuscript_number, 
            request_date, 
            status, 
            status_date,
            accept_date,
            complete_date
        ])

    return data

def generate_csv_response(review_requests):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reviewer_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Reviewer Name', 
        'Manuscript Number', 
        'Status of Review Request',
        'Date Review was Requested', 
        'Date Review was Accepted',
        'Date Review was Declined',
        'Date Review was Withdrawn',
        'Date Review was Completed',
    ])

    for row in review_requests:
        # Rearrange the data to match the new column order
        reviewer_name, manuscript_number, request_date, status, status_date, accept_date, complete_date, withdraw_date = row
        writer.writerow([
            reviewer_name, 
            manuscript_number, 
            status, 
            request_date,
            accept_date,
            status_date if status == "Declined" else "",  # Only populate if Declined
            withdraw_date if status == "Withdrawn" else "",  # Only populate if Withdrawn
            complete_date,
        ])

    return response